import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s59_residual_state_evidence_decomposition as s59
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60

REGIMES=('linear','heteroskedastic')
RIDGE=5.0
MAX_TILT=0.75
FEATURES=s60.FEATURES
MODEL_FEATURE_NAMES=list(FEATURES)+['log_competitor_advantage','anchor_competitor_score_gap']


def predictive_detail(data,targets,fs,v):
    targets=np.asarray(targets,dtype=object)
    keep=np.asarray([not ((t==v) if isinstance(t,(int,np.integer)) else False) for t in targets],bool)
    idx=np.where(keep)[0]; y=np.asarray(data[:,v],float)
    labs=[]
    for i in idx:
        lab=s60.key_lab(targets[i])
        if lab not in labs: labs.append(lab)
    pms=s60.legal_pms(v); sel=max(pms,key=lambda pm:float(fs[v,pm]))
    by_pm={pm:[] for pm in pms}; selected_losses=[]; disagree=[]; comp_adv=[]
    for lab in labs:
        te=np.asarray([i for i in idx if s60.key_lab(targets[i])==lab],int)
        tr=np.asarray([i for i in idx if s60.key_lab(targets[i])!=lab],int)
        if len(te)<1 or len(tr)<8: continue
        trm=np.zeros(len(data),bool); trm[tr]=True
        tem=np.zeros(len(data),bool); tem[te]=True
        losses={}
        for pm in pms:
            z=s60.fit_loss(data,y,trm,tem,pm,v)
            if math.isfinite(z): losses[pm]=z; by_pm[pm].append(z)
        if sel not in losses or len(losses)<2: continue
        sl=losses[sel]; others=[x for pm,x in losses.items() if pm!=sel]
        bo=min(others) if others else sl
        selected_losses.append(sl); disagree.append(float(bo<sl)); comp_adv.append(max(0.0,sl-bo))
    means={pm:float(np.mean(vals)) for pm,vals in by_pm.items() if vals}
    candidates=[(loss,pm) for pm,loss in means.items() if pm!=sel]
    comp=min(candidates)[1] if candidates else sel
    if not selected_losses:
        selected_losses=[0.0]; disagree=[0.0]; comp_adv=[0.0]
    a=np.asarray(selected_losses,float)
    feat={
      'selected_cv_mean_loss':float(np.mean(a)),
      'selected_cv_std_loss':float(np.std(a)),
      'selected_cv_worst_loss':float(np.max(a)),
      'cv_rank_volatility':float(np.mean(disagree)),
      'cv_competitor_advantage':float(np.mean(comp_adv)),
      'state_loss_range':float(np.max(a)-np.min(a)),
      'n_cv_states':int(len(a)),
    }
    return int(sel),int(comp),feat


def hamming(a,c): return int((int(a)^int(c)).bit_count())


def dag_parent_mask(dagmask,v):
    pm=0
    for k,(u,t) in enumerate(b.EDGES):
        if t==v and ((int(dagmask)>>k)&1): pm |= (1<<u)
    return pm


def correction_features(feat,gap):
    vals=[float(feat[k]) for k in FEATURES]
    vals += [math.log1p(max(0.0,float(feat['cv_competitor_advantage']))),float(gap)]
    return vals


def world_base(external_seed):
    base=s54.world_base(external_seed)
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,_=b.build_family_models(data,targets)
    nodes=[]
    for v in range(b.N):
        truth=s59.true_parent_mask(base['true_mask'],v)
        margin=s59.margin(fs,v,truth)
        sel,comp,feat=predictive_detail(data,targets,fs,v)
        gap=float(fs[v,sel]-fs[v,comp]) if comp!=sel else 0.0
        row={'node':int(v),'selected_parent_mask':sel,'competitor_parent_mask':comp,
             'anchor_rank_error':bool(margin<0),'anchor_margin':float(margin),
             'competitor_better_than_selected':bool(hamming(comp,truth)<hamming(sel,truth)),
             'features':correction_features(feat,gap),'raw_predictive':feat}
        nodes.append(row)
    base=dict(base); base['nodes']=nodes
    base['mechanics_ok']=bool(base['mechanics_ok'] and all(np.all(np.isfinite(n['features'])) for n in nodes))
    return base


def generate(start,n_each):
    seeds=s60.selected(start,n_each)
    return [world_base(s) for s in seeds]


def mechanics(rows,n_each):
    return (len(rows)==2*n_each and all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES)
            and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok']
                    and len(r['nodes'])==b.N for r in rows))


def node_matrix(rows,mean=None,std=None):
    Z=np.asarray([n['features'] for r in rows for n in r['nodes']],float)
    if mean is None: mean=Z.mean(0)
    if std is None:
        std=Z.std(0); std=np.where(std<1e-8,1.0,std)
    X=(Z-np.asarray(mean))/np.asarray(std)
    return np.column_stack([np.ones(len(X)),X]),np.asarray(mean),np.asarray(std)


def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-30,30)))


def fit_logistic(X,y,lam=RIDGE):
    y=np.asarray(y,float); beta=np.zeros(X.shape[1]); prev=float((y.sum()+.5)/(len(y)+1.0)); beta[0]=math.log(prev/(1-prev))
    pen=np.diag([1e-8]+[lam]*(X.shape[1]-1))
    for _ in range(80):
        eta=X@beta; p=np.clip(sigmoid(eta),1e-6,1-1e-6); ww=p*(1-p); z=eta+(y-p)/ww
        nb=np.linalg.solve(X.T@(ww[:,None]*X)+pen,X.T@(ww*z))
        if np.max(np.abs(nb-beta))<1e-9: beta=nb; break
        beta=nb
    return beta,prev


def train_model(rows):
    X,mean,std=node_matrix(rows); y=np.asarray([n['anchor_rank_error'] for r in rows for n in r['nodes']],float)
    beta,prev=fit_logistic(X,y)
    return {'feature_names':MODEL_FEATURE_NAMES,'mean':mean.tolist(),'std':std.tolist(),'beta':beta.tolist(),
            'train_error_prevalence':float(prev),'ridge_lambda':RIDGE,'max_tilt':MAX_TILT}


def node_predictions(row,model):
    Z=np.asarray([n['features'] for n in row['nodes']],float); mean=np.asarray(model['mean']); std=np.asarray(model['std'])
    X=np.column_stack([np.ones(len(Z)),(Z-mean)/std]); p=sigmoid(X@np.asarray(model['beta']))
    prev=float(model['train_error_prevalence']); activation=np.clip((p-prev)/max(1.0-prev,1e-6),0.0,1.0)
    adv=np.asarray([max(0.0,n['raw_predictive']['cv_competitor_advantage']) for n in row['nodes']],float)
    reliability=np.clip(np.log1p(adv)/math.log(3.0),0.0,1.0)
    lam=float(model['max_tilt'])*activation*reliability
    for i,n in enumerate(row['nodes']):
        if n['competitor_parent_mask']==n['selected_parent_mask']: lam[i]=0.0
    return p,lam


def corrected_posterior(row,model):
    ps=np.asarray(row['ps30'],float); pnode,lam=node_predictions(row,model); logp=np.log(np.clip(ps,1e-300,None))
    for j,dagmask in enumerate(b.dags):
        add=0.0
        for v,n in enumerate(row['nodes']):
            if lam[v]<=0: continue
            pm=dag_parent_mask(dagmask,v)
            if pm==n['competitor_parent_mask']: add += lam[v]
            elif pm==n['selected_parent_mask']: add -= lam[v]
        logp[j]+=add
    logp-=np.max(logp); p=np.exp(logp); p/=p.sum()
    return p,pnode,lam


def boot(x,reps=10000,seed=26161):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def evaluate(rows,model,seed):
    control=[]; cand=[]; control_b=[]; cand_b=[]; regs=[]; probs=[]; labels=[]; lams=[]; outer=[]
    harms_c=harms_x=0; err_nodes=0; useful_on_err=0
    for r in rows:
        p61,pnode,lam=corrected_posterior(r,model); mm=b.posterior_metrics(p61,r['true_mask'])
        ce=float(mm['edge_error']-r['baseline_edge_error']); cb=float(mm['brier']-r['baseline_brier']); op=bool(r['outer_promote'])
        c0=float(r['s30_edge_delta_vs_baseline']) if op else 0.0; x0=ce if op else 0.0
        c0b=float(r['s30_brier_delta_vs_baseline']) if op else 0.0; x0b=cb if op else 0.0
        control.append(c0); cand.append(x0); control_b.append(c0b); cand_b.append(x0b); regs.append(r['regime']); outer.append(op)
        probs.extend(pnode.tolist()); labels.extend([n['anchor_rank_error'] for n in r['nodes']]); lams.extend(lam.tolist())
        harms_c += int(op and r['s30_edge_delta_vs_baseline']>.50); harms_x += int(op and ce>.50)
        for n in r['nodes']:
            if n['anchor_rank_error']:
                err_nodes+=1; useful_on_err += int(n['competitor_better_than_selected'])
    control=np.asarray(control); cand=np.asarray(cand); diff=cand-control; probs=np.asarray(probs); labels=np.asarray(labels,bool); lams=np.asarray(lams); outer=np.asarray(outer,bool)
    prev=float(model['train_error_prevalence']); auc=s60.auc(labels,probs); bri=float(np.mean((probs-labels.astype(float))**2)); const=float(np.mean((prev-labels.astype(float))**2))
    by={}
    for rg in REGIMES:
        idx=np.asarray([x==rg for x in regs],bool)
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),
                'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),
                'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),
                'paired_mean_edge_difference':float(np.mean(diff[idx]))}
    return {'coverage':float(np.mean(outer)),'mean_local_tilt':float(np.mean(lams)),
            'nonzero_correction_fraction':float(np.mean(lams>1e-10)),
            'control_hybrid_mean_edge_delta':float(np.mean(control)),
            'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),
            'paired_mean_edge_difference':float(np.mean(diff)),
            'bootstrap95_paired_edge_difference':boot(diff,seed=seed),
            'control_hybrid_mean_brier_delta':float(np.mean(control_b)),
            'candidate_hybrid_mean_brier_delta':float(np.mean(cand_b)),
            'control_promoted_large_harms':int(harms_c),'candidate_promoted_large_harms':int(harms_x),
            'error_localization_auc':auc,'error_localization_brier':bri,'constant_prevalence_brier':const,
            'n_anchor_error_nodes':int(err_nodes),'competitor_useful_fraction_on_error_nodes':float(useful_on_err/max(1,err_nodes)),
            'by_regime':by,'mechanics_ok':mechanics(rows,int(len(rows)/2))}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']; auc=ev['error_localization_auc']
    ok=(ev['mechanics_ok'] and .02<=ev['nonzero_correction_fraction']<=.60
        and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.005
        and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.01
        and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.015
        and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms']
        and ev['candidate_hybrid_mean_brier_delta']<=ev['control_hybrid_mean_brier_delta']+.005
        and auc is not None and auc>=.60 and ev['error_localization_brier']<=ev['constant_prevalence_brier']
        and ev['competitor_useful_fraction_on_error_nodes']>.50)
    if validation: ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.005
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.01
    return bool(ok)


def failure_class(ev):
    if ev.get('error_localization_auc') is None or ev['error_localization_auc']<.60 or ev['competitor_useful_fraction_on_error_nodes']<=.50:
        return 'FALSIFIED_TARGETING'
    return 'FALSIFIED_CORRECTION_GEOMETRY'


if __name__=='__main__':
    me=generate(94101,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(94201,64); model=train_model(tr); ev=evaluate(tr,model,26162); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']=failure_class(ev)+'_AT_TRAINING'
        else:
            va=generate(94601,32); vv=evaluate(va,model,26163); out['validation']=vv
            if not qualifies(vv,validation=True): out['disposition']=failure_class(vv)+'_ON_VALIDATION'
            else:
                co=generate(94901,64); cv=evaluate(co,model,26164); out['confirmation']=cv
                out['disposition']='SUPPORTED' if qualifies(cv,validation=True,confirmation=True) else failure_class(cv)+'_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
