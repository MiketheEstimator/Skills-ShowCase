import json, numpy as np, math
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s17_compound as s17

def residual_features(data,targets,p0):
    fs,models=b.build_family_models(data,targets); gi=int(np.argmax(p0)); tail=[]; nonlin=[]
    for v in range(b.N):
        pm=int(b.parents[gi,v]); cols,mu,Ainv=models[(v,pm)]; keep=np.array([t!=v for t in targets],dtype=bool); rows=data[keep]; y=rows[:,v]; zs=[]; preds=[]
        for row,yy in zip(rows,y):
            x=np.array([1.0]+[row[u] for u in cols]); pred=float(x@mu); scale=math.sqrt(max(1.0+float(x@Ainv@x),1e-12)); zs.append(float(np.clip((yy-pred)/scale,-8,8))); preds.append(math.tanh(pred))
        z=np.asarray(zs); q=np.asarray(preds); tail.append(abs(float(np.mean(z**4))-3.0) if len(z) else 0.0)
        nonlin.append(abs(float(np.corrcoef(z,q)[0,1])) if len(z)>=3 and np.std(z)>1e-12 and np.std(q)>1e-12 else 0.0)
    return float(max(tail)),float(max(nonlin))

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0=s17.run_control(w,seed); fs,_=s5.build(data,targets); ps=b.posterior_from_fs(fs); t=b.posterior_metrics(ps,w.dag_mask); gap=np.abs(b.edge_marginals(ps)-b.edge_marginals(p0)); tail,nl=residual_features(data,targets,p0)
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'dag_count':len(b.dags),'posterior_sum_control':float(p0.sum()),'posterior_sum_science':float(ps.sum()),'spend':int(c['spend']),'action_trace':c['trace'],'D_sum':float(gap.sum()),'PPC_tail':tail,'PPC_nonlinear':nl,'edge_delta':float(t['edge_error']-c['edge_error']),'brier_delta':float(t['brier']-c['brier']),'map_delta':int(t['map']-c['map']),'true_mass_delta':float(t['true_mass']-c['true_mass']),'large_harm':int(t['edge_error']-c['edge_error']>0.50),'trace_identical':True}

def eval_gate(rows,a,t,n):
    pr=[x for x in rows if x['D_sum']<=a and x['PPC_tail']<=t and x['PPC_nonlinear']<=n]
    if not pr:return {'a':a,'t':t,'n':n,'n_promoted':0,'coverage':0,'mean_edge_delta':None,'mean_brier_delta':None,'large_harms':0,'wins':0,'qualifies':False}
    cov=len(pr)/len(rows); e=float(np.mean([x['edge_delta'] for x in pr])); br=float(np.mean([x['brier_delta'] for x in pr])); h=sum(x['large_harm'] for x in pr); w=sum(x['edge_delta']<0 for x in pr)
    return {'a':a,'t':t,'n':n,'n_promoted':len(pr),'coverage':cov,'mean_edge_delta':e,'mean_brier_delta':br,'large_harms':h,'wins':w,'qualifies':bool(cov>=.5 and e<=-.1 and br<=.005 and h<=2)}
def train(rows):
    grid=[eval_gate(rows,a,t,n) for a in (1.,1.25,1.5,2.,3.) for t in (.5,1.,2.,4.,8.) for n in (.1,.2,.3,.45,.6)]; q=[g for g in grid if g['qualifies']]
    return grid,(sorted(q,key=lambda g:(-g['coverage'],g['mean_brier_delta'],g['mean_edge_delta'],g['a'],g['t'],g['n']))[0] if q else None)
def summarize(rows,g):
    pr=[x for x in rows if x['D_sum']<=g['a'] and x['PPC_tail']<=g['t'] and x['PPC_nonlinear']<=g['n']]
    return {'n_total':len(rows),'n_promoted':len(pr),'coverage':len(pr)/len(rows),'mean_edge_delta_promoted':float(np.mean([x['edge_delta'] for x in pr])) if pr else None,'mean_brier_delta_promoted':float(np.mean([x['brier_delta'] for x in pr])) if pr else None,'wins_promoted':sum(x['edge_delta']<0 for x in pr),'large_harms_promoted':sum(x['large_harm'] for x in pr),'trace_identical_all':all(x['trace_identical'] for x in rows),'max_spend':max(x['spend'] for x in rows),'all_finite_normalized':all(np.isfinite(x['posterior_sum_control']) and np.isfinite(x['posterior_sum_science']) and abs(x['posterior_sum_control']-1)<1e-8 and abs(x['posterior_sum_science']-1)<1e-8 for x in rows)}
if __name__=='__main__':
 import sys
 print(json.dumps([paired(int(s)) for s in sys.argv[1:]],separators=(',',':')))
