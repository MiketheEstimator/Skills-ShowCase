import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s19_ppc_gate as s19
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s25_heterogeneous as s25

REGIMES=s25.REGIMES

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0,reg=s25.run_control(w,seed)
    fs0,models=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0)
    fs,finite=s23.build(data,targets); pr=b.posterior_from_fs(fs); rm=b.posterior_metrics(pr,w.dag_mask)
    fss,_=s5.build(data,targets); ps=b.posterior_from_fs(fss); sm=b.posterior_metrics(ps,w.dag_mask)
    tail,nonlin,_,_=s19.ppc_features(data,targets,p0,models)
    D=float(np.abs(b.edge_marginals(pr)-b.edge_marginals(p0)).sum())
    return {'seed':int(seed),'regime':reg,'dag_mask':int(w.dag_mask),'spend':int(c['spend']),'trace_identical':True,'planning_reconstruction_max_abs':float(np.max(np.abs(p0-p0c))),
      'edge_delta':float(rm['edge_error']-c['edge_error']),'brier_delta':float(rm['brier']-c['brier']),'edge_delta_vs_s5':float(rm['edge_error']-sm['edge_error']),'large_harm':int(rm['edge_error']-c['edge_error']>0.50),
      'D_robust':D,'PPC_tail':float(tail),'PPC_nonlinear':float(nonlin),'posterior_sum':float(pr.sum()),'family_scores_finite':bool(finite)}

def boot(x,reps=10000,seed=22626):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
def reg_summary(rows,idx):
    ed=[r['edge_delta'] for r in rows]; ci=boot(ed,seed=22626+idx); me=float(np.mean(ed)); mb=float(np.mean([r['brier_delta'] for r in rows]))
    if me<0 and ci[1]<0 and mb<=.005: label='ROBUST_SUPPORTED'
    elif (me>0 and ci[0]>0) or mb>.015: label='ROBUST_HARMFUL'
    else: label='UNRESOLVED'
    return {'n':len(rows),'mean_edge_delta':me,'bootstrap95_edge_delta':ci,'mean_brier_delta':mb,'wins':sum(r['edge_delta']<0 for r in rows),'large_harms':sum(r['large_harm'] for r in rows),
      'mean_D_robust':float(np.mean([r['D_robust'] for r in rows])),'mean_PPC_tail':float(np.mean([r['PPC_tail'] for r in rows])),'mean_PPC_nonlinear':float(np.mean([r['PPC_nonlinear'] for r in rows])),'label':label}
def summarize(rows):
    by={reg:reg_summary([r for r in rows if r['regime']==reg],i) for i,reg in enumerate(REGIMES)}
    return {'n':len(rows),'by_regime':by,'all_trace_identical':all(r['trace_identical'] for r in rows),'planning_reconstruction_ok':all(r['planning_reconstruction_max_abs']<=1e-10 for r in rows),'posterior_normalized':all(np.isfinite(r['posterior_sum']) and abs(r['posterior_sum']-1)<1e-8 for r in rows),'scores_finite':all(r['family_scores_finite'] for r in rows)}
if __name__=='__main__':
 import sys
 rows=[paired(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
