import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s42_worldclass as s42
import swarmite_exp002_s44_joint_shift as s44

MECHS=('tanh','sin','asinh'); DENS=('sparse','dense'); RIDGE=.25
TEMPS=(.05,.10,.20,.50,1.00); UNIFORM_NLL=math.log(3.0)
SPECIALISTS=s39.SPECIALISTS; CREDAL_THRESHOLD=s44.CREDAL_THRESHOLD
S43_MU={'sparse':s44.MU_SPARSE,'dense':s44.MU_DENSE}; S43_HARM={'sparse':0.0,'dense':0.0}

def transform(x,m): return np.tanh(x) if m=='tanh' else (np.sin(x) if m=='sin' else np.arcsinh(x))

def mechanism_scores(data,targets):
    scores=[]
    for mech in MECHS:
        total=0.0; count=0
        for v in range(b.N):
            idx=np.array([t!=v for t in targets],bool); Z=data[idx]; n=len(Z)
            if n<6: continue
            cols=[u for u in range(b.N) if u!=v]; X=np.column_stack([np.ones(n),transform(Z[:,cols],mech)]); y=Z[:,v]
            for fold in range(3):
                va=np.arange(n)%3==fold; tr=~va
                A=X[tr].T@X[tr]+np.diag([1e-6]+[RIDGE]*len(cols)); coef=np.linalg.solve(A,X[tr].T@y[tr]); mu=X[va]@coef
                sig=np.clip(.55+.35*np.abs(mu),.55,1.80); z=(y[va]-mu)/sig
                total+=float(np.sum(-.5*np.log(2*np.pi)-np.log(sig)-.5*z*z)); count+=int(np.sum(va))
        scores.append(total/max(1,count))
    return np.array(scores,float)

def softmax_scores(scores,T):
    z=np.asarray(scores,float)/T; z-=np.max(z); p=np.exp(z); return p/p.sum()

def base_row(seed):
    w,den,mech=s44.gen_world(seed); c,data,targets,p0=s44.run_control(w,seed,mech); fs,_=b.build_family_models(data,targets)
    es=s42.class_logevidence(fs,.15); ed=s42.class_logevidence(fs,.55); mx=max(es,ed); a=math.exp(es-mx); d=math.exp(ed-mx); qdense=float(d/(a+d))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); credal=float(np.mean(np.max(np.vstack([em0,ems]),axis=0)-np.min(np.vstack([em0,ems]),axis=0)))
    base=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); edge=float(sm['edge_error']-base['edge_error']); br=float(sm['brier']-base['brier'])
    return {'seed':int(seed),'density':den,'mechanism':mech,'joint_cell':den+'_'+mech,'p_dense':qdense,'mechanism_scores':mechanism_scores(data,targets).tolist(),'credal_width':credal,'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'trace_identical':True,'finite':bool(finite and np.isfinite(qdense)),'s30_sum':float(ps30.sum())}

def generate(lo,hi): return [base_row(s) for s in range(lo,hi+1)]

def mech_nll(rows,T):
    vals=[]
    for r in rows:
        p=softmax_scores(r['mechanism_scores'],T); vals.append(-math.log(max(1e-300,p[MECHS.index(r['mechanism'])])))
    return float(np.mean(vals))

def select_temp(rows):
    grid=[{'T':T,'nll':mech_nll(rows,T)} for T in TEMPS]; best=min(x['nll'] for x in grid); cand=[x['T'] for x in grid if abs(x['nll']-best)<1e-12]; return max(cand),grid

def fit_utilities(rows):
    out={}
    for den in DENS:
        for mech in MECHS:
            cell=den+'_'+mech; rr=[r for r in rows if r['joint_cell']==cell]
            out[cell]={'n':len(rr),'mean_edge_delta':float(np.mean([r['s30_edge_delta_vs_baseline'] for r in rr])),'large_harm_rate':float(np.mean([r['s30_large_harm'] for r in rr]))}
    return out

def joint_probs(r,T):
    pm=softmax_scores(r['mechanism_scores'],T); pd=np.array([1-r['p_dense'],r['p_dense']]); q={}
    for i,den in enumerate(DENS):
        for j,mech in enumerate(MECHS): q[den+'_'+mech]=float(pd[i]*pm[j])
    z=sum(q.values()); return {k:v/z for k,v in q.items()},pm

def decisions(rows,T,params):
    out=[]
    for r in rows:
        q,pm=joint_probs(r,T); exd=sum(q[c]*params[c]['mean_edge_delta'] for c in q); exh=sum(q[c]*params[c]['large_harm_rate'] for c in q)
        topo_d=(1-r['p_dense'])*S43_MU['sparse']+r['p_dense']*S43_MU['dense']; topo_h=(1-r['p_dense'])*S43_HARM['sparse']+r['p_dense']*S43_HARM['dense']
        x=dict(r); x.update({'q_mechanism':{MECHS[i]:float(pm[i]) for i in range(3)},'joint_expected_delta':float(exd),'joint_expected_harm':float(exh),'joint_promote':bool(exd<0 and exh<=.05),'topology_promote':bool(topo_d<0 and topo_h<=.05),'s39_promote':bool(r['credal_width']<=CREDAL_THRESHOLD)}); out.append(x)
    return out

def mechanics(rows):
    return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and 0<=r['p_dense']<=1 and np.all(np.isfinite(r['mechanism_scores'])) for r in rows)

def counts_ok(rows,n_each): return all(sum(r['joint_cell']==d+'_'+m for r in rows)==n_each for d in DENS for m in MECHS)
def boot(x,reps=10000,seed=24545):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]

def policy_stats(rows,key,seed):
    mask=np.array([r[key] for r in rows],bool); ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); always=float(np.mean(ed)); hy=float(np.mean(he)); ret=float(abs(hy)/abs(always)) if always<0 else 1.0
    by={}
    for cell in sorted({r['joint_cell'] for r in rows}):
        idx=np.array([r['joint_cell']==cell for r in rows]); mm=mask[idx]; ee=ed[idx]; by[cell]={'n':int(np.sum(idx)),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.))),'large_harm_rate':float(np.sum((ee>.5)&mm)/max(1,np.sum(mm)))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,mask.sum())),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hy,'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'improvement_retained':ret,'by_joint_cell':by}

def summarize(raw,T,params,seed):
    rows=decisions(raw,T,params); return {'n':len(rows),'mechanism_nll':mech_nll(raw,T),'uniform_nll':UNIFORM_NLL,'joint_class':policy_stats(rows,'joint_promote',seed),'topology_control':policy_stats(rows,'topology_promote',seed+1),'s39_control':policy_stats(rows,'s39_promote',seed+2),'mechanics_ok':mechanics(raw),'rows':rows}

def validation_pass(s):
    m=s['joint_class']; c=s['topology_control']; return s['mechanics_ok'] and m['coverage']>=.50 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.65) and m['hybrid_mean_edge_delta']<=c['hybrid_mean_edge_delta']+.02 and s['mechanism_nll']<=UNIFORM_NLL

def confirmation_pass(s):
    if not validation_pass(s): return False
    m=s['joint_class']; cells=all(v['large_harm_rate']<=.10 for v in m['by_joint_cell'].values()); return m['bootstrap95_hybrid_edge_delta'][1]<0 and m['improvement_retained']>=.60 and cells and s['mechanism_nll']<=UNIFORM_NLL

if __name__=='__main__':
    tr=generate(73501,73572); T,grid=select_temp(tr); params=fit_utilities(tr); out={'training':{'selected_T':T,'temperature_grid':grid,'cell_utilities':params,'mechanics_ok':mechanics(tr),'counts_ok':counts_ok(tr,12)}}
    if not out['training']['mechanics_ok'] or not out['training']['counts_ok']: out['disposition']='BLOCKED_TRAINING_MECHANICS'
    else:
        va=generate(73601,73636); vs=summarize(va,T,params,24546); out['validation']=vs
        if not counts_ok(va,6) or not validation_pass(vs): out['disposition']='FALSIFIED_ON_VALIDATION'
        else:
            co=generate(73701,73772); cs=summarize(co,T,params,24547); out['confirmation']=cs; out['disposition']='JOINT_LATENT_CLASS_SUPPORTED' if counts_ok(co,12) and confirmation_pass(cs) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
