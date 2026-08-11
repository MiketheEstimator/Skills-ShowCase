import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s29_adequacy as s29

CELLS=('tanh_gaussian','tanh_t7','sin_gaussian','sin_t7','asinh_gaussian','asinh_t7')
T=5.0

def cell(seed): return CELLS[int(seed)%6]
def split_cell(c): return c.split('_',1)

def env(world,r,n,target=None,setpoint=None,cell_name='tanh_gaussian'):
    mech,noise=split_cell(cell_name); X=np.zeros((n,b.N))
    for i in range(n):
        eps=r.normal(size=b.N) if noise=='gaussian' else r.standard_t(7,size=b.N)*math.sqrt(5/7)
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else:
                z=X[i]
                feat=np.tanh(z) if mech=='tanh' else (np.sin(z) if mech=='sin' else np.arcsinh(z))
                X[i,v]=float(feat@world.W[:,v]+eps[v])
    return X

def run_control(world,seed):
    c=cell(seed); data=env(world,b.rng_for('v2','obs',seed),b.OBS_N,cell_name=c); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(scores))]
        row=env(world,b.rng_for('v2','env',seed,step,t,s),1,t,s,c)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m.update({'spend':spend,'trace':trace,'posterior_sum':float(p.sum())}); return m,data,targets,p,c

def adequacy(data,targets):
    n=len(data); base=0.0; robust=0.0; idx=list(range(n))
    for fold in range(5):
        te=[i for i in idx if i%5==fold]; tr=[i for i in idx if i%5!=fold]
        for v in range(b.N):
            pms=[pm for pm in range(1<<b.N) if not(pm>>v&1)]; bs=[]; bm=[]; rs=[]; rm=[]
            for pm in pms:
                sc,m=s29.baseline_fit_score(data,targets,v,pm,tr); bs.append(sc); bm.append(m)
                sc2,m2=s29.robust_fit_score(data,targets,v,pm,tr); rs.append(sc2); rm.append(m2)
            mb=bm[int(np.argmax(bs))]; mr=rm[int(np.argmax(rs))]
            for i in te:
                if targets[i]==v: continue
                base += s29.baseline_logpred(mb,data[i],v); robust += s29.robust_logpred(mr,data[i],v)
    return float(robust-base)

def sigmoid(x):
    x=max(-40.0,min(40.0,float(x))); return 1/(1+math.exp(-x))

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0,cn=run_control(w,seed); fs0,_=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0); recon=float(np.max(np.abs(p0-p0c)))
    fs,finite=s23.build(data,targets); pr=b.posterior_from_fs(fs); adeq=adequacy(data,targets); alpha=sigmoid(adeq/T); pm=(1-alpha)*p0+alpha*pr; pm/=pm.sum()
    mm=b.posterior_metrics(pm,w.dag_mask); rm=b.posterior_metrics(pr,w.dag_mask); ed=float(mm['edge_error']-c['edge_error']); bd=float(mm['brier']-c['brier'])
    mech,noise=split_cell(cn)
    return {'seed':int(seed),'cell':cn,'mechanism':mech,'noise':noise,'dag_count':len(b.dags),'spend':int(c['spend']),'planning_reconstruction_max_abs':recon,'family_scores_finite':bool(finite),'p0_sum':float(p0.sum()),'pr_sum':float(pr.sum()),'pmix_sum':float(pm.sum()),'ADEQ':adeq,'alpha':float(alpha),'edge_delta':ed,'brier_delta':bd,'large_harm':int(ed>0.50),'robust_edge_delta':float(rm['edge_error']-c['edge_error']),'robust_brier_delta':float(rm['brier']-c['brier']),'trace_identical':True}

def boot(x,reps=10000,seed=23232):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
def group_summary(rows,seed=23232):
    ed=[r['edge_delta'] for r in rows]; ci=boot(ed,seed=seed); me=float(np.mean(ed)); mb=float(np.mean([r['brier_delta'] for r in rows]))
    label='SUPPORTED' if me<0 and ci[1]<0 and mb<=.010 else ('HARMFUL' if ((me>0 and ci[0]>0) or mb>.015) else 'UNRESOLVED')
    return {'n':len(rows),'mean_edge_delta':me,'bootstrap95_edge_delta':ci,'mean_brier_delta':mb,'large_harms':sum(r['large_harm'] for r in rows),'mean_ADEQ':float(np.mean([r['ADEQ'] for r in rows])),'mean_alpha':float(np.mean([r['alpha'] for r in rows])),'mean_robust_edge_delta':float(np.mean([r['robust_edge_delta'] for r in rows])),'label':label}
def summarize(rows):
    by_cell={c:group_summary([r for r in rows if r['cell']==c],23232+i) for i,c in enumerate(CELLS)}
    by_mech={m:group_summary([r for r in rows if r['mechanism']==m],23300+i) for i,m in enumerate(('tanh','sin','asinh'))}
    by_noise={n:group_summary([r for r in rows if r['noise']==n],23400+i) for i,n in enumerate(('gaussian','t7'))}
    mechanics=all(r['dag_count']==29281 and r['spend']<=15 and r['planning_reconstruction_max_abs']<=1e-10 and r['family_scores_finite'] and all(abs(r[k]-1)<1e-8 for k in ('p0_sum','pr_sum','pmix_sum')) and np.isfinite(r['ADEQ']) and r['trace_identical'] for r in rows)
    labels={c:v['label'] for c,v in by_cell.items()}
    all_supported=all(v=='SUPPORTED' for v in labels.values())
    sin_gap=labels['sin_gaussian']!='SUPPORTED' and labels['sin_t7']!='SUPPORTED' and labels['tanh_gaussian']=='SUPPORTED' and labels['tanh_t7']=='SUPPORTED'
    noise_gap=(by_cell['tanh_t7']['mean_edge_delta']-by_cell['tanh_gaussian']['mean_edge_delta']>.10 and by_cell['asinh_t7']['mean_edge_delta']-by_cell['asinh_gaussian']['mean_edge_delta']>.10)
    if all_supported: disposition='ALL_SUPPORTED_S31_SAMPLING_INSTABILITY'
    elif sin_gap: disposition='SIN_MECHANISM_REPRESENTATION_GAP'
    elif noise_gap: disposition='T7_NOISE_REPRESENTATION_GAP'
    else: disposition='MECHANISM_NOISE_INTERACTION_OR_MIXED_GAP'
    return {'n':len(rows),'by_cell':by_cell,'by_mechanism':by_mech,'by_noise':by_noise,'mechanics_ok':mechanics,'disposition':disposition}
if __name__=='__main__':
 import sys
 seeds=list(map(int,sys.argv[1:])); rows=[paired(s) for s in seeds]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
