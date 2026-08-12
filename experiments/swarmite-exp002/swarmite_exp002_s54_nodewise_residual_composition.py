import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s49_hetero_likelihood as s49
import swarmite_exp002_s50_world_model_mixture as s50
import swarmite_exp002_s51_residual_diagnostic as s51

REGIMES=('linear','heteroskedastic')
FOLDS=5
RIDGE=5.0
GAIN_SCALE=0.25
NODE_FEATURE_NAMES=['logvar','absfit_absres_corr','logvar_slope','hi_lo_var_ratio','tail_frac','mean_absz','bin_var_dispersion','target_interventions','n_residual']


def safe_corr(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<4 or np.std(x)<1e-10 or np.std(y)<1e-10: return 0.0
    return float(np.corrcoef(x,y)[0,1])


def node_residual_features(data,targets):
    n=len(data); all_idx=list(range(n)); bynode={v:{'pred':[],'res':[]} for v in range(b.N)}
    for fold in range(FOLDS):
        te=[i for i in all_idx if i%FOLDS==fold]; tr=[i for i in all_idx if i%FOLDS!=fold]
        for v in range(b.N):
            cand=[]
            for pm in range(1<<b.N):
                if pm>>v&1: continue
                sc,cols,mu=s50.fit_mean(data,targets,v,pm,tr); cand.append((sc,cols,mu))
            _,cols,mu=max(cand,key=lambda z:z[0])
            tev=[i for i in te if targets[i]!=v]
            if not tev: continue
            X=data[tev][:,cols] if cols else np.empty((len(tev),0)); X=np.column_stack([np.ones(len(tev)),X])
            pred=X@mu; res=data[tev,v]-pred
            bynode[v]['pred'].extend(pred.tolist()); bynode[v]['res'].extend(res.tolist())
    out=[]; ok=True
    for v in range(b.N):
        pred=np.asarray(bynode[v]['pred'],float); res=np.asarray(bynode[v]['res'],float)
        if len(res)<10:
            ok=False; out.append([0.0]*8+[float(len(res))]); continue
        var=max(float(np.mean(res*res)),1e-8); sd=math.sqrt(var); af=np.log1p(np.abs(pred)); ar=np.abs(res)
        corr=safe_corr(af,ar)
        Z=np.column_stack([np.ones(len(res)),af]); y=np.log(res*res+0.05)
        coef=np.linalg.solve(Z.T@Z+np.eye(2),Z.T@y); slope=float(coef[1])
        q1,q3=np.quantile(af,[.25,.75]); lo=res[af<=q1]; hi=res[af>=q3]
        vlo=max(float(np.mean(lo*lo)) if len(lo) else var,1e-8); vhi=max(float(np.mean(hi*hi)) if len(hi) else var,1e-8)
        ratio=float(math.log(vhi/vlo)); z=res/sd; tail=float(np.mean(np.abs(z)>2.0)); maz=float(np.mean(np.abs(z)))
        qs=np.quantile(af,[0,.25,.5,.75,1.0]); vv=[]
        for j in range(4):
            m=(af>=qs[j]) & ((af<=qs[j+1]) if j==3 else (af<qs[j+1]))
            if m.sum()>=3: vv.append(max(float(np.mean(res[m]**2)),1e-8))
        disp=float(np.std(np.log(vv))) if len(vv)>=2 else 0.0
        intervention_count=sum(t==v for t in targets)
        f=[math.log(var),corr,slope,ratio,tail,maz,disp,float(intervention_count),float(len(res))]
        ok=ok and bool(np.all(np.isfinite(f))); out.append(f)
    return out,ok


def incoming_edge_error(marg,true_mask,v):
    ans=0.0
    for k,(u,t) in enumerate(b.EDGES):
        if t!=v: continue
        truth=(true_mask>>k)&1; ans += (1-marg[k]) if truth else marg[k]
    return float(ans)


def compose_posterior(ps30,phet,node_weights):
    m30=b.edge_marginals(ps30); mh=b.edge_marginals(phet); mix=np.empty(len(b.EDGES),float)
    for k,(u,v) in enumerate(b.EDGES): mix[k]=(1-node_weights[v])*m30[k]+node_weights[v]*mh[k]
    mix=np.clip(mix,1e-6,1-1e-6); logp=np.zeros(len(b.dags),float)
    for k in range(len(b.EDGES)):
        present=((b.dags>>k)&1).astype(bool); logp += np.where(present,np.log(mix[k]),np.log1p(-mix[k]))
    logp-=logp.max(); p=np.exp(logp); p/=p.sum(); return p


def world_base(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s49.s30_posterior(data,targets,p0); phet,okh=s49.hetero_posterior(data,targets)
    feats,okf=node_residual_features(data,targets)
    m30=b.edge_marginals(ps30); mh=b.edge_marginals(phet)
    node_gain=[]; node_win=[]
    for v in range(b.N):
        e30=incoming_edge_error(m30,w.dag_mask,v); eh=incoming_edge_error(mh,w.dag_mask,v); g=e30-eh
        node_gain.append(float(g)); node_win.append(int(g>0))
    bm=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask)
    base=s48.world_row(external_seed); amodel,rule=s48.load_anchor(); pred=s46.predict([base],amodel)[0]
    promote=bool(pred['pred_edge_delta']<=rule['edge_cut'] and pred['pred_harm_prob']<=rule['harm_cut'])
    return {'external_seed':external_seed,'regime':reg,'true_mask':int(w.dag_mask),'spend':base['spend'],'trace_identical':base['trace_identical'],'finite':base['finite'],'features':feats,'node_gain':node_gain,'node_win':node_win,'p0':p0.tolist(),'ps30':ps30.tolist(),'phet':phet.tolist(),'baseline_edge_error':float(bm['edge_error']),'baseline_brier':float(bm['brier']),'s30_edge_delta_vs_baseline':float(sm['edge_error']-bm['edge_error']),'s30_brier_delta_vs_baseline':float(sm['brier']-bm['brier']),'outer_promote':promote,'mechanics_ok':bool(ok30 and okh and okf and np.isfinite(ps30).all() and np.isfinite(phet).all() and abs(ps30.sum()-1)<1e-8 and abs(phet.sum()-1)<1e-8)}


def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_base(s) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] and len(r['features'])==b.N for r in rows)


def node_design(rows,mean=None,std=None):
    Z=np.asarray([r['features'][v] for r in rows for v in range(b.N)],float)
    if mean is None: mean=Z.mean(0)
    if std is None: std=Z.std(0); std=np.where(std<1e-8,1.0,std)
    X=(Z-mean)/std; return np.column_stack([np.ones(len(X)),X]),np.asarray(mean),np.asarray(std)


def fit_ridge(X,y,lam=RIDGE):
    pen=np.diag([1e-8]+[lam]*(X.shape[1]-1)); return np.linalg.solve(X.T@X+pen,X.T@np.asarray(y,float))


def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-30,30)))


def fit_logistic(X,y,lam=RIDGE):
    y=np.asarray(y,float); beta=np.zeros(X.shape[1]); prev=(y.sum()+.5)/(len(y)+1.0); beta[0]=math.log(prev/(1-prev)); pen=np.diag([1e-8]+[lam]*(X.shape[1]-1))
    for _ in range(60):
        eta=X@beta; p=np.clip(sigmoid(eta),1e-6,1-1e-6); ww=p*(1-p); z=eta+(y-p)/ww
        nb=np.linalg.solve(X.T@(ww[:,None]*X)+pen,X.T@(ww*z))
        if np.max(np.abs(nb-beta))<1e-8: beta=nb; break
        beta=nb
    return beta,float(prev)


def train_model(rows):
    X,mean,std=node_design(rows); gain=np.asarray([g for r in rows for g in r['node_gain']],float); win=np.asarray([w for r in rows for w in r['node_win']],float)
    return {'feature_names':NODE_FEATURE_NAMES,'mean':mean.tolist(),'std':std.tolist(),'gain_beta':fit_ridge(X,gain).tolist(),'win_beta':fit_logistic(X,win)[0].tolist(),'train_win_prevalence':float((win.sum()+.5)/(len(win)+1.0)),'gain_scale':GAIN_SCALE,'ridge_lambda':RIDGE}


def predict_weights(row,model):
    Z=np.asarray(row['features'],float); mean=np.asarray(model['mean']); std=np.asarray(model['std']); X=np.column_stack([np.ones(len(Z)),(Z-mean)/std])
    pg=X@np.asarray(model['gain_beta']); pw=sigmoid(X@np.asarray(model['win_beta'])); w=pw*np.clip(pg/float(model['gain_scale']),0,1)
    return pw,pg,w


def boot(x,reps=10000,seed=25454):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def evaluate(rows,model,seed):
    control=[]; cand=[]; control_b=[]; cand_b=[]; weights=[]; node_prob=[]; node_win=[]; outer=[]; regs=[]; harms_c=harms_x=0
    for r in rows:
        ps=np.asarray(r['ps30']); ph=np.asarray(r['phet']); pwin,pg,w=predict_weights(r,model); p54=compose_posterior(ps,ph,w); mm=b.posterior_metrics(p54,r['true_mask'])
        ce=float(mm['edge_error']-r['baseline_edge_error']); cb=float(mm['brier']-r['baseline_brier']); op=bool(r['outer_promote'])
        c0=r['s30_edge_delta_vs_baseline'] if op else 0.0; x0=ce if op else 0.0; c0b=r['s30_brier_delta_vs_baseline'] if op else 0.0; x0b=cb if op else 0.0
        control.append(c0); cand.append(x0); control_b.append(c0b); cand_b.append(x0b); weights.extend(w.tolist()); node_prob.extend(pwin.tolist()); node_win.extend(r['node_win']); outer.append(op); regs.append(r['regime'])
        harms_c += int(op and r['s30_edge_delta_vs_baseline']>.50); harms_x += int(op and ce>.50)
    control=np.asarray(control); cand=np.asarray(cand); diff=cand-control; weights=np.asarray(weights); node_prob=np.asarray(node_prob); node_win=np.asarray(node_win,bool); outer=np.asarray(outer,bool)
    prev=float(model['train_win_prevalence']); brier=float(np.mean((node_prob-node_win.astype(float))**2)); const=float(np.mean((prev-node_win.astype(float))**2)); auc=s51.auc(node_prob,node_win)
    by={}
    for rg in REGIMES:
        idx=np.asarray([x==rg for x in regs],bool); wi=np.concatenate([predict_weights(rows[i],model)[2] for i in range(len(rows)) if idx[i]])
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),'paired_mean_edge_difference':float(np.mean(diff[idx])),'mean_node_specialist_mass':float(np.mean(wi))}
    return {'coverage':float(np.mean(outer)),'mean_node_specialist_mass':float(np.mean(weights)),'control_hybrid_mean_edge_delta':float(np.mean(control)),'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':boot(diff,seed=seed),'control_hybrid_mean_brier_delta':float(np.mean(control_b)),'candidate_hybrid_mean_brier_delta':float(np.mean(cand_b)),'control_promoted_large_harms':int(harms_c),'candidate_promoted_large_harms':int(harms_x),'node_specialist_win_auc':auc,'node_specialist_win_brier':brier,'constant_prevalence_brier':const,'by_regime':by,'mechanics_ok':mechanics(rows,int(len(rows)/2))}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']; auc=ev['node_specialist_win_auc']
    ok=(ev['mechanics_ok'] and .005<=ev['mean_node_specialist_mass']<=.20 and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.01 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.02 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.02 and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and ev['candidate_hybrid_mean_brier_delta']<=.005 and auc is not None and auc>=.60 and ev['node_specialist_win_brier']<=ev['constant_prevalence_brier'])
    if validation or confirmation: ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.01
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.02
    return bool(ok)

if __name__=='__main__':
    me=generate(82501,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(82601,64); model=train_model(tr); ev=evaluate(tr,model,25455); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']='FALSIFIED_AT_TRAINING'
        else:
            va=generate(83001,32); vv=evaluate(va,model,25456); out['validation']=vv
            if not qualifies(vv,validation=True): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(83501,64); cv=evaluate(co,model,25457); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,validation=True,confirmation=True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
