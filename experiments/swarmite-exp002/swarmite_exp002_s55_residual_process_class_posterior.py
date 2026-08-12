import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s51_residual_diagnostic as s51
import swarmite_exp002_s54_nodewise_residual_composition as s54

REGIMES=s54.REGIMES


def explicit_class_posterior(ps30,phet,pclass):
    m30=b.edge_marginals(ps30); mh=b.edge_marginals(phet)
    out=np.zeros(len(b.dags),float)
    for zmask in range(1<<b.N):
        q=1.0
        logp=np.zeros(len(b.dags),float)
        for v in range(b.N):
            use_h=bool((zmask>>v)&1)
            q*=float(pclass[v] if use_h else 1.0-pclass[v])
        if q<=0: continue
        for k,(u,v) in enumerate(b.EDGES):
            m=float(mh[k] if ((zmask>>v)&1) else m30[k])
            m=min(max(m,1e-6),1-1e-6)
            present=((b.dags>>k)&1).astype(bool)
            logp += np.where(present,np.log(m),np.log1p(-m))
        logp-=logp.max(); p=np.exp(logp); p/=p.sum(); out += q*p
    s=out.sum()
    if not np.isfinite(s) or s<=0: raise ValueError('invalid S55 mixture')
    out/=s
    return out


def entropy_binary(p):
    p=np.clip(np.asarray(p,float),1e-12,1-1e-12)
    return float(np.mean(-(p*np.log(p)+(1-p)*np.log(1-p))))


def evaluate(rows,model,seed):
    control=[]; cand=[]; control_b=[]; cand_b=[]; probs=[]; wins=[]; outer=[]; regs=[]; ent=[]
    harms_c=harms_x=0
    for r in rows:
        ps=np.asarray(r['ps30'],float); ph=np.asarray(r['phet'],float)
        pwin,pg,_=s54.predict_weights(r,model)
        p55=explicit_class_posterior(ps,ph,pwin)
        mm=b.posterior_metrics(p55,r['true_mask'])
        ce=float(mm['edge_error']-r['baseline_edge_error']); cb=float(mm['brier']-r['baseline_brier']); op=bool(r['outer_promote'])
        c0=r['s30_edge_delta_vs_baseline'] if op else 0.0; x0=ce if op else 0.0
        c0b=r['s30_brier_delta_vs_baseline'] if op else 0.0; x0b=cb if op else 0.0
        control.append(c0); cand.append(x0); control_b.append(c0b); cand_b.append(x0b); probs.extend(pwin.tolist()); wins.extend(r['node_win']); outer.append(op); regs.append(r['regime']); ent.append(entropy_binary(pwin))
        harms_c += int(op and r['s30_edge_delta_vs_baseline']>.50); harms_x += int(op and ce>.50)
    control=np.asarray(control); cand=np.asarray(cand); diff=cand-control; probs=np.asarray(probs); wins=np.asarray(wins,bool); outer=np.asarray(outer,bool)
    prev=float(model['train_win_prevalence']); node_brier=float(np.mean((probs-wins.astype(float))**2)); const=float(np.mean((prev-wins.astype(float))**2)); auc=s51.auc(probs,wins)
    by={}
    for rg in REGIMES:
        idx=np.asarray([x==rg for x in regs],bool)
        rg_probs=np.concatenate([s54.predict_weights(rows[i],model)[0] for i in range(len(rows)) if idx[i]])
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),'paired_mean_edge_difference':float(np.mean(diff[idx])),'mean_heteroskedastic_class_mass':float(np.mean(rg_probs))}
    return {'coverage':float(np.mean(outer)),'mean_heteroskedastic_class_mass':float(np.mean(probs)),'mean_class_entropy':float(np.mean(ent)),'control_hybrid_mean_edge_delta':float(np.mean(control)),'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':s54.boot(diff,seed=seed),'control_hybrid_mean_brier_delta':float(np.mean(control_b)),'candidate_hybrid_mean_brier_delta':float(np.mean(cand_b)),'control_promoted_large_harms':int(harms_c),'candidate_promoted_large_harms':int(harms_x),'node_specialist_win_auc':auc,'node_specialist_win_brier':node_brier,'constant_prevalence_brier':const,'by_regime':by,'mechanics_ok':s54.mechanics(rows,int(len(rows)/2))}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']; auc=ev['node_specialist_win_auc']
    ok=(ev['mechanics_ok'] and .05<=ev['mean_heteroskedastic_class_mass']<=.50 and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.01 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.02 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.02 and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and ev['candidate_hybrid_mean_brier_delta']<=.005 and auc is not None and auc>=.60 and ev['node_specialist_win_brier']<=ev['constant_prevalence_brier'])
    if validation or confirmation: ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.01
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.02
    return bool(ok)


def generate(start,n_each): return s54.generate(start,n_each)
def mechanics(rows,n_each): return s54.mechanics(rows,n_each)
def train_model(rows): return s54.train_model(rows)

if __name__=='__main__':
    me=generate(84501,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(84601,64); model=train_model(tr); ev=evaluate(tr,model,25555); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']='FALSIFIED_AT_TRAINING'
        else:
            va=generate(85001,32); vv=evaluate(va,model,25556); out['validation']=vv
            if not qualifies(vv,validation=True): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(85501,64); cv=evaluate(co,model,25557); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,validation=True,confirmation=True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
