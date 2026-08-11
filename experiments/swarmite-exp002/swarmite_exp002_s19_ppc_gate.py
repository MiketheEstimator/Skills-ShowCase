import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s17_compound as s17

A_GRID=(1.00,1.25,1.50,2.00,3.00)
T_GRID=(0.50,1.00,2.00,4.00,8.00)
N_GRID=(0.10,0.20,0.30,0.45,0.60)

def ppc_features(data,targets,p0,models):
    gi=int(np.argmax(p0)); map_mask=int(b.dags[gi])
    tail=[]; nonlin=[]; node_detail=[]
    for v in range(b.N):
        pm=int(b.parents[gi,v]); cols,mu,Ainv=models[(v,pm)]
        keep=np.array([t!=v for t in targets],dtype=bool)
        rows=data[keep]
        if len(rows)==0:
            tail.append(0.0); nonlin.append(0.0); node_detail.append({'node':v,'n':0,'tail':0.0,'nonlinear':0.0}); continue
        X=np.column_stack([np.ones(len(rows))]+[rows[:,u] for u in cols]) if cols else np.ones((len(rows),1))
        pred=X@mu
        scales=np.sqrt(np.maximum(1.0+np.einsum('ij,jk,ik->i',X,Ainv,X),1e-12))
        z=np.clip((rows[:,v]-pred)/scales,-8.0,8.0)
        tv=float(abs(np.mean(z**4)-3.0))
        q=np.tanh(pred)
        if len(z)<2 or float(np.std(z))<1e-12 or float(np.std(q))<1e-12:
            nv=0.0
        else:
            nv=float(abs(np.corrcoef(z,q)[0,1])); nv=nv if np.isfinite(nv) else 0.0
        tail.append(tv); nonlin.append(nv); node_detail.append({'node':v,'n':int(len(z)),'tail':tv,'nonlinear':nv})
    return float(max(tail) if tail else 0.0),float(max(nonlin) if nonlin else 0.0),node_detail,map_mask

def paired(seed):
    w=b.gen_world(seed)
    c,data,targets,p0=s17.run_control(w,seed)
    fs0,models=b.build_family_models(data,targets)
    # Ensure features use the exact terminal planning posterior reconstructed from the terminal data.
    p0_check=b.posterior_from_fs(fs0)
    if float(np.max(np.abs(p0_check-p0)))>1e-10:
        raise RuntimeError('terminal planning posterior reconstruction mismatch')
    fss,_=s5.build(data,targets); ps=b.posterior_from_fs(fss); t=b.posterior_metrics(ps,w.dag_mask)
    e0=b.edge_marginals(p0); es=b.edge_marginals(ps)
    D_sum=float(np.abs(es-e0).sum())
    tail,nonlin,node_detail,map_mask=ppc_features(data,targets,p0,models)
    return {
      'seed':int(seed),'dag_mask':int(w.dag_mask),'planning_map_mask':int(map_mask),'dag_count':len(b.dags),
      'posterior_sum_control':float(p0.sum()),'posterior_sum_science':float(ps.sum()),'spend':int(c['spend']),
      'action_trace':c['trace'],'D_sum':D_sum,'PPC_tail':tail,'PPC_nonlinear':nonlin,'ppc_nodes':node_detail,
      'edge_delta':float(t['edge_error']-c['edge_error']),'brier_delta':float(t['brier']-c['brier']),
      'map_delta':int(t['map']-c['map']),'true_mass_delta':float(t['true_mass']-c['true_mass']),
      'large_harm':int(t['edge_error']-c['edge_error']>0.50),'trace_identical':True,
      'control_entropy':float(c['entropy']),'science_entropy':float(t['entropy'])}

def eval_gate(rows,a,t,n):
    pr=[x for x in rows if x['D_sum']<=a and x['PPC_tail']<=t and x['PPC_nonlinear']<=n]
    if not pr:
        return {'a':a,'t':t,'n':n,'n_promoted':0,'coverage':0.0,'mean_edge_delta':None,'mean_brier_delta':None,'large_harms':0,'wins':0,'qualifies':False}
    cov=len(pr)/len(rows); edge=float(np.mean([x['edge_delta'] for x in pr])); br=float(np.mean([x['brier_delta'] for x in pr])); harms=sum(x['large_harm'] for x in pr)
    return {'a':a,'t':t,'n':n,'n_promoted':len(pr),'coverage':cov,'mean_edge_delta':edge,'mean_brier_delta':br,'large_harms':harms,'wins':sum(x['edge_delta']<0 for x in pr),'qualifies':bool(cov>=.50 and edge<=-.10 and br<=.005 and harms<=2)}

def train(rows):
    grid=[eval_gate(rows,a,t,n) for a in A_GRID for t in T_GRID for n in N_GRID]
    q=[g for g in grid if g['qualifies']]
    selected=sorted(q,key=lambda g:(-g['coverage'],g['mean_brier_delta'],g['mean_edge_delta'],g['a'],g['t'],g['n']))[0] if q else None
    return grid,selected

def summarize(rows,gate):
    pr=[x for x in rows if x['D_sum']<=gate['a'] and x['PPC_tail']<=gate['t'] and x['PPC_nonlinear']<=gate['n']]
    return {'n_total':len(rows),'n_promoted':len(pr),'coverage':len(pr)/len(rows) if rows else 0.0,'mean_edge_delta_promoted':float(np.mean([x['edge_delta'] for x in pr])) if pr else None,'mean_brier_delta_promoted':float(np.mean([x['brier_delta'] for x in pr])) if pr else None,'wins_promoted':sum(x['edge_delta']<0 for x in pr),'large_harms_promoted':sum(x['large_harm'] for x in pr),'trace_identical_all':all(x['trace_identical'] for x in rows),'max_spend':max([x['spend'] for x in rows],default=0),'all_finite_normalized':all(np.isfinite(x['posterior_sum_control']) and np.isfinite(x['posterior_sum_science']) and abs(x['posterior_sum_control']-1)<1e-8 and abs(x['posterior_sum_science']-1)<1e-8 for x in rows)}

def bootstrap_edge(rows,gate,reps=10000,seed=21919):
    pr=[x for x in rows if x['D_sum']<=gate['a'] and x['PPC_tail']<=gate['t'] and x['PPC_nonlinear']<=gate['n']]
    if not pr:return None
    x=np.array([r['edge_delta'] for r in pr]); rr=np.random.default_rng(seed); means=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]

if __name__=='__main__':
    import sys
    args=sys.argv[1:]
    mode='rows'
    if args and args[0] in ('train','rows'):
        mode=args.pop(0)
    rows=[paired(int(s)) for s in args]
    if mode=='train':
        grid,selected=train(rows); print(json.dumps({'rows':rows,'grid':grid,'selected_gate':selected},separators=(',',':')))
    else:
        print(json.dumps(rows,separators=(',',':')))
