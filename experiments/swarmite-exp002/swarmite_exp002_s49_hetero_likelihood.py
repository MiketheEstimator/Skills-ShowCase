import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48

BETAS=(0.25,0.50,0.75,1.00)
REGIMES=('linear','heteroskedastic')
EPS=0.05
RIDGE=1.0
LOGVAR_MIN=-4.0
LOGVAR_MAX=3.0
ADJ_CLIP=12.0

def s30_posterior(data,targets,p0):
    posts={'LG':p0.copy()}
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n)
        if not ok: return p0.copy(),False
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT')
    alpha=s33.sigmoid((tt-lg)/s33.T)
    p=(1-alpha)*posts['LG']+alpha*posts['TT']; p/=p.sum()
    return p,bool(np.all(np.isfinite(p)))

def hetero_posterior(data,targets):
    fs,models=b.build_family_models(data,targets); hs=fs.copy()
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]; n=len(y)
        if n<8: continue
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols,mu,_=models[(v,pm)]
            X=data[keep][:,cols] if cols else np.empty((n,0)); Xd=np.column_stack([np.ones(n),X]); pred=Xd@mu; res=y-pred
            z=np.log1p(np.abs(pred)); Z=np.column_stack([np.ones(n),z]); target=np.log(res*res+EPS)
            A=Z.T@Z + RIDGE*np.eye(2); coef=np.linalg.solve(A,Z.T@target)
            logvar=np.clip(Z@coef,LOGVAR_MIN,LOGVAR_MAX); var=np.exp(logvar)
            llh=float(-0.5*np.sum(np.log(2*math.pi*var)+(res*res)/var))
            var0=max(float(np.mean(res*res)),1e-6); ll0=float(-0.5*np.sum(math.log(2*math.pi*var0)+(res*res)/var0))
            adj=llh-ll0-0.5*math.log(max(n,2))
            hs[v,pm]=fs[v,pm]+float(np.clip(adj,-ADJ_CLIP,ADJ_CLIP))
    p=b.posterior_from_fs(hs)
    return p,bool(np.all(np.isfinite(p)) and abs(float(p.sum())-1.0)<1e-8)

def world_row(external_seed):
    base_row=s48.world_row(external_seed)
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s30_posterior(data,targets,p0); phet,okh=hetero_posterior(data,targets)
    bm=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); hm=b.posterior_metrics(phet,w.dag_mask)
    cand={}
    for beta in BETAS:
        p=(1-beta)*ps30+beta*phet; p/=p.sum(); m=b.posterior_metrics(p,w.dag_mask)
        cand[str(beta)]={'edge_delta':float(m['edge_error']-bm['edge_error']),'brier_delta':float(m['brier']-bm['brier']),'large_harm':int(m['edge_error']-bm['edge_error']>.50)}
    out=dict(base_row)
    out.update({'phet_edge_delta_vs_baseline':float(hm['edge_error']-bm['edge_error']),'phet_brier_delta_vs_baseline':float(hm['brier']-bm['brier']),'candidate':cand,'posterior_mechanics_ok':bool(ok30 and okh),'phet_sum':float(phet.sum())})
    return out

def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]

def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['posterior_mechanics_ok'] and abs(r['phet_sum']-1)<1e-8 for r in rows)

def load_anchor(): return s48.load_anchor()
def promote_mask(rows,model,rule):
    pr=s46.predict(rows,model)
    mask=np.array([r['pred_edge_delta']<=rule['edge_cut'] and r['pred_harm_prob']<=rule['harm_cut'] for r in pr],bool)
    return mask,pr

def boot(x,reps=10000,seed=24949):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]
def stats(rows,mask,beta,seed):
    mask=np.asarray(mask,bool)
    if beta is None:
        ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows],float)
    else:
        key=str(beta); ed=np.array([r['candidate'][key]['edge_delta'] for r in rows],float); bd=np.array([r['candidate'][key]['brier_delta'] for r in rows],float)
    he=np.where(mask,ed,0.0); hb=np.where(mask,bd,0.0); by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in rows]); mm=mask[idx]; ee=ed[idx]
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.0))),'large_harm_rate':float(np.sum((ee>.50)&mm)/max(1,mm.sum()))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.50)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.50)&mask)/max(1,mask.sum())),'hybrid_mean_edge_delta':float(np.mean(he)),'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'by_regime':by}

def evaluate(rows,model,rule,beta,seed):
    mask,pr=promote_mask(rows,model,rule); frozen=stats(rows,mask,None,seed+1); spec=stats(rows,mask,beta,seed+2)
    retained=(abs(spec['hybrid_mean_edge_delta'])/abs(frozen['hybrid_mean_edge_delta'])) if frozen['hybrid_mean_edge_delta']<0 else 1.0
    return {'beta':beta,'specialist':spec,'frozen_s46_s30':frozen,'improvement_retained_vs_s46':float(retained),'mechanics_ok':all(r['posterior_mechanics_ok'] for r in rows),'rows':[dict(r,pred_edge_delta=float(p['pred_edge_delta']),pred_harm_prob=float(p['pred_harm_prob']),promote=bool(mask[i])) for i,(r,p) in enumerate(zip(rows,pr))]}

def qualifies(ev,confirmation=False):
    m=ev['specialist']; f=ev['frozen_s46_s30']; lin=m['by_regime']['linear']; het=m['by_regime']['heteroskedastic']; fhet=f['by_regime']['heteroskedastic']
    ok=ev['mechanics_ok'] and m['coverage']>=.50 and m['hybrid_mean_edge_delta']<0 and het['hybrid_mean_edge_delta']<0 and lin['hybrid_mean_edge_delta']<=.02 and m['promoted_large_harm_rate']<=.05 and het['large_harm_rate']<=.05 and m['hybrid_mean_brier_delta']<=.005 and ev['improvement_retained_vs_s46']>=.65 and het['hybrid_mean_edge_delta']<=fhet['hybrid_mean_edge_delta']+.02
    if confirmation: ok=ok and m['bootstrap95_hybrid_edge_delta'][1]<0
    return bool(ok)

def train(rows,model,rule):
    grid=[]
    for beta in BETAS:
        ev=evaluate(rows,model,rule,beta,24950); grid.append({'beta':beta,'summary':{k:v for k,v in ev.items() if k!='rows'},'qualifies':qualifies(ev)})
    good=[g for g in grid if g['qualifies']]
    if not good: return None,grid
    good.sort(key=lambda g:(g['summary']['specialist']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta'],g['beta']))
    best=good[0]
    near=[g for g in good if g['summary']['specialist']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta']<=best['summary']['specialist']['by_regime']['heteroskedastic']['hybrid_mean_edge_delta']+.01]
    near.sort(key=lambda g:g['beta'])
    return near[0]['beta'],grid

if __name__=='__main__':
    model,rule=load_anchor(); me=generate(75801,2); out={'mechanics':{'passed':mechanics(me,2),'rows':me}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(75901,48); beta,grid=train(tr,model,rule); out['training']={'selected_beta':beta,'grid':grid,'mechanics_ok':mechanics(tr,48)}
        if beta is None or not mechanics(tr,48): out['disposition']='FALSIFIED_AT_TRAINING' if beta is None else 'BLOCKED_MECHANICS'
        else:
            va=generate(76301,24); ev=evaluate(va,model,rule,beta,24951); out['validation']={k:v for k,v in ev.items() if k!='rows'}
            if not mechanics(va,24) or not qualifies(ev): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(76601,48); ce=evaluate(co,model,rule,beta,24952); out['confirmation']={k:v for k,v in ce.items() if k!='rows'}; out['disposition']='HETEROSKEDASTIC_LIKELIHOOD_SPECIALIST_SUPPORTED' if mechanics(co,48) and qualifies(ce,True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
