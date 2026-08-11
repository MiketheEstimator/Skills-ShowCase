import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s17_compound as s17
import swarmite_exp002_s20_mixture as s20

TAUS=(0.00,0.02,0.05,0.10,0.25,0.50,1.00)

def softmax(x):
    x=np.asarray(x,float); x=x-float(np.max(x)); y=np.exp(x); return y/y.sum()

def base_world(seed):
    w=b.gen_world(seed); c,data,targets,p_plan=s17.run_control(w,seed); out=s20.terminal_mixture(data,targets)
    if float(np.max(np.abs(out['posteriors'][0]-p_plan)))>1e-10: raise RuntimeError('planning posterior reconstruction mismatch')
    return w,c,out

def eval_tau(base,tau):
    w,c,out=base; weights=softmax(float(tau)*np.asarray(out['log_evidence'],float)); p=sum(float(wi)*pi for wi,pi in zip(weights,out['posteriors'])); p/=p.sum(); m=b.posterior_metrics(p,w.dag_mask)
    return {'tau':float(tau),'class_weights':[float(x) for x in weights],'posterior_sum':float(p.sum()),
      'edge_delta':float(m['edge_error']-c['edge_error']),'brier_delta':float(m['brier']-c['brier']),
      'map_delta':int(m['map']-c['map']),'true_mass_delta':float(m['true_mass']-c['true_mass']),
      'large_harm':int(m['edge_error']-c['edge_error']>0.50),'metrics':m}

def row(seed):
    base=base_world(seed); w,c,out=base
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'dag_count':len(b.dags),'spend':int(c['spend']),'action_trace':c['trace'],
      'log_evidence':[float(x) for x in out['log_evidence']], 'tau_results':[eval_tau(base,t) for t in TAUS]}

def aggregate(rows,tau):
    ix=TAUS.index(float(tau)); rs=[r['tau_results'][ix] for r in rows]
    return {'tau':float(tau),'n':len(rows),'mean_edge_delta':float(np.mean([x['edge_delta'] for x in rs])),
      'mean_brier_delta':float(np.mean([x['brier_delta'] for x in rs])),'wins':sum(x['edge_delta']<0 for x in rs),
      'large_harms':sum(x['large_harm'] for x in rs),'mean_class_weights':[float(np.mean([x['class_weights'][j] for x in rs])) for j in range(3)],
      'trace_identical_all':True,'dag_count_ok':all(r['dag_count']==29281 for r in rows),'spend_ok':all(r['spend']<=15 for r in rows),
      'normalized':all(abs(x['posterior_sum']-1)<1e-8 and np.isfinite(x['posterior_sum']) for x in rs)}

def train(rows):
    grid=[aggregate(rows,t) for t in TAUS]
    q=[g for g in grid if g['mean_edge_delta']<=-.10 and g['mean_brier_delta']<=.005 and g['large_harms']<=3 and g['trace_identical_all'] and g['dag_count_ok'] and g['spend_ok'] and g['normalized']]
    if not q:return grid,None
    best=min(g['mean_edge_delta'] for g in q); near=[g for g in q if g['mean_edge_delta']<=best+.01]; sel=max(near,key=lambda g:g['tau'])
    return grid,sel

def summarize(rows,tau): return aggregate(rows,float(tau))
def bootstrap(rows,tau,reps=10000,seed=22222):
    ix=TAUS.index(float(tau)); x=np.asarray([r['tau_results'][ix]['edge_delta'] for r in rows]); rr=np.random.default_rng(seed); means=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]

if __name__=='__main__':
 import sys
 args=sys.argv[1:]; mode='rows'
 if args and args[0] in ('train','rows'): mode=args.pop(0)
 rows=[row(int(s)) for s in args]
 if mode=='train':
  grid,selected=train(rows); print(json.dumps({'rows':rows,'grid':grid,'selected':selected},separators=(',',':')))
 else: print(json.dumps({'rows':rows},separators=(',',':')))
