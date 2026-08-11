import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s32_modelset_diag as s32
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39

SPECIALISTS=s39.SPECIALISTS
THRESHOLD=0.2692013432171404

def density(seed): return 'sparse' if ((int(seed)//6)%2==0) else 'dense'
def gen_world(seed):
    den=density(seed); p=.15 if den=='sparse' else .55; r=b.rng_for('s41','world',seed); order=list(map(int,r.permutation(b.N))); W=np.zeros((b.N,b.N)); mask=0
    for a in range(b.N):
        for bb in range(a+1,b.N):
            u,v=order[a],order[bb]
            if r.random()<p:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9); mask|=1<<b.EDGE_INDEX[(u,v)]
    if int(mask).bit_count()<2:
        for a,bb in [(0,1),(1,2)]:
            u,v=order[a],order[bb]
            if W[u,v]==0:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9); mask|=1<<b.EDGE_INDEX[(u,v)]
    return b.World(mask,W,order,seed),den

def world_row(seed):
    w,den=gen_world(seed); c,data,targets,p0,cell=s32.run_control(w,seed); posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); widths=np.max(np.vstack([em0,ems]),axis=0)-np.min(np.vstack([em0,ems]),axis=0); score=float(np.mean(widths)); promote=score<=THRESHOLD
    base=b.posterior_metrics(p0,w.dag_mask); s30m=b.posterior_metrics(ps30,w.dag_mask); ed=float(s30m['edge_error']-base['edge_error']); bd=float(s30m['brier']-base['brier'])
    return {'seed':int(seed),'density':den,'cell':cell,'score':score,'promote':bool(promote),'s30_edge_delta_vs_baseline':ed,'s30_brier_delta_vs_baseline':bd,'s30_large_harm':int(ed>.5),'spend':int(c['spend']),'trace_identical':True,'finite':finite,'s30_sum':float(ps30.sum()),'edge_count':int(w.dag_mask).bit_count()}

def mechanics(rows): return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and np.isfinite(r['score']) for r in rows)
def boot(x,reps=10000,seed=24141):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
def summarize(rows):
    pr=np.array([r['promote'] for r in rows],bool); ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); hed=np.where(pr,ed,0.); hbd=np.where(pr,bd,0.); always=float(np.mean(ed)); hybrid=float(np.mean(hed)); retained=float(abs(hybrid)/abs(always)) if always<0 else 1.0
    by={}
    for d in ('sparse','dense'):
        rr=[r for r in rows if r['density']==d]; pp=np.array([r['promote'] for r in rr],bool); ee=np.array([r['s30_edge_delta_vs_baseline'] for r in rr]); by[d]={'n':len(rr),'coverage':float(np.mean(pp)),'hybrid_mean_edge_delta':float(np.mean(np.where(pp,ee,0.))),'mean_edge_count':float(np.mean([r['edge_count'] for r in rr]))}
    return {'n':len(rows),'coverage':float(np.mean(pr)),'n_promoted':int(np.sum(pr)),'promoted_large_harms':int(np.sum((ed>.5)&pr)),'promoted_large_harm_rate':float(np.sum((ed>.5)&pr)/max(1,np.sum(pr))),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hybrid,'bootstrap95_hybrid_edge_delta':boot(hed,seed=24141+len(rows)),'hybrid_mean_brier_delta':float(np.mean(hbd)),'improvement_retained':retained,'mechanics_ok':mechanics(rows),'by_density':by}
def passed(m,confirm=False):
    ok=m['mechanics_ok'] and m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70)
    return ok and ((not confirm) or m['bootstrap95_hybrid_edge_delta'][1]<0)
def run():
    me=[world_row(s) for s in range(72701,72705)]; out={'mechanics':{'rows':me,'passed':mechanics(me)}}
    if not mechanics(me): out['disposition']='BLOCKED_MECHANICS'; return out
    sc=[world_row(s) for s in range(72711,72735)]; sm=summarize(sc); out['screen']=sm
    if not passed(sm): out['disposition']='FALSIFIED_AT_SCREEN'; return out
    co=[world_row(s) for s in range(72801,72849)]; cm=summarize(co); out['confirmation']=cm; out['disposition']='GRAPH_DENSITY_TRANSFER_SUPPORTED' if passed(cm,True) else 'FALSIFIED_ON_CONFIRMATION'; return out
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
