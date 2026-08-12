import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s59_residual_state_evidence_decomposition as s59
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s61_bounded_predictive_state_structural_correction as s61
import swarmite_exp002_s62_posterior_disagreement_parent_proposal as s62

REGIMES=('linear','heteroskedastic')
RIDGE=5.0
MAX_TILT=0.75
FEATURES=s62.FEATURES


def world_base(external_seed):
    base=s54.world_base(external_seed); reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed); fs,_=b.build_family_models(data,targets)
    nodes=[]
    for v in range(b.N):
        truth=s59.true_parent_mask(base['true_mask'],v); margin=s59.margin(fs,v,truth); sel,comp,feat=s62.node_diagnostic(data,targets,fs,v)
        nodes.append({'node':int(v),'selected_parent_mask':int(sel),'competitor_parent_mask':int(comp),'anchor_rank_error':bool(margin<0),
                      'competitor_better_than_selected':bool(s62.hamming(comp,truth)<s62.hamming(sel,truth)),
                      'features':[float(feat[k]) for k in FEATURES],'competitor_mean_mass':float(feat['competitor_mean_mass'])})
    base=dict(base); base['nodes']=nodes; base['mechanics_ok']=bool(base['mechanics_ok'] and all(np.all(np.isfinite(n['features'])) for n in nodes)); return base


def generate(start,n_each): return [world_base(s) for s in s60.selected(start,n_each)]

def mechanics(rows,n_each):
    return len(rows)==2*n_each and all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] and len(r['nodes'])==b.N for r in rows)


def node_matrix(rows,mean=None,std=None):
    Z=np.asarray([n['features'] for r in rows for n in r['nodes']],float)
    if mean is None: mean=Z.mean(0)
    if std is None: std=Z.std(0); std=np.where(std<1e-8,1.0,std)
    return np.column_stack([np.ones(len(Z)),(Z-np.asarray(mean))/np.asarray(std)]),np.asarray(mean),np.asarray(std)


def fit_logistic(X,y): return s61.fit_logistic(X,y,RIDGE)

def train_model(rows):
    X,mean,std=node_matrix(rows); y=np.asarray([n['anchor_rank_error'] for r in rows for n in r['nodes']],float); beta,prev=fit_logistic(X,y)
    return {'feature_names':list(FEATURES),'mean':mean.tolist(),'std':std.tolist(),'beta':beta.tolist(),'train_error_prevalence':float(prev),'ridge_lambda':RIDGE,'max_tilt':MAX_TILT}


def node_predictions(row,model):
    Z=np.asarray([n['features'] for n in row['nodes']],float); X=np.column_stack([np.ones(len(Z)),(Z-np.asarray(model['mean']))/np.asarray(model['std'])]); p=s61.sigmoid(X@np.asarray(model['beta']))
    prev=float(model['train_error_prevalence']); activation=np.clip((p-prev)/max(1-prev,1e-6),0,1); K=float(1<<(b.N-1)); uni=1.0/K
    q=np.asarray([n['competitor_mean_mass'] for n in row['nodes']],float); reliability=np.clip((q-uni)/max(1-uni,1e-6),0,1); lam=float(model['max_tilt'])*activation*reliability
    for i,n in enumerate(row['nodes']):
        if n['competitor_parent_mask']==n['selected_parent_mask']: lam[i]=0.0
    return p,lam


def corrected_posterior(row,model):
    ps=np.asarray(row['ps30'],float); pnode,lam=node_predictions(row,model); logp=np.log(np.clip(ps,1e-300,None))
    for j,dagmask in enumerate(b.dags):
        add=0.0
        for v,n in enumerate(row['nodes']):
            if lam[v]<=0: continue
            pm=s61.dag_parent_mask(dagmask,v)
            if pm==n['competitor_parent_mask']: add+=lam[v]
            elif pm==n['selected_parent_mask']: add-=lam[v]
        logp[j]+=add
    logp-=np.max(logp); p=np.exp(logp); p/=p.sum(); return p,pnode,lam


def evaluate(rows,model,seed):
    control=[]; cand=[]; control_b=[]; cand_b=[]; regs=[]; probs=[]; labels=[]; lams=[]; outer=[]; harms_c=harms_x=0; err=use=0
    for r in rows:
        pc,pnode,lam=corrected_posterior(r,model); mm=b.posterior_metrics(pc,r['true_mask']); ce=float(mm['edge_error']-r['baseline_edge_error']); cb=float(mm['brier']-r['baseline_brier']); op=bool(r['outer_promote'])
        c0=float(r['s30_edge_delta_vs_baseline']) if op else 0.; x0=ce if op else 0.; c0b=float(r['s30_brier_delta_vs_baseline']) if op else 0.; x0b=cb if op else 0.
        control.append(c0); cand.append(x0); control_b.append(c0b); cand_b.append(x0b); regs.append(r['regime']); outer.append(op); probs.extend(pnode.tolist()); labels.extend([n['anchor_rank_error'] for n in r['nodes']]); lams.extend(lam.tolist())
        harms_c+=int(op and r['s30_edge_delta_vs_baseline']>.50); harms_x+=int(op and ce>.50)
        for n in r['nodes']:
            if n['anchor_rank_error']: err+=1; use+=int(n['competitor_better_than_selected'])
    control=np.asarray(control); cand=np.asarray(cand); diff=cand-control; probs=np.asarray(probs); labels=np.asarray(labels,bool); lams=np.asarray(lams); outer=np.asarray(outer,bool); prev=float(model['train_error_prevalence'])
    auc=s60.auc(labels,probs); bri=float(np.mean((probs-labels.astype(float))**2)); const=float(np.mean((prev-labels.astype(float))**2)); by={}
    for rg in REGIMES:
        idx=np.asarray([x==rg for x in regs],bool); by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),'paired_mean_edge_difference':float(np.mean(diff[idx]))}
    return {'coverage':float(np.mean(outer)),'mean_local_tilt':float(np.mean(lams)),'nonzero_correction_fraction':float(np.mean(lams>1e-10)),
            'control_hybrid_mean_edge_delta':float(np.mean(control)),'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':s61.boot(diff,seed=seed),
            'control_hybrid_mean_brier_delta':float(np.mean(control_b)),'candidate_hybrid_mean_brier_delta':float(np.mean(cand_b)),'control_promoted_large_harms':int(harms_c),'candidate_promoted_large_harms':int(harms_x),
            'error_localization_auc':auc,'error_localization_brier':bri,'constant_prevalence_brier':const,'n_anchor_error_nodes':int(err),'competitor_useful_fraction_on_error_nodes':float(use/max(1,err)),'by_regime':by,'mechanics_ok':mechanics(rows,int(len(rows)/2))}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']; auc=ev['error_localization_auc']
    ok=(ev['mechanics_ok'] and .02<=ev['nonzero_correction_fraction']<=.60 and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.005 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.01 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.015 and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and ev['candidate_hybrid_mean_brier_delta']<=ev['control_hybrid_mean_brier_delta']+.005 and auc is not None and auc>=.60 and ev['error_localization_brier']<=ev['constant_prevalence_brier'] and ev['competitor_useful_fraction_on_error_nodes']>.50)
    if validation: ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.005
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.01
    return bool(ok)

def failure_class(ev):
    if ev.get('error_localization_auc') is None or ev['error_localization_auc']<.60 or ev['competitor_useful_fraction_on_error_nodes']<=.50: return 'FALSIFIED_TARGETING'
    return 'FALSIFIED_CORRECTION_GEOMETRY'

if __name__=='__main__':
    me=generate(95601,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(95701,64); model=train_model(tr); ev=evaluate(tr,model,26363); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']=failure_class(ev)+'_AT_TRAINING'
        else:
            va=generate(96101,32); vv=evaluate(va,model,26364); out['validation']=vv
            if not qualifies(vv,validation=True): out['disposition']=failure_class(vv)+'_ON_VALIDATION'
            else:
                co=generate(96401,64); cv=evaluate(co,model,26365); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,validation=True,confirmation=True) else failure_class(cv)+'_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
