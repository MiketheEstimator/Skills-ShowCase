import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s49_hetero_likelihood as s49

CAPS=(0.10,0.20,0.30,0.40)
REGIMES=('linear','heteroskedastic')
FOLDS=5
EPS=0.05
RIDGE=1.0
LOGVAR_MIN=-4.0
LOGVAR_MAX=3.0


def sigmoid(x):
    x=max(-40.0,min(40.0,float(x)))
    return 1.0/(1.0+math.exp(-x))


def fit_mean(data,targets,v,pm,idx):
    idx=[i for i in idx if targets[i]!=v]
    y=data[idx,v]
    cols=[u for u in range(b.N) if pm>>u&1]
    X=data[idx][:,cols] if cols else np.empty((len(y),0))
    Xd=np.column_stack([np.ones(len(y)),X])
    A=np.eye(Xd.shape[1])/b.TAU2+Xd.T@Xd
    Ainv=np.linalg.inv(A); rhs=Xd.T@y; mu=Ainv@rhs
    quad=float(y@y-rhs@mu); _,ld=np.linalg.slogdet(A)
    logdetC=float(ld+Xd.shape[1]*math.log(b.TAU2))
    sc=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad)
    return float(sc),cols,mu


def cv_variance_evidence(data,targets):
    n=len(data); total_h=0.0; total_het=0.0; count=0
    all_idx=list(range(n))
    for fold in range(FOLDS):
        te=[i for i in all_idx if i%FOLDS==fold]
        tr=[i for i in all_idx if i%FOLDS!=fold]
        for v in range(b.N):
            candidates=[]
            for pm in range(1<<b.N):
                if pm>>v&1: continue
                sc,cols,mu=fit_mean(data,targets,v,pm,tr)
                candidates.append((sc,pm,cols,mu))
            _,pm,cols,mu=max(candidates,key=lambda z:z[0])
            trv=[i for i in tr if targets[i]!=v]
            tev=[i for i in te if targets[i]!=v]
            if len(trv)<8 or not tev: continue
            Xtr=data[trv][:,cols] if cols else np.empty((len(trv),0)); Xtr=np.column_stack([np.ones(len(trv)),Xtr])
            predtr=Xtr@mu; rtr=data[trv,v]-predtr
            var0=max(float(np.mean(rtr*rtr)),1e-6)
            ztr=np.log1p(np.abs(predtr)); Z=np.column_stack([np.ones(len(trv)),ztr]); target=np.log(rtr*rtr+EPS)
            coef=np.linalg.solve(Z.T@Z+RIDGE*np.eye(2),Z.T@target)
            Xte=data[tev][:,cols] if cols else np.empty((len(tev),0)); Xte=np.column_stack([np.ones(len(tev)),Xte])
            pred=Xte@mu; rr=data[tev,v]-pred
            logv=np.clip(np.column_stack([np.ones(len(tev)),np.log1p(np.abs(pred))])@coef,LOGVAR_MIN,LOGVAR_MAX); vv=np.exp(logv)
            total_h += float(-0.5*np.sum(math.log(2*math.pi*var0)+(rr*rr)/var0))
            total_het += float(-0.5*np.sum(np.log(2*math.pi*vv)+(rr*rr)/vv))
            count += len(tev)
    d=(total_het-total_h)/max(1,count)
    return float(d),float(sigmoid(d)),int(count),bool(np.isfinite(d) and np.isfinite(total_h) and np.isfinite(total_het))


def world_row(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s49.s30_posterior(data,targets,p0); phet,okh=s49.hetero_posterior(data,targets)
    dvar,qhet,nscore,oke=cv_variance_evidence(data,targets)
    bm=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask)
    cand={}
    for cap in CAPS:
        wt=cap*qhet; p=(1-wt)*ps30+wt*phet; p/=p.sum(); m=b.posterior_metrics(p,w.dag_mask)
        cand[str(cap)]={'weight':float(wt),'edge_delta':float(m['edge_error']-bm['edge_error']),'brier_delta':float(m['brier']-bm['brier']),'large_harm':int(m['edge_error']-bm['edge_error']>.50)}
    base=s48.world_row(external_seed)
    out=dict(base)
    out.update({'d_var':dvar,'q_het':qhet,'variance_score_n':nscore,'candidate':cand,'s30_edge_delta_vs_baseline':float(sm['edge_error']-bm['edge_error']),'s30_brier_delta_vs_baseline':float(sm['brier']-bm['brier']),'posterior_mechanics_ok':bool(ok30 and okh and oke),'s30_sum':float(ps30.sum()),'phet_sum':float(phet.sum())})
    return out


def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['posterior_mechanics_ok'] and r['variance_score_n']>0 and 0<=r['q_het']<=1 and abs(r['s30_sum']-1)<1e-8 and abs(r['phet_sum']-1)<1e-8 for r in rows)


def load_anchor(): return s48.load_anchor()
def promote_mask(rows,model,rule):
    pr=s46.predict(rows,model); mask=np.array([r['pred_edge_delta']<=rule['edge_cut'] and r['pred_harm_prob']<=rule['harm_cut'] for r in pr],bool); return mask,pr

def boot(x,reps=10000,seed=25050):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]

def stats(rows,mask,cap,seed):
    mask=np.asarray(mask,bool)
    if cap is None:
        ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows],float); ww=np.zeros(len(rows))
    else:
        key=str(cap); ed=np.array([r['candidate'][key]['edge_delta'] for r in rows],float); bd=np.array([r['candidate'][key]['brier_delta'] for r in rows],float); ww=np.array([r['candidate'][key]['weight'] for r in rows],float)
    he=np.where(mask,ed,0.0); hb=np.where(mask,bd,0.0); by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in rows]); mm=mask[idx]; ee=ed[idx]; wx=ww[idx]
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.0))),'large_harm_rate':float(np.sum((ee>.50)&mm)/max(1,mm.sum())),'mean_specialist_weight':float(np.mean(wx))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.50)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.50)&mask)/max(1,mask.sum())),'hybrid_mean_edge_delta':float(np.mean(he)),'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'mean_specialist_weight':float(np.mean(ww)),'by_regime':by}


def evaluate(rows,model,rule,cap,seed):
    mask,pr=promote_mask(rows,model,rule); frozen=stats(rows,mask,None,seed+1); mix=stats(rows,mask,cap,seed+2)
    retained=(abs(mix['hybrid_mean_edge_delta'])/abs(frozen['hybrid_mean_edge_delta'])) if frozen['hybrid_mean_edge_delta']<0 else 1.0
    return {'cap':cap,'mixture':mix,'frozen_s46_s30':frozen,'improvement_retained_vs_s46':float(retained),'mechanics_ok':all(r['posterior_mechanics_ok'] for r in rows),'rows':[dict(r,pred_edge_delta=float(p['pred_edge_delta']),pred_harm_prob=float(p['pred_harm_prob']),promote=bool(mask[i])) for i,(r,p) in enumerate(zip(rows,pr))]}


def qualifies(ev,confirmation=False):
    m=ev['mixture']; f=ev['frozen_s46_s30']; lin=m['by_regime']['linear']; het=m['by_regime']['heteroskedastic']; fhet=f['by_regime']['heteroskedastic']
    ok=ev['mechanics_ok'] and m['coverage']>=.50 and m['hybrid_mean_edge_delta']<0 and het['hybrid_mean_edge_delta']<0 and lin['hybrid_mean_edge_delta']<=.02 and m['promoted_large_harm_rate']<=.05 and het['large_harm_rate']<=.05 and m['hybrid_mean_brier_delta']<=.005 and ev['improvement_retained_vs_s46']>=.65 and het['hybrid_mean_edge_delta']<=fhet['hybrid_mean_edge_delta']+.02
    if confirmation: ok=ok and m['bootstrap95_hybrid_edge_delta'][1]<0
    return bool(ok)


def train(rows,model,rule):
    grid=[]
    for cap in CAPS:
        ev=evaluate(rows,model,rule,cap,25051); grid.append({'cap':cap,'summary':{k:v for k,v in ev.items() if k!='rows'},'qualifies':qualifies(ev)})
    good=[g for g in grid if g['qualifies']]
    if not good: return None,grid
    good.sort(key=lambda g:(g['summary']['mixture']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta'],g['cap']))
    best=good[0]; near=[g for g in good if g['summary']['mixture']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta']<=best['summary']['mixture']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta']+.01]; near.sort(key=lambda g:g['cap'])
    return near[0]['cap'],grid

if __name__=='__main__':
    model,rule=load_anchor(); me=generate(77001,2); out={'mechanics':{'passed':mechanics(me,2),'rows':me}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(77101,48); cap,grid=train(tr,model,rule); out['training']={'selected_cap':cap,'grid':grid,'mechanics_ok':mechanics(tr,48)}
        if cap is None or not mechanics(tr,48): out['disposition']='FALSIFIED_AT_TRAINING' if cap is None else 'BLOCKED_MECHANICS'
        else:
            va=generate(77501,24); ev=evaluate(va,model,rule,cap,25052); out['validation']={k:v for k,v in ev.items() if k!='rows'}
            if not mechanics(va,24) or not qualifies(ev): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(77801,48); ce=evaluate(co,model,rule,cap,25053); out['confirmation']={k:v for k,v in ce.items() if k!='rows'}; out['disposition']='WORLD_MODEL_MIXTURE_SUPPORTED' if mechanics(co,48) and qualifies(ce,True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
