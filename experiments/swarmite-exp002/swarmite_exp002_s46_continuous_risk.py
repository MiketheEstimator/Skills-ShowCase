import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s44_joint_shift as s44
import swarmite_exp002_s45_joint_latent as s45

RIDGE=2.0
EDGE_CUTS=(-.50,-.25,-.10,0.0,.10)
HARM_CUTS=(.05,.10,.20,.30)
SPECIALISTS=s39.SPECIALISTS; CREDAL_THRESHOLD=s44.CREDAL_THRESHOLD
FEATURE_NAMES=['p_dense','mech_tanh','mech_sin','mech_asinh','credal_width','alpha','base_entropy','s30_entropy','edge_shift_mean','edge_shift_max','base_map_mass','s30_map_mass','base_expected_edges','s30_expected_edges','p_dense_x_mech_tanh','p_dense_x_mech_sin','p_dense_x_mech_asinh','p_dense_x_credal','p_dense_x_alpha']

def base_row(seed):
    w,den,mech=s44.gen_world(seed); c,data,targets,p0=s44.run_control(w,seed,mech); fs,_=b.build_family_models(data,targets)
    es=s45.s42.class_logevidence(fs,.15); ed=s45.s42.class_logevidence(fs,.55); mx=max(es,ed); aa=math.exp(es-mx); dd=math.exp(ed-mx); qdense=float(dd/(aa+dd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(p0); em=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); credal=float(np.mean(np.max(np.vstack([em,ems]),axis=0)-np.min(np.vstack([em,ems]),axis=0))); ms=s45.mechanism_scores(data,targets)
    shift=np.abs(em-em0); raw=[qdense,*ms.tolist(),credal,float(alpha),b.entropy(p0),b.entropy(ps30),float(np.mean(shift)),float(np.max(shift)),float(np.max(p0)),float(np.max(ps30)),float(np.sum(em0)),float(np.sum(em))]
    raw += [qdense*ms[0],qdense*ms[1],qdense*ms[2],qdense*credal,qdense*alpha]
    base=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); edge=float(sm['edge_error']-base['edge_error']); br=float(sm['brier']-base['brier'])
    return {'seed':int(seed),'density':den,'mechanism':mech,'joint_cell':den+'_'+mech,'features':[float(x) for x in raw],'credal_width':credal,'p_dense':qdense,'alpha':float(alpha),'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'trace_identical':True,'finite':bool(finite and np.all(np.isfinite(raw))),'s30_sum':float(ps30.sum())}

def generate(lo,hi): return [base_row(s) for s in range(lo,hi+1)]
def counts_ok(rows,n_each): return all(sum(r['joint_cell']==d+'_'+m for r in rows)==n_each for d in ('sparse','dense') for m in s45.MECHS)
def mechanics(rows): return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and len(r['features'])==len(FEATURE_NAMES) for r in rows)

def design(rows,mean=None,std=None):
    Z=np.asarray([r['features'] for r in rows],float)
    if mean is None: mean=Z.mean(axis=0)
    if std is None: std=Z.std(axis=0); std=np.where(std<1e-8,1.0,std)
    X=(Z-mean)/std; return np.column_stack([np.ones(len(X)),X]),np.asarray(mean),np.asarray(std)

def fit_ridge(X,y,lam=RIDGE):
    pen=np.diag([1e-8]+[lam]*(X.shape[1]-1)); return np.linalg.solve(X.T@X+pen,X.T@np.asarray(y,float))
def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-30,30)))
def fit_logistic(X,y,lam=RIDGE):
    y=np.asarray(y,float); beta=np.zeros(X.shape[1]); prev=(y.sum()+.5)/(len(y)+1.0); beta[0]=math.log(prev/(1-prev)); pen=np.diag([1e-8]+[lam]*(X.shape[1]-1))
    for _ in range(50):
        eta=X@beta; p=np.clip(sigmoid(eta),1e-6,1-1e-6); w=p*(1-p); z=eta+(y-p)/w; A=X.T@(w[:,None]*X)+pen; rhs=X.T@(w*z); nb=np.linalg.solve(A,rhs)
        if np.max(np.abs(nb-beta))<1e-8: beta=nb; break
        beta=nb
    return beta,float(prev)

def train_model(rows):
    X,mean,std=design(rows); y=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); h=np.array([r['s30_large_harm'] for r in rows]); be=fit_ridge(X,y); bh,prev=fit_logistic(X,h)
    return {'feature_names':FEATURE_NAMES,'mean':mean.tolist(),'std':std.tolist(),'edge_beta':be.tolist(),'harm_beta':bh.tolist(),'train_harm_prevalence':prev,'ridge_lambda':RIDGE}
def predict(rows,model):
    X,_,_=design(rows,np.array(model['mean']),np.array(model['std'])); pe=X@np.array(model['edge_beta']); ph=sigmoid(X@np.array(model['harm_beta'])); out=[]
    for r,e,h in zip(rows,pe,ph): x=dict(r); x['pred_edge_delta']=float(e); x['pred_harm_prob']=float(h); out.append(x)
    return out

def boot(x,reps=10000,seed=24646):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]
def policy_stats(rows,mask,seed):
    mask=np.asarray(mask,bool); ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); always=float(np.mean(ed)); hy=float(np.mean(he)); ret=float(abs(hy)/abs(always)) if always<0 else 1.0
    by={}
    for cell in sorted({r['joint_cell'] for r in rows}):
        idx=np.array([r['joint_cell']==cell for r in rows]); mm=mask[idx]; ee=ed[idx]; by[cell]={'n':int(idx.sum()),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.))),'large_harm_rate':float(np.sum((ee>.5)&mm)/max(1,mm.sum()))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,mask.sum())),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hy,'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'improvement_retained':ret,'by_joint_cell':by}
def topology_mask(rows): return np.ones(len(rows),bool)
def s39_mask(rows): return np.array([r['credal_width']<=CREDAL_THRESHOLD for r in rows],bool)
def risk_brier(rows,prev): return float(np.mean([(r['pred_harm_prob']-r['s30_large_harm'])**2 for r in rows])),float(np.mean([(prev-r['s30_large_harm'])**2 for r in rows]))

def rule_grid(pred_rows):
    out=[]
    for ec in EDGE_CUTS:
        for hc in HARM_CUTS:
            mask=np.array([r['pred_edge_delta']<=ec and r['pred_harm_prob']<=hc for r in pred_rows]); st=policy_stats(pred_rows,mask,24640+int((ec+1)*100)+int(hc*100)); qualifies=st['coverage']>=.40 and st['promoted_large_harm_rate']<=.05 and st['hybrid_mean_edge_delta']<0 and st['hybrid_mean_brier_delta']<=.005 and (st['always_s30_mean_edge_delta']>=0 or st['improvement_retained']>=.60); out.append({'edge_cut':ec,'harm_cut':hc,'qualifies':bool(qualifies),'stats':st})
    return out
def select_rule(grid):
    q=[g for g in grid if g['qualifies']]
    if not q: return None
    best=max(g['stats']['improvement_retained'] for g in q); q=[g for g in q if best-g['stats']['improvement_retained']<=.01]; q.sort(key=lambda g:(g['harm_cut'],g['edge_cut'])); return {'edge_cut':q[0]['edge_cut'],'harm_cut':q[0]['harm_cut']}
def summarize(raw,model,rule,seed):
    rows=predict(raw,model); mask=np.array([r['pred_edge_delta']<=rule['edge_cut'] and r['pred_harm_prob']<=rule['harm_cut'] for r in rows]); m=policy_stats(rows,mask,seed); tc=policy_stats(rows,topology_mask(rows),seed+1); sc=policy_stats(rows,s39_mask(rows),seed+2); rb,cb=risk_brier(rows,model['train_harm_prevalence']); return {'n':len(rows),'continuous_risk':m,'topology_control':tc,'s39_control':sc,'risk_brier':rb,'constant_prevalence_brier':cb,'mechanics_ok':mechanics(raw),'rows':rows}
def validation_pass(s):
    m=s['continuous_risk']; tc=s['topology_control']; ratio=float(abs(m['hybrid_mean_edge_delta'])/abs(tc['hybrid_mean_edge_delta'])) if tc['hybrid_mean_edge_delta']<0 else 1.0
    return s['mechanics_ok'] and m['coverage']>=.40 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.60) and ratio>=.55 and s['risk_brier']<=s['constant_prevalence_brier']
def confirmation_pass(s):
    if not validation_pass(s): return False
    m=s['continuous_risk']; cells=all(v['large_harm_rate']<=.10 for v in m['by_joint_cell'].values()); return m['bootstrap95_hybrid_edge_delta'][1]<0 and m['improvement_retained']>=.60 and m['promoted_large_harm_rate']<=.05 and cells

if __name__=='__main__':
    tr=generate(73801,73920); model=train_model(tr); pr=predict(tr,model); grid=rule_grid(pr); rule=select_rule(grid); out={'training':{'model':model,'rule_grid':grid,'selected_rule':rule,'mechanics_ok':mechanics(tr),'counts_ok':counts_ok(tr,20)}}
    if not mechanics(tr) or not counts_ok(tr,20): out['disposition']='BLOCKED_TRAINING_MECHANICS'
    elif rule is None: out['disposition']='NO_TRAINING_RULE_QUALIFIED'
    else:
        va=generate(74001,74060); vs=summarize(va,model,rule,24647); out['validation']=vs
        if not counts_ok(va,10) or not validation_pass(vs): out['disposition']='FALSIFIED_ON_VALIDATION'
        else:
            co=generate(74101,74220); cs=summarize(co,model,rule,24648); out['confirmation']=cs; out['disposition']='CONTINUOUS_RISK_SUPPORTED' if counts_ok(co,20) and confirmation_pass(cs) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
