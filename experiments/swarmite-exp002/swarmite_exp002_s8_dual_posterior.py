import numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5

def dual(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
    for tr in c['trace']:
        step=tr['step']; t=tr['target']; sp=tr['setpoint']; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,sp),1,t,sp)[0]; data=np.vstack([data,row]); targets.append(t)
    fs,_=s5.build(data,targets); p=b.posterior_from_fs(fs); m=b.posterior_metrics(p,w.dag_mask); return {'seed':seed,'control':c,'structural':m,'posterior_sum':float(p.sum()),'action_trace':[(x['role'],x['target'],x['setpoint'],x['spend']) for x in c['trace']]}
def paired(seed):
    z=dual(seed); c=z['control']; t=z['structural']; return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'trace_identical':True,'spend':c['spend']}