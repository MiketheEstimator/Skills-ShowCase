import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s61_bounded_predictive_state_structural_correction as s61
import swarmite_exp002_s64_constrained_local_posterior_projection as s64

REGIMES=('linear','heteroskedastic')


def generate(start,n):
    return [s64.world_base(s) for s in s60.selected(start,n)]


def mechanics(rows,n):
    return len(rows)==2*n and all(sum(r['regime']==rg for r in rows)==n for rg in REGIMES) and all(
        r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in rows)


def train_model(rows):
    return s64.train_model(rows)


def local_marginal(p,v,pms):
    p=np.asarray(p,float); z=np.zeros(len(pms),float); ix={pm:i for i,pm in enumerate(pms)}
    for j,d in enumerate(b.dags): z[ix[s64.dag_pm(d,v)]] += p[j]
    z=np.clip(z,1e-12,None); return z/z.sum()


def expected_hamming_risk(action_pm,pms,belief):
    return float(sum(float(q)*s62_hamming(action_pm,pm) for pm,q in zip(pms,belief)))


def s62_hamming(a,c):
    return int((int(a)^int(c)).bit_count())


def choose_dag_from_beliefs(node_beliefs):
    risks=[]
    for d in b.dags:
        loss=0.0
        for v,(pms,belief) in enumerate(node_beliefs):
            loss += expected_hamming_risk(s64.dag_pm(d,v),pms,belief)
        risks.append(loss)
    return int(b.dags[int(np.argmin(np.asarray(risks,float)))])


def posterior_action(p,row):
    beliefs=[]
    for v,n in enumerate(row['nodes']):
        pms=n['pms']; beliefs.append((pms,local_marginal(p,v,pms)))
    return choose_dag_from_beliefs(beliefs)


def predictions(row,model):
    Z=np.asarray([n['features'] for n in row['nodes']],float)
    X=np.column_stack([np.ones(len(Z)),(Z-np.asarray(model['mean']))/np.asarray(model['std'])])
    return s61.sigmoid(X@np.asarray(model['beta']))


def candidate_action(row,model):
    pe=predictions(row,model); beliefs=[]
    p30=np.asarray(row['ps30'],float)
    for v,n in enumerate(row['nodes']):
        pms=n['pms']; m30=local_marginal(p30,v,pms); q62=np.asarray(n['q62'],float); q62=np.clip(q62,1e-12,None); q62/=q62.sum()
        dv=(1-float(pe[v]))*m30+float(pe[v])*q62; dv=np.clip(dv,1e-12,None); dv/=dv.sum(); beliefs.append((pms,dv))
    return choose_dag_from_beliefs(beliefs),pe


def graph_error(mask,true_mask):
    return int((int(mask)^int(true_mask)).bit_count())


def evaluate(rows,model,seed):
    ctl=[]; can=[]; regs=[]; outer=[]; changed=[]; probs=[]; labels=[]; hc=hx=0; err=use=0
    for r in rows:
        base_action=posterior_action(np.asarray(r['p0'],float),r)
        control_action=posterior_action(np.asarray(r['ps30'],float),r)
        cand_action,pe=candidate_action(r,model)
        be=graph_error(base_action,r['true_mask']); ce=graph_error(control_action,r['true_mask']); xe=graph_error(cand_action,r['true_mask']); op=bool(r['outer_promote'])
        c=ce if op else be; x=xe if op else be
        ctl.append(float(c)); can.append(float(x)); regs.append(r['regime']); outer.append(op); changed.append(bool(op and cand_action!=control_action)); probs.extend(pe.tolist()); labels.extend([bool(n['anchor_rank_error']) for n in r['nodes']])
        hc += int(op and ce-be>=2); hx += int(op and xe-be>=2)
        for n in r['nodes']:
            if n['anchor_rank_error']:
                err += 1; use += int(n['competitor_better_than_selected'])
    ctl=np.asarray(ctl,float); can=np.asarray(can,float); diff=can-ctl; outer=np.asarray(outer,bool); labels=np.asarray(labels,bool); probs=np.asarray(probs,float); changed=np.asarray(changed,bool)
    prev=float(model['train_error_prevalence']); auc=s60.auc(labels,probs); bri=float(np.mean((probs-labels.astype(float))**2)); const=float(np.mean((prev-labels.astype(float))**2)); by={}
    for rg in REGIMES:
        i=np.asarray([z==rg for z in regs],bool)
        by[rg]={'n':int(i.sum()),'coverage':float(np.mean(outer[i])),'control_mean_action_edge_error':float(np.mean(ctl[i])),'candidate_mean_action_edge_error':float(np.mean(can[i])),'paired_mean_action_edge_difference':float(np.mean(diff[i])),'action_change_fraction':float(np.mean(changed[i]))}
    return {'coverage':float(np.mean(outer)),'control_mean_action_edge_error':float(np.mean(ctl)),'candidate_mean_action_edge_error':float(np.mean(can)),'paired_mean_action_edge_difference':float(np.mean(diff)),'bootstrap95_paired_action_edge_difference':s61.boot(diff,seed=seed),'action_change_fraction':float(np.mean(changed)),'control_large_action_harms':int(hc),'candidate_large_action_harms':int(hx),'error_localization_auc':auc,'error_localization_brier':bri,'constant_prevalence_brier':const,'competitor_useful_fraction_on_error_nodes':float(use/max(1,err)),'posterior_calibration_changed':False,'by_regime':by,'mechanics_ok':mechanics(rows,len(rows)//2)}


def qualifies(e,val=False,conf=False):
    lin=e['by_regime']['linear']; het=e['by_regime']['heteroskedastic']; ok=(e['mechanics_ok'] and e['error_localization_auc'] is not None and e['error_localization_auc']>=.60 and e['error_localization_brier']<=e['constant_prevalence_brier'] and e['competitor_useful_fraction_on_error_nodes']>.50 and .02<=e['action_change_fraction']<=.70 and e['paired_mean_action_edge_difference']<=.03 and het['paired_mean_action_edge_difference']<=-.08 and lin['paired_mean_action_edge_difference']<=.08 and e['candidate_large_action_harms']<=e['control_large_action_harms']+1)
    if val: ok=ok and e['paired_mean_action_edge_difference']<=0 and het['paired_mean_action_edge_difference']<=-.04 and e['candidate_large_action_harms']<=e['control_large_action_harms']
    if conf: ok=ok and e['bootstrap95_paired_action_edge_difference'][1]<0 and het['paired_mean_action_edge_difference']<-.08 and e['candidate_large_action_harms']<=e['control_large_action_harms']
    return bool(ok)


def failclass(e):
    if e.get('error_localization_auc') is None or e['error_localization_auc']<.60 or e['competitor_useful_fraction_on_error_nodes']<=.50: return 'FALSIFIED_EVIDENCE_TRANSFER'
    return 'FALSIFIED_ACTION_GEOMETRY'


if __name__=='__main__':
    me=generate(98001,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(98101,64); model=train_model(tr); ev=evaluate(tr,model,26565); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']=failclass(ev)+'_AT_TRAINING'
        else:
            va=generate(98501,32); vv=evaluate(va,model,26566); out['validation']=vv
            if not qualifies(vv,True): out['disposition']=failclass(vv)+'_ON_VALIDATION'
            else:
                co=generate(98801,64); cv=evaluate(co,model,26567); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,True,True) else failclass(cv)+'_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))