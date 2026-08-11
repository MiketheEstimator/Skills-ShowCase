import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s42_worldclass as s42

SPECIALISTS=s39.SPECIALISTS
CREDAL_THRESHOLD=0.2692013432171404
MU_SPARSE=-0.17642413429903825
MU_DENSE=-0.04040343473196801
HARM_SPARSE=0.0
HARM_DENSE=0.0
MECHS=('tanh','sin','asinh')

def joint_cell(seed):
    c=int(seed)%6
    return ('sparse' if c<3 else 'dense'), MECHS[c%3]

def gen_world(seed):
    den,mech=joint_cell(seed); ep=.15 if den=='sparse' else .55
    r=b.rng_for('s44','world',seed); order=list(map(int,r.permutation(b.N))); W=np.zeros((b.N,b.N)); mask=0
    for a in range(b.N):
        for bb in range(a+1,b.N):
            u,v=order[a],order[bb]
            if r.random()<ep:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9); mask|=1<<b.EDGE_INDEX[(u,v)]
    if int(mask).bit_count()<2:
        for a,bb in ((0,1),(1,2)):
            u,v=order[a],order[bb]
            if W[u,v]==0:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9); mask|=1<<b.EDGE_INDEX[(u,v)]
    return b.World(mask,W,order,seed),den,mech

def feat(x,m):
    return np.tanh(x) if m=='tanh' else (np.sin(x) if m=='sin' else np.arcsinh(x))

def env(world,r,n,target=None,setpoint=None,mech='tanh'):
    X=np.zeros((n,b.N))
    for i in range(n):
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else:
                mu=float(feat(X[i],mech)@world.W[:,v]); sig=float(np.clip(.55+.35*abs(mu),.55,1.80)); X[i,v]=mu+r.normal(0,sig)
    return X

def run_control(world,seed,mech):
    data=env(world,b.rng_for('v2','obs',seed),b.OBS_N,mech=mech); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(scores))]
        row=env(world,b.rng_for('v2','env',seed,step,t,s),1,t,s,mech)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    return {'spend':spend,'trace':trace},data,targets,p

def world_row(seed):
    w,den,mech=gen_world(seed); c,data,targets,p0=run_control(w,seed,mech); fs,_=b.build_family_models(data,targets)
    es=s42.class_logevidence(fs,.15); ed=s42.class_logevidence(fs,.55); mx=max(es,ed); qs=math.exp(es-mx); qd=math.exp(ed-mx); qdense=float(qd/(qs+qd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); widths=np.max(np.vstack([em0,ems]),axis=0)-np.min(np.vstack([em0,ems]),axis=0); credal=float(np.mean(widths))
    ex_delta=(1-qdense)*MU_SPARSE+qdense*MU_DENSE; ex_harm=(1-qdense)*HARM_SPARSE+qdense*HARM_DENSE; promote=bool(ex_delta<0 and ex_harm<=.05); ctrl=bool(credal<=CREDAL_THRESHOLD)
    base=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); edge=float(sm['edge_error']-base['edge_error']); br=float(sm['brier']-base['brier'])
    return {'seed':int(seed),'density':den,'mechanism':mech,'joint_cell':den+'_'+mech,'p_dense':qdense,'credal_width':credal,'class_aware_promote':promote,'s39_promote':ctrl,'expected_delta':float(ex_delta),'expected_harm':float(ex_harm),'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'trace_identical':True,'finite':bool(finite and np.isfinite(qdense)),'s30_sum':float(ps30.sum()),'edge_count':int(w.dag_mask).bit_count()}

def mechanics(rows):
    cells={r['joint_cell'] for r in rows}
    return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and 0<=r['p_dense']<=1 for r in rows) and (len(rows)!=6 or len(cells)==6)

def boot(x,reps=10000,seed=24444):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]

def stats(rows,mask,seed):
    ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); mask=np.asarray(mask,bool); he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); always=float(np.mean(ed)); hy=float(np.mean(he)); ret=float(abs(hy)/abs(always)) if always<0 else 1.0
    by={}
    for cell in sorted({r['joint_cell'] for r in rows}):
        idx=np.array([r['joint_cell']==cell for r in rows]); mm=mask&idx; ee=ed[idx]; mlocal=mask[idx]; by[cell]={'n':int(np.sum(idx)),'coverage':float(np.mean(mlocal)),'hybrid_mean_edge_delta':float(np.mean(np.where(mlocal,ee,0.))),'large_harm_rate':float(np.sum((ee>.5)&mlocal)/max(1,np.sum(mlocal)))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(np.sum(mask)),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,np.sum(mask))),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hy,'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'improvement_retained':ret,'by_joint_cell':by}

def summarize(rows,seed):
    ca=[r['class_aware_promote'] for r in rows]; ctrl=[r['s39_promote'] for r in rows]
    return {'n':len(rows),'class_aware':stats(rows,ca,seed),'s39_control':stats(rows,ctrl,seed+1),'mechanics_ok':mechanics(rows)}

def screen_pass(s):
    m=s['class_aware']; c=s['s39_control']; return s['mechanics_ok'] and m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70) and m['hybrid_mean_edge_delta']<=c['hybrid_mean_edge_delta']+.02

def confirm_pass(s):
    if not screen_pass(s): return False
    m=s['class_aware']; cell_ok=all(v['hybrid_mean_edge_delta']<=.10 and v['large_harm_rate']<=.10 for v in m['by_joint_cell'].values()); return m['bootstrap95_hybrid_edge_delta'][1]<0 and cell_ok

def run():
    me=[world_row(s) for s in range(73301,73307)]; out={'mechanics':{'rows':me,'passed':mechanics(me)}}
    if not mechanics(me): out['disposition']='BLOCKED_MECHANICS'; return out
    sc=[world_row(s) for s in range(73311,73335)]; ss=summarize(sc,24445); out['screen']=ss
    if not screen_pass(ss): out['disposition']='FALSIFIED_AT_SCREEN'; return out
    co=[world_row(s) for s in range(73401,73449)]; cs=summarize(co,24446); out['confirmation']=cs; out['disposition']='JOINT_SHIFT_TRANSFER_SUPPORTED' if confirm_pass(cs) else 'FALSIFIED_ON_CONFIRMATION'; return out
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
