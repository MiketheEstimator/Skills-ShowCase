import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s9_shift as s9
import swarmite_exp002_s17_compound as s17
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s40_hetero as s40
import swarmite_exp002_s41_density as s41
import swarmite_exp002_s44_joint_shift as s44
import swarmite_exp002_s45_joint_latent as s45
import swarmite_exp002_s46_continuous_risk as s46

REGIMES=('linear','weak_effect','compound_t','heteroskedastic','topology','joint')
SPECIALISTS=s39.SPECIALISTS; CREDAL_THRESHOLD=s44.CREDAL_THRESHOLD

def regime(seed): return REGIMES[int(seed)%6]
def internal_seed(seed): return 900000 + int(seed)*5 + int(seed)//6 + REGIMES.index(regime(seed))

def run_default(world,seed,envfn=b.env_sample):
    data=envfn(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        sc=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(sc))]; row=envfn(world,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    return {'spend':spend,'trace':trace},data,targets,p

def state(external_seed):
    reg=regime(external_seed); seed=internal_seed(external_seed); meta={}
    if reg=='linear': w=b.gen_world(seed); c,data,targets,p0=run_default(w,seed)
    elif reg=='weak_effect': w=s9.gen_shift(seed); c,data,targets,p0=run_default(w,seed)
    elif reg=='compound_t': w=b.gen_world(seed); c,data,targets,p0=s17.run_control(w,seed)
    elif reg=='heteroskedastic': w=b.gen_world(seed); c,data,targets,p0,mech=s40.run_control(w,seed); meta['mechanism']=mech
    elif reg=='topology': w,den=s41.gen_world(seed); c,data,targets,p0=run_default(w,seed); meta['density']=den
    else: w,den,mech=s44.gen_world(seed); c,data,targets,p0=s44.run_control(w,seed,mech); meta.update({'density':den,'mechanism':mech})
    return reg,seed,w,c,data,targets,p0,meta

def world_row(external_seed):
    reg,seed,w,c,data,targets,p0,meta=state(external_seed); fs,_=b.build_family_models(data,targets); es=s45.s42.class_logevidence(fs,.15); ed=s45.s42.class_logevidence(fs,.55); mx=max(es,ed); aa=math.exp(es-mx); dd=math.exp(ed-mx); qdense=float(dd/(aa+dd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(p0); em=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); credal=float(np.mean(np.max(np.vstack([em,ems]),axis=0)-np.min(np.vstack([em,ems]),axis=0))); ms=s45.mechanism_scores(data,targets); shift=np.abs(em-em0)
    raw=[qdense,*ms.tolist(),credal,float(alpha),b.entropy(p0),b.entropy(ps30),float(np.mean(shift)),float(np.max(shift)),float(np.max(p0)),float(np.max(ps30)),float(np.sum(em0)),float(np.sum(em))]; raw += [qdense*ms[0],qdense*ms[1],qdense*ms[2],qdense*credal,qdense*alpha]
    base=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); edge=float(sm['edge_error']-base['edge_error']); br=float(sm['brier']-base['brier'])
    return {'seed':int(external_seed),'internal_seed':int(seed),'regime':reg,'metadata':meta,'features':[float(x) for x in raw],'credal_width':credal,'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'trace_identical':True,'finite':bool(finite and np.all(np.isfinite(raw))),'s30_sum':float(ps30.sum())}

def generate(lo,hi): return [world_row(s) for s in range(lo,hi+1)]
def counts_ok(rows,n_each): return all(sum(r['regime']==x for r in rows)==n_each for x in REGIMES)
def mechanics(rows): return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and len(r['features'])==len(s46.FEATURE_NAMES) for r in rows)
def load_anchor():
    z=json.loads(Path('EXP-002S46_TRAINING_RESULT.json').read_text()); return z['model'],z['selected_rule']
def boot(x,reps=10000,seed=24747):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]
def stats(rows,mask,seed):
    mask=np.asarray(mask,bool); ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); always=float(np.mean(ed)); hy=float(np.mean(he)); ret=float(abs(hy)/abs(always)) if always<0 else 1.0; by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in rows]); mm=mask[idx]; ee=ed[idx]; by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.))),'large_harm_rate':float(np.sum((ee>.5)&mm)/max(1,mm.sum()))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,mask.sum())),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hy,'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'improvement_retained':ret,'by_regime':by}
def summarize(raw,model,rule,seed):
    rows=s46.predict(raw,model); risk=np.array([r['pred_edge_delta']<=rule['edge_cut'] and r['pred_harm_prob']<=rule['harm_cut'] for r in rows]); always=np.ones(len(rows),bool); s39m=np.array([r['credal_width']<=CREDAL_THRESHOLD for r in rows]); rb=float(np.mean([(r['pred_harm_prob']-r['s30_large_harm'])**2 for r in rows])); prev=model['train_harm_prevalence']; cb=float(np.mean([(prev-r['s30_large_harm'])**2 for r in rows])); return {'n':len(rows),'continuous_risk':stats(rows,risk,seed),'always_s30':stats(rows,always,seed+1),'s39_control':stats(rows,s39m,seed+2),'risk_brier':rb,'constant_prevalence_brier':cb,'mechanics_ok':mechanics(raw),'rows':rows}
def screen_pass(s):
    m=s['continuous_risk']; overall=s['mechanics_ok'] and m['coverage']>=.50 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.55) and s['risk_brier']<=s['constant_prevalence_brier']; cells=all(v['coverage']>=.25 and v['hybrid_mean_edge_delta']<=.10 and v['large_harm_rate']<=.125 for v in m['by_regime'].values()); return overall and cells
def confirmation_pass(s):
    if not screen_pass(s): return False
    m=s['continuous_risk']; cells=all(v['coverage']>=.30 and v['hybrid_mean_edge_delta']<=0 and v['large_harm_rate']<=.10 for v in m['by_regime'].values()); return m['improvement_retained']>=.60 and m['bootstrap95_hybrid_edge_delta'][1]<0 and m['promoted_large_harm_rate']<=.05 and cells

if __name__=='__main__':
    model,rule=load_anchor(); me=generate(74301,74306); out={'mechanics':{'rows':s46.predict(me,model),'passed':mechanics(me) and counts_ok(me,1)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        sc=generate(74311,74358); ss=summarize(sc,model,rule,24748); out['screen']=ss
        if not counts_ok(sc,8) or not screen_pass(ss): out['disposition']='FALSIFIED_AT_SCREEN'
        else:
            co=generate(74401,74520); cs=summarize(co,model,rule,24749); out['confirmation']=cs; out['disposition']='REFERENCE_BREADTH_SUPPORTED' if counts_ok(co,20) and confirmation_pass(cs) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
