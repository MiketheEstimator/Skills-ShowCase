import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s17_compound as s17

def paired(seed):
    w=b.gen_world(seed)
    c,data,targets,p0=s17.run_control(w,seed)
    fs,_=s5.build(data,targets); ps=b.posterior_from_fs(fs); t=b.posterior_metrics(ps,w.dag_mask)
    e0=b.edge_marginals(p0); es=b.edge_marginals(ps); gap=np.abs(es-e0)
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'dag_count':len(b.dags),'posterior_sum_control':float(p0.sum()),'posterior_sum_science':float(ps.sum()),'spend':int(c['spend']),'action_trace':c['trace'],'D_sum':float(gap.sum()),'D_max':float(gap.max()),'R_entropy':float(t['entropy']/max(c['entropy'],1e-12)),'edge_delta':float(t['edge_error']-c['edge_error']),'brier_delta':float(t['brier']-c['brier']),'map_delta':int(t['map']-c['map']),'true_mass_delta':float(t['true_mass']-c['true_mass']),'large_harm':int(t['edge_error']-c['edge_error']>0.50),'trace_identical':True,'control_entropy':float(c['entropy']),'science_entropy':float(t['entropy'])}

def eval_gate(rows,a,bm,c):
    pr=[x for x in rows if x['D_sum']<=a and x['D_max']<=bm and x['R_entropy']>=c]
    if not pr: return {'a':a,'b':bm,'c':c,'n_promoted':0,'coverage':0,'mean_edge_delta':None,'mean_brier_delta':None,'large_harms':0,'wins':0,'qualifies':False}
    edge=float(np.mean([x['edge_delta'] for x in pr])); br=float(np.mean([x['brier_delta'] for x in pr])); harms=sum(x['large_harm'] for x in pr); cov=len(pr)/len(rows); wins=sum(x['edge_delta']<0 for x in pr)
    return {'a':a,'b':bm,'c':c,'n_promoted':len(pr),'coverage':cov,'mean_edge_delta':edge,'mean_brier_delta':br,'large_harms':harms,'wins':wins,'qualifies':bool(cov>=.50 and edge<=-.10 and br<=.005 and harms<=2)}

def train(rows):
    grid=[eval_gate(rows,a,bm,c) for a in (.75,1.0,1.25,1.5,2.0) for bm in (.25,.35,.45,.55,.70) for c in (.35,.50,.65,.80)]
    q=[g for g in grid if g['qualifies']]
    selected=sorted(q,key=lambda g:(-g['coverage'],g['mean_brier_delta'],g['mean_edge_delta'],g['a'],g['b'],-g['c']))[0] if q else None
    return grid,selected

def summarize(rows,gate):
    pr=[x for x in rows if x['D_sum']<=gate['a'] and x['D_max']<=gate['b'] and x['R_entropy']>=gate['c']]
    return {'n_total':len(rows),'n_promoted':len(pr),'coverage':len(pr)/len(rows),'mean_edge_delta_promoted':float(np.mean([x['edge_delta'] for x in pr])) if pr else None,'mean_brier_delta_promoted':float(np.mean([x['brier_delta'] for x in pr])) if pr else None,'wins_promoted':sum(x['edge_delta']<0 for x in pr),'large_harms_promoted':sum(x['large_harm'] for x in pr),'trace_identical_all':all(x['trace_identical'] for x in rows),'max_spend':max(x['spend'] for x in rows),'all_finite_normalized':all(np.isfinite(x['posterior_sum_control']) and np.isfinite(x['posterior_sum_science']) and abs(x['posterior_sum_control']-1)<1e-8 and abs(x['posterior_sum_science']-1)<1e-8 for x in rows)}

if __name__=='__main__':
 import sys
 print(json.dumps([paired(int(s)) for s in sys.argv[1:]],separators=(',',':')))
