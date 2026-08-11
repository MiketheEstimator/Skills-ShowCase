import json, math, numpy as np
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
EPS=0.05
P_CUTS=(0.55,0.65,0.75,0.85)
GAIN_CUTS=(0.00,0.05,0.10)

RESIDUAL_FEATURE_NAMES=[
    'mean_logvar','std_logvar','max_logvar',
    'mean_absfit_absres_corr','std_absfit_absres_corr','max_absfit_absres_corr',
    'mean_logvar_slope','std_logvar_slope','max_logvar_slope',
    'mean_hi_lo_var_ratio','std_hi_lo_var_ratio','max_hi_lo_var_ratio',
    'mean_tail_frac','max_tail_frac','mean_absz','max_absz',
    'mean_bin_var_dispersion','max_bin_var_dispersion',
    'global_absfit_absres_corr','global_tail_frac','global_absz_mean',
    'd_var','q_het'
]
FEATURE_NAMES=list(s46.FEATURE_NAMES)+RESIDUAL_FEATURE_NAMES


def safe_corr(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<4 or np.std(x)<1e-10 or np.std(y)<1e-10: return 0.0
    return float(np.corrcoef(x,y)[0,1])


def agg(vals):
    v=np.asarray(vals,float)
    if len(v)==0: return (0.0,0.0,0.0)
    return float(np.mean(v)),float(np.std(v)),float(np.max(v))


def residual_state(data,targets):
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
    logvars=[]; corrs=[]; slopes=[]; ratios=[]; tails=[]; abszs=[]; dispersions=[]
    gp=[]; gr=[]
    for v in range(b.N):
        pred=np.asarray(bynode[v]['pred'],float); res=np.asarray(bynode[v]['res'],float)
        if len(res)<10: continue
        gp.extend(pred.tolist()); gr.extend(res.tolist())
        var=max(float(np.mean(res*res)),1e-8); sd=math.sqrt(var); logvars.append(math.log(var))
        af=np.log1p(np.abs(pred)); ar=np.abs(res); corrs.append(safe_corr(af,ar))
        Z=np.column_stack([np.ones(len(res)),af]); y=np.log(res*res+EPS)
        coef=np.linalg.solve(Z.T@Z+np.eye(2),Z.T@y); slopes.append(float(coef[1]))
        q1,q3=np.quantile(af,[.25,.75]); lo=res[af<=q1]; hi=res[af>=q3]
        vlo=max(float(np.mean(lo*lo)) if len(lo) else var,1e-8); vhi=max(float(np.mean(hi*hi)) if len(hi) else var,1e-8)
        ratios.append(float(math.log(vhi/vlo)))
        z=res/sd; tails.append(float(np.mean(np.abs(z)>2.0))); abszs.append(float(np.mean(np.abs(z))))
        qs=np.quantile(af,[0,.25,.5,.75,1.0]); vv=[]
        for j in range(4):
            m=(af>=qs[j]) & ((af<=qs[j+1]) if j==3 else (af<qs[j+1]))
            if m.sum()>=3: vv.append(max(float(np.mean(res[m]**2)),1e-8))
        dispersions.append(float(np.std(np.log(vv))) if len(vv)>=2 else 0.0)
    ml,sl,xl=agg(logvars); mc,sc,xc=agg(corrs); ms,ss,xs=agg(slopes); mr,sr,xr=agg(ratios)
    mt,_,xt=agg(tails); ma,_,xa=agg(abszs); md,_,xd=agg(dispersions)
    gp=np.asarray(gp,float); gr=np.asarray(gr,float)
    gv=max(float(np.mean(gr*gr)),1e-8) if len(gr) else 1.0; gz=gr/math.sqrt(gv) if len(gr) else np.array([0.0])
    gc=safe_corr(np.log1p(np.abs(gp)),np.abs(gr)) if len(gr) else 0.0
    gt=float(np.mean(np.abs(gz)>2.0)); ga=float(np.mean(np.abs(gz)))
    dvar,qhet,nscore,ok=s50.cv_variance_evidence(data,targets)
    feats=[ml,sl,xl,mc,sc,xc,ms,ss,xs,mr,sr,xr,mt,xt,ma,xa,md,xd,gc,gt,ga,float(dvar),float(qhet)]
    return feats,bool(ok and nscore>0 and np.all(np.isfinite(feats)))


def world_row(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s49.s30_posterior(data,targets,p0); phet,okh=s49.hetero_posterior(data,targets)
    bm=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); hm=b.posterior_metrics(phet,w.dag_mask)
    base=s48.world_row(external_seed); rf,okr=residual_state(data,targets)
    model,rule=s48.load_anchor(); pred=s46.predict([base],model)[0]
    promote=bool(pred['pred_edge_delta']<=rule['edge_cut'] and pred['pred_harm_prob']<=rule['harm_cut'])
    gain=float(sm['edge_error']-hm['edge_error'])
    out=dict(base); out.update({
        'latent_features':[float(x) for x in list(base['features'])+rf],
        'baseline_edge_error':float(bm['edge_error']),'baseline_brier':float(bm['brier']),
        's30_edge_error':float(sm['edge_error']),'s30_brier':float(sm['brier']),
        'phet_edge_error':float(hm['edge_error']),'phet_brier':float(hm['brier']),
        's30_edge_delta_vs_baseline':float(sm['edge_error']-bm['edge_error']),
        's30_brier_delta_vs_baseline':float(sm['brier']-bm['brier']),
        'phet_edge_delta_vs_baseline':float(hm['edge_error']-bm['edge_error']),
        'phet_brier_delta_vs_baseline':float(hm['brier']-bm['brier']),
        'specialist_gain_over_s30':gain,'specialist_beats_s30':int(gain>0),
        'outer_promote':promote,'outer_pred_edge_delta':float(pred['pred_edge_delta']),'outer_pred_harm_prob':float(pred['pred_harm_prob']),
        'posterior_mechanics_ok':bool(ok30 and okh and okr and np.isfinite(ps30).all() and np.isfinite(phet).all()),
        's30_sum':float(ps30.sum()),'phet_sum':float(phet.sum())
    })
    return out


def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(
        r['spend']<=15 and r['trace_identical'] and r['finite'] and r['posterior_mechanics_ok'] and
        len(r['latent_features'])==len(FEATURE_NAMES) and abs(r['s30_sum']-1)<1e-8 and abs(r['phet_sum']-1)<1e-8
        for r in rows)


def design(rows,mean=None,std=None):
    Z=np.asarray([r['latent_features'] for r in rows],float)
    if mean is None: mean=Z.mean(axis=0)
    if std is None: std=Z.std(axis=0); std=np.where(std<1e-8,1.0,std)
    X=(Z-mean)/std
    return np.column_stack([np.ones(len(X)),X]),np.asarray(mean),np.asarray(std)


def fit_ridge(X,y,lam=RIDGE):
    pen=np.diag([1e-8]+[lam]*(X.shape[1]-1)); return np.linalg.solve(X.T@X+pen,X.T@np.asarray(y,float))


def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-30,30)))


def fit_logistic(X,y,lam=RIDGE):
    y=np.asarray(y,float); beta=np.zeros(X.shape[1]); prev=(y.sum()+.5)/(len(y)+1.0); beta[0]=math.log(prev/(1-prev)); pen=np.diag([1e-8]+[lam]*(X.shape[1]-1))
    for _ in range(60):
        eta=X@beta; p=np.clip(sigmoid(eta),1e-6,1-1e-6); w=p*(1-p); z=eta+(y-p)/w
        A=X.T@(w[:,None]*X)+pen; rhs=X.T@(w*z); nb=np.linalg.solve(A,rhs)
        if np.max(np.abs(nb-beta))<1e-8: beta=nb; break
        beta=nb
    return beta,float(prev)


def train_model(rows):
    X,mean,std=design(rows); gain=np.array([r['specialist_gain_over_s30'] for r in rows],float); win=np.array([r['specialist_beats_s30'] for r in rows],float)
    bg=fit_ridge(X,gain); bw,prev=fit_logistic(X,win)
    return {'feature_names':FEATURE_NAMES,'mean':mean.tolist(),'std':std.tolist(),'gain_beta':bg.tolist(),'win_beta':bw.tolist(),'train_win_prevalence':prev,'ridge_lambda':RIDGE}


def predict(rows,model):
    X,_,_=design(rows,np.array(model['mean']),np.array(model['std'])); pg=X@np.array(model['gain_beta']); pw=sigmoid(X@np.array(model['win_beta'])); out=[]
    for r,g,p in zip(rows,pg,pw):
        x=dict(r); x['pred_specialist_gain']=float(g); x['pred_specialist_win_prob']=float(p); out.append(x)
    return out


def boot(x,reps=10000,seed=25252):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def evaluate(rows,model,rule,p_cut,g_cut,seed):
    pr=predict(rows,model); outer=np.array([r['outer_promote'] for r in pr],bool)
    use=np.array([outer[i] and r['pred_specialist_win_prob']>=p_cut and r['pred_specialist_gain']>=g_cut for i,r in enumerate(pr)],bool)
    s30e=np.array([r['s30_edge_delta_vs_baseline'] for r in pr],float); phe=np.array([r['phet_edge_delta_vs_baseline'] for r in pr],float)
    s30b=np.array([r['s30_brier_delta_vs_baseline'] for r in pr],float); phb=np.array([r['phet_brier_delta_vs_baseline'] for r in pr],float)
    control=np.where(outer,s30e,0.0); cand=np.where(outer,np.where(use,phe,s30e),0.0)
    cb=np.where(outer,s30b,0.0); xb=np.where(outer,np.where(use,phb,s30b),0.0); diff=cand-control
    win=np.array([r['specialist_beats_s30'] for r in pr],bool); prob=np.array([r['pred_specialist_win_prob'] for r in pr],float)
    harm_c=int(np.sum(outer & (s30e>.50))); harm_x=int(np.sum(outer & (np.where(use,phe,s30e)>.50)))
    by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in pr],bool); om=outer[idx]; um=use[idx]
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(om)),'specialist_use_rate_promoted':float(um.sum()/max(1,om.sum())),'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),'paired_mean_edge_difference':float(np.mean(diff[idx]))}
    auc=s51.auc(prob,win); pb=float(np.mean((prob-win.astype(float))**2)); prev=float(model['train_win_prevalence']); const=float(np.mean((prev-win.astype(float))**2))
    return {'p_cut':p_cut,'gain_cut':g_cut,'coverage':float(np.mean(outer)),'specialist_use_rate_promoted':float(use.sum()/max(1,outer.sum())),'control_hybrid_mean_edge_delta':float(np.mean(control)),'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':boot(diff,seed=seed),'control_hybrid_mean_brier_delta':float(np.mean(cb)),'candidate_hybrid_mean_brier_delta':float(np.mean(xb)),'control_promoted_large_harms':harm_c,'candidate_promoted_large_harms':harm_x,'specialist_selection_precision':float(win[use].mean()) if use.any() else None,'specialist_win_auc':auc,'specialist_win_brier':pb,'constant_prevalence_brier':const,'by_regime':by,'mechanics_ok':mechanics(rows,int(len(rows)/2)),'rows':pr}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']; use=ev['specialist_use_rate_promoted']; prec=ev['specialist_selection_precision']
    lower=.02 if validation or confirmation else .03
    ok=(ev['mechanics_ok'] and lower<=use<=.35 and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.01 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.02 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.02 and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and ev['candidate_hybrid_mean_brier_delta']<=.005 and prec is not None and prec>=.55)
    if validation or confirmation: ok=ok and ev['paired_mean_edge_difference']<=0 and ev['specialist_win_auc'] is not None and ev['specialist_win_auc']>=.60
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.02 and lin['paired_mean_edge_difference']<=.02 and ev['specialist_win_brier']<=ev['constant_prevalence_brier']
    return bool(ok)


def select_rule(rows,model):
    grid=[]
    for pc in P_CUTS:
        for gc in GAIN_CUTS:
            ev=evaluate(rows,model,None,pc,gc,25253); grid.append({'p_cut':pc,'gain_cut':gc,'qualifies':qualifies(ev),'summary':{k:v for k,v in ev.items() if k!='rows'}})
    good=[g for g in grid if g['qualifies']]
    if not good: return None,grid
    best=min(g['summary']['by_regime']['heteroskedastic']['paired_mean_edge_difference'] for g in good)
    near=[g for g in good if g['summary']['by_regime']['heteroskedastic']['paired_mean_edge_difference']<=best+.01]
    near.sort(key=lambda g:(-g['p_cut'],-g['gain_cut']))
    return {'p_cut':near[0]['p_cut'],'gain_cut':near[0]['gain_cut']},grid

if __name__=='__main__':
    me=generate(79001,2); out={'mechanics':{'passed':mechanics(me,2),'rows':me}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(79101,64); model=train_model(tr); rule,grid=select_rule(tr,model); out['training']={'model':model,'selected_rule':rule,'grid':grid,'mechanics_ok':mechanics(tr,64)}
        if rule is None or not mechanics(tr,64): out['disposition']='FALSIFIED_AT_TRAINING' if rule is None else 'BLOCKED_MECHANICS'
        else:
            va=generate(79601,32); ev=evaluate(va,model,rule,rule['p_cut'],rule['gain_cut'],25254); out['validation']={k:v for k,v in ev.items() if k!='rows'}
            if not qualifies(ev,validation=True): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(79901,64); ce=evaluate(co,model,rule,rule['p_cut'],rule['gain_cut'],25255); out['confirmation']={k:v for k,v in ce.items() if k!='rows'}; out['disposition']='LATENT_RESIDUAL_ADJUDICATION_SUPPORTED' if qualifies(ce,validation=True,confirmation=True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
