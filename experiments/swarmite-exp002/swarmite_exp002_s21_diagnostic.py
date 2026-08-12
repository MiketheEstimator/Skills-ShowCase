import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s17_compound as s17
import swarmite_exp002_s20_mixture as s20


def paired(seed):
    w=b.gen_world(seed); c,data,targets,p_plan=s17.run_control(w,seed); out=s20.terminal_mixture(data,targets)
    ps=out['posteriors']; pm=out['mixture']; weights=np.asarray(out['weights'],float)
    cms=[b.posterior_metrics(p,w.dag_mask) for p in ps]; mm=b.posterior_metrics(pm,w.dag_mask)
    ee=[float(b.edge_marginals(p).sum()) for p in ps]; true_edges=int(w.dag_mask).bit_count()
    selected=int(np.argmax(weights)); best=int(np.argmin([m['edge_error'] for m in cms]))
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'true_edges':true_edges,'spend':int(c['spend']),'action_trace':c['trace'],
      'class_names':list(s20.CLASS_NAMES),'class_weights':[float(x) for x in weights],'class_log_evidence':[float(x) for x in out['log_evidence']],
      'class_metrics':cms,'class_expected_edges':ee,'mixture_metrics':mm,
      'selected_class':selected,'best_class':best,'selected_is_best':int(selected==best),
      'selection_regret':float(cms[selected]['edge_error']-cms[best]['edge_error']),
      'mixture_regret':float(mm['edge_error']-cms[best]['edge_error']),
      'oracle_best_delta_vs_control':float(cms[best]['edge_error']-c['edge_error']),
      'mixture_delta_vs_control':float(mm['edge_error']-c['edge_error']),
      'dominant_density_error':float(ee[selected]-true_edges),'control_edge_error':float(c['edge_error'])}


def corr(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<2 or np.std(x)<1e-12 or np.std(y)<1e-12:return 0.0
    v=float(np.corrcoef(x,y)[0,1]); return v if np.isfinite(v) else 0.0


def summarize(rows):
    selected_best=float(np.mean([r['selected_is_best'] for r in rows])); oracle=float(np.mean([r['oracle_best_delta_vs_control'] for r in rows])); reg=float(np.mean([r['selection_regret'] for r in rows]))
    if selected_best<.50 and oracle<=-.10 and reg>=.20: disposition='EVIDENCE_DOMINANCE_FAILURE'
    elif oracle>-.10: disposition='SHARED_MODEL_CLASS_FAILURE'
    else: disposition='MIXED_FAILURE_MODE'
    return {'n':len(rows),'selected_class_best_rate':selected_best,'mean_oracle_best_delta_vs_control':oracle,
      'mean_selection_regret':reg,'mean_mixture_regret':float(np.mean([r['mixture_regret'] for r in rows])),
      'mean_mixture_delta_vs_control':float(np.mean([r['mixture_delta_vs_control'] for r in rows])),
      'mean_class_weights':[float(np.mean([r['class_weights'][j] for r in rows])) for j in range(3)],
      'selected_class_counts':[sum(r['selected_class']==j for r in rows) for j in range(3)],
      'best_class_counts':[sum(r['best_class']==j for r in rows) for j in range(3)],
      'mean_dominant_density_error':float(np.mean([r['dominant_density_error'] for r in rows])),
      'dominant_weight_vs_mixture_harm_r':corr([max(r['class_weights']) for r in rows],[r['mixture_delta_vs_control'] for r in rows]),
      'tanh_weight_vs_mixture_harm_r':corr([r['class_weights'][2] for r in rows],[r['mixture_delta_vs_control'] for r in rows]),
      'disposition':disposition}

if __name__=='__main__':
 import sys
 rows=[paired(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
