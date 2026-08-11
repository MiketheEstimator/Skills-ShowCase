import json, numpy as np
import swarmite_exp002_s26_regime_diag as s26

THRESHOLDS=(2.0,3.0,4.0,5.0,6.0,8.0,12.0)
REGIMES=s26.REGIMES

def boot(vals,reps=10000,seed=22727):
    x=np.asarray(vals,float)
    if len(x)==0: return [None,None]
    rr=np.random.default_rng(seed)
    m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]

def apply(rows,t):
    out=[]
    for r in rows:
        use=bool(r['PPC_tail']>t)
        ed=float(r['edge_delta']) if use else 0.0
        bd=float(r['brier_delta']) if use else 0.0
        q=dict(r)
        q.update({'threshold':float(t),'selected':'ROBUST' if use else 'BASELINE','selected_edge_delta':ed,'selected_brier_delta':bd,'selected_large_harm':int(ed>0.50)})
        out.append(q)
    return out

def summarize(rows,seed=22727):
    ed=[r['selected_edge_delta'] for r in rows]; bd=[r['selected_brier_delta'] for r in rows]
    by={}
    for i,reg in enumerate(REGIMES):
        z=[r for r in rows if r['regime']==reg]
        by[reg]={
          'n':len(z),'mean_edge_delta':float(np.mean([r['selected_edge_delta'] for r in z])),
          'bootstrap95_edge_delta':boot([r['selected_edge_delta'] for r in z],seed=seed+i+10),
          'mean_brier_delta':float(np.mean([r['selected_brier_delta'] for r in z])),
          'robust_selected':sum(r['selected']=='ROBUST' for r in z),
          'large_harms':sum(r['selected_large_harm'] for r in z)
        }
    return {
      'n':len(rows),'mean_edge_delta':float(np.mean(ed)),'bootstrap95_edge_delta':boot(ed,seed=seed),
      'mean_brier_delta':float(np.mean(bd)),'wins':sum(x<0 for x in ed),'large_harms':sum(r['selected_large_harm'] for r in rows),
      'robust_selected':sum(r['selected']=='ROBUST' for r in rows),'coverage':1.0,'by_regime':by,
      'trace_identical_all':all(r['trace_identical'] for r in rows),'planning_reconstruction_ok':all(r['planning_reconstruction_max_abs']<=1e-10 for r in rows),
      'posterior_normalized':all(np.isfinite(r['posterior_sum']) and abs(r['posterior_sum']-1)<1e-8 for r in rows),'scores_finite':all(r['family_scores_finite'] for r in rows)
    }

def qualifies_training(sm):
    if sm['mean_edge_delta']>-0.10 or sm['mean_brier_delta']>0.005 or sm['large_harms']>5: return False
    lg=sm['by_regime']['linear_gaussian']
    if lg['mean_edge_delta']>0.10 or lg['mean_brier_delta']>0.010: return False
    for reg in REGIMES[1:]:
        v=sm['by_regime'][reg]
        if v['mean_edge_delta']>0 or v['mean_brier_delta']>0.005: return False
    return sm['coverage']==1.0 and sm['trace_identical_all']

def qualifies_validation(sm): return qualifies_training(sm)

def qualifies_confirmation(sm):
    if sm['mean_edge_delta']>-0.10 or sm['bootstrap95_edge_delta'][1]>=0 or sm['mean_brier_delta']>0.005 or sm['large_harms']>8: return False
    lg=sm['by_regime']['linear_gaussian']
    if lg['mean_edge_delta']>0.05 or lg['mean_brier_delta']>0.005: return False
    for reg in REGIMES[1:]:
        v=sm['by_regime'][reg]
        if v['mean_edge_delta']>=0 or v['bootstrap95_edge_delta'][1]>=0 or v['mean_brier_delta']>0.005: return False
    return sm['coverage']==1.0 and sm['trace_identical_all']

def training_grid(rows):
    g=[]
    for t in THRESHOLDS:
        selected=apply(rows,t); sm=summarize(selected,seed=22727+int(t*10)); g.append({'threshold':t,'summary':sm,'qualifies':qualifies_training(sm)})
    return g

def select_threshold(grid):
    q=[x for x in grid if x['qualifies']]
    if not q: return None
    best=min(x['summary']['mean_edge_delta'] for x in q)
    tied=[x for x in q if x['summary']['mean_edge_delta']<=best+0.01]
    return float(max(x['threshold'] for x in tied))

def generate(seeds): return [s26.paired(int(s)) for s in seeds]

if __name__=='__main__':
 import sys
 mode=sys.argv[1]
 if mode=='train':
    rows=generate(range(71100,71148)); grid=training_grid(rows); t=select_threshold(grid); print(json.dumps({'rows':rows,'grid':grid,'selected_threshold':t},separators=(',',':')))
 elif mode in ('validation','confirmation'):
    t=float(sys.argv[2]); seeds=range(71200,71248) if mode=='validation' else range(71300,71396); rows=apply(generate(seeds),t); print(json.dumps({'threshold':t,'rows':rows,'summary':summarize(rows,seed=22728 if mode=='validation' else 22729)},separators=(',',':')))
 else: raise SystemExit('mode must be train|validation|confirmation')
