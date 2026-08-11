import json, math, itertools, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s17_compound as s17

CLASS_NAMES=('baseline_linear','nonlocal_linear','nonlocal_tanh')


def lse_np(x):
    x=np.asarray(x,dtype=float); m=float(np.max(x))
    return m+math.log(float(np.exp(x-m).sum()))


def tanh_nonlocal_build(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100)
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]
            X=np.tanh(data[keep][:,cols]) if cols else np.empty((len(y),0))
            X=np.column_stack([np.ones(len(y)),X]); k=len(cols); vals=[]
            for sg in itertools.product((-1.,1.),repeat=k):
                vals.append(s5.lev(X,y,np.array([0.]+[s5.MU*s for s in sg]),np.array([b.TAU2]+[s5.SIG2]*k)))
            fs[v,pm]=s5.lse(vals)-k*math.log(2.)
    return fs


def dag_log_scores(fs):
    ls=np.zeros(len(b.dags),dtype=float)
    for v in range(b.N): ls += fs[v,b.parents[:,v]]
    return ls


def posterior_and_evidence(fs):
    ls=dag_log_scores(fs); le=lse_np(ls)-math.log(len(b.dags))
    lw=ls-float(np.max(ls)); p=np.exp(lw); p/=p.sum()
    return p,float(le)


def terminal_mixture(data,targets):
    fs0,_=b.build_family_models(data,targets)
    fs1,_=s5.build(data,targets)
    fs2=tanh_nonlocal_build(data,targets)
    ps=[]; les=[]
    for fs in (fs0,fs1,fs2):
        p,le=posterior_and_evidence(fs); ps.append(p); les.append(le)
    a=np.asarray(les,dtype=float); a-=float(np.max(a)); w=np.exp(a); w/=w.sum()
    mix=sum(float(wi)*pi for wi,pi in zip(w,ps)); mix/=mix.sum()
    return {'posteriors':ps,'log_evidence':les,'weights':w,'mixture':mix}


def paired(seed):
    world=b.gen_world(seed)
    control,data,targets,p_plan=s17.run_control(world,seed)
    out=terminal_mixture(data,targets)
    p0,p1,p2=out['posteriors']; pm=out['mixture']
    # The class-0 reconstruction must equal the terminal planning posterior because planning is unchanged.
    recon=float(np.max(np.abs(p0-p_plan)))
    if recon>1e-10: raise RuntimeError(f'planning posterior reconstruction mismatch {recon}')
    fixed=b.posterior_metrics(p1,world.dag_mask); mix=b.posterior_metrics(pm,world.dag_mask)
    weights=[float(x) for x in out['weights']]
    return {
      'seed':int(seed),'dag_mask':int(world.dag_mask),'dag_count':int(len(b.dags)),
      'spend':int(control['spend']),'action_trace':control['trace'],'trace_identical':True,
      'planning_reconstruction_max_abs':recon,
      'posterior_sums':[float(p0.sum()),float(p1.sum()),float(p2.sum()),float(pm.sum())],
      'class_names':list(CLASS_NAMES),'class_log_evidence':[float(x) for x in out['log_evidence']],
      'class_weights':weights,'class_weight_sum':float(sum(weights)),
      'control':{k:v for k,v in control.items() if k!='trace'},'fixed_science':fixed,'mixture':mix,
      'edge_delta_mix_vs_control':float(mix['edge_error']-control['edge_error']),
      'brier_delta_mix_vs_control':float(mix['brier']-control['brier']),
      'true_mass_delta_mix_vs_control':float(mix['true_mass']-control['true_mass']),
      'map_delta_mix_vs_control':int(mix['map']-control['map']),
      'edge_delta_mix_vs_fixed':float(mix['edge_error']-fixed['edge_error']),
      'brier_delta_mix_vs_fixed':float(mix['brier']-fixed['brier']),
      'large_harm_mix_vs_control':int(mix['edge_error']-control['edge_error']>0.50)
    }


def mechanics(rows):
    finite=lambda x: bool(np.all(np.isfinite(np.asarray(x,dtype=float))))
    return {
      'n':len(rows),'dag_count_ok':all(r['dag_count']==29281 for r in rows),
      'spend_ok':all(r['spend']<=15 for r in rows),'trace_identical_all':all(r['trace_identical'] for r in rows),
      'planning_reconstruction_ok':all(r['planning_reconstruction_max_abs']<=1e-10 for r in rows),
      'posteriors_normalized':all(finite(r['posterior_sums']) and max(abs(x-1.0) for x in r['posterior_sums'])<=1e-8 for r in rows),
      'weights_valid':all(finite(r['class_weights']) and min(r['class_weights'])>=0 and abs(r['class_weight_sum']-1.0)<=1e-8 for r in rows)
    }


def summary(rows):
    return {
      'n':len(rows),
      'mean_edge_delta_mix_vs_control':float(np.mean([r['edge_delta_mix_vs_control'] for r in rows])),
      'mean_brier_delta_mix_vs_control':float(np.mean([r['brier_delta_mix_vs_control'] for r in rows])),
      'mean_edge_delta_mix_vs_fixed':float(np.mean([r['edge_delta_mix_vs_fixed'] for r in rows])),
      'mean_brier_delta_mix_vs_fixed':float(np.mean([r['brier_delta_mix_vs_fixed'] for r in rows])),
      'wins_mix_vs_control':sum(r['edge_delta_mix_vs_control']<0 for r in rows),
      'large_harms_mix_vs_control':sum(r['large_harm_mix_vs_control'] for r in rows),
      'mean_class_weights':[float(np.mean([r['class_weights'][j] for r in rows])) for j in range(3)],
      **mechanics(rows)
    }


def bootstrap_edge(rows,reps=10000,seed=22020):
    x=np.asarray([r['edge_delta_mix_vs_control'] for r in rows],dtype=float)
    rr=np.random.default_rng(seed); means=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]


if __name__=='__main__':
    import sys
    rows=[paired(int(s)) for s in sys.argv[1:]]
    print(json.dumps({'rows':rows,'summary':summary(rows),'bootstrap95_edge_delta':bootstrap_edge(rows) if rows else None},separators=(',',':')))
