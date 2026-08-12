import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s45_joint_latent as s45
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47

SPECIALISTS=s39.SPECIALISTS
REGIMES=('linear','heteroskedastic')

def selected_external_seeds(start, regime, n):
    out=[]; s=int(start)
    while len(out)<n:
        if s47.regime(s)==regime: out.append(s)
        s+=1
    return out

def hetero_score(data,targets,p0):
    fs,models=b.build_family_models(data,targets); gi=int(np.argmax(p0)); vals=[]
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]
        pm=int(b.parents[gi,v]); cols,mu,_=models[(v,pm)]
        X=data[keep][:,cols] if cols else np.empty((len(y),0)); Xd=np.column_stack([np.ones(len(y)),X]); pred=Xd@mu
        if len(y)<8: continue
        mag=np.abs(pred-np.median(pred)); r2=(y-pred)**2; med=float(np.median(mag)); hi=mag>=med; lo=~hi
        if hi.sum()<3 or lo.sum()<3: continue
        vr=math.log((float(np.mean(r2[hi]))+1e-8)/(float(np.mean(r2[lo]))+1e-8))
        if np.std(mag)>1e-12 and np.std(r2)>1e-12: cor=float(np.corrcoef(mag,r2)[0,1])
        else: cor=0.0
        vals.append(max(0.0,vr)+max(0.0,cor))
    return float(max(vals) if vals else 0.0)

def world_row(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    fs,_=b.build_family_models(data,targets); es=s45.s42.class_logevidence(fs,.15); ed=s45.s42.class_logevidence(fs,.55); mx=max(es,ed); aa=math.exp(es-mx); dd=math.exp(ed-mx); qdense=float(dd/(aa+dd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(p0); em=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); credal=float(np.mean(np.max(np.vstack([em,ems]),axis=0)-np.min(np.vstack([em,ems]),axis=0))); ms=s45.mechanism_scores(data,targets); shift=np.abs(em-em0)
    raw=[qdense,*ms.tolist(),credal,float(alpha),b.entropy(p0),b.entropy(ps30),float(np.mean(shift)),float(np.max(shift)),float(np.max(p0)),float(np.max(ps30)),float(np.sum(em0)),float(np.sum(em))]; raw += [qdense*ms[0],qdense*ms[1],qdense*ms[2],qdense*credal,qdense*alpha]
    base=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); edge=float(sm['edge_error']-base['edge_error']); br=float(sm['brier']-base['brier']); hs=hetero_score(data,targets,p0)
    return {'seed':int(external_seed),'internal_seed':int(seed),'regime':reg,'features':[float(x) for x in raw],'hetero_score':hs,'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'trace_identical':True,'finite':bool(finite and np.all(np.isfinite(raw)) and np.isfinite(hs)),'s30_sum':float(ps30.sum())}

def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]

def mechanics(rows,n_each):
    return all(sum(r['regime']==x for r in rows)==n_each for x in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and len(r['features'])==len(s46.FEATURE_NAMES) for r in rows)

def load_anchor():
    z=json.loads(Path('EXP-002S46_TRAINING_RESULT.json').read_text()); return z['model'],z['selected_rule']

def predict(rows,model): return s46.predict(rows,model)

def masks(rows,model,rule,repair=None):
    pr=predict(rows,model); base=np.array([r['pred_edge_delta']<=rule['edge_cut'] and r['pred_harm_prob']<=rule['harm_cut'] for r in pr],bool)
    if repair is None: return base,pr
    out=base.copy()
    for i,r in enumerate(pr):
        if not out[i]: continue
        if rows[i]['hetero_score']>=repair['hetero_threshold']:
            out[i]=bool(r['pred_edge_delta']<=-0.10 and r['pred_harm_prob']<=repair['tight_harm_cut'])
    return out,pr

def boot(x,reps=10000,seed=24848):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]

def stats(rows,mask,seed):
    ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows],float); mask=np.asarray(mask,bool); he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in rows]); mm=mask[idx]; ee=ed[idx]; by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(mm)),'hybrid_mean_edge_delta':float(np.mean(np.where(mm,ee,0.))),'large_harm_rate':float(np.sum((ee>.5)&mm)/max(1,mm.sum()))}
    return {'coverage':float(np.mean(mask)),'n_promoted':int(mask.sum()),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,mask.sum())),'hybrid_mean_edge_delta':float(np.mean(he)),'bootstrap95_hybrid_edge_delta':boot(he,seed=seed),'hybrid_mean_brier_delta':float(np.mean(hb)),'by_regime':by}

def evaluate(rows,model,rule,repair,seed):
    bm,_=masks(rows,model,rule,None); rm,pr=masks(rows,model,rule,repair); bs=stats(rows,bm,seed+1); rs=stats(rows,rm,seed+2); retained=(abs(rs['hybrid_mean_edge_delta'])/abs(bs['hybrid_mean_edge_delta'])) if bs['hybrid_mean_edge_delta']<0 else 1.0
    return {'repair':rs,'frozen_s46':bs,'improvement_retained_vs_s46':float(retained),'mechanics_ok':all(r['finite'] for r in rows),'rows':[dict(r,pred_edge_delta=float(p['pred_edge_delta']),pred_harm_prob=float(p['pred_harm_prob']),base_promote=bool(bm[i]),repair_promote=bool(rm[i])) for i,(r,p) in enumerate(zip(rows,pr))]}

def qualifies(ev,confirmation=False):
    m=ev['repair']; b=ev['frozen_s46']; lin=m['by_regime']['linear']; het=m['by_regime']['heteroskedastic']; lin_base=b['by_regime']['linear']; ok=ev['mechanics_ok'] and m['coverage']>=.50 and het['coverage']>=.40 and m['promoted_large_harm_rate']<=.05 and het['large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and lin['hybrid_mean_edge_delta']<0.02 and het['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and ev['improvement_retained_vs_s46']>=.65 and lin['hybrid_mean_edge_delta']-lin_base['hybrid_mean_edge_delta']<=.02
    if confirmation: ok=ok and m['bootstrap95_hybrid_edge_delta'][1]<0
    return bool(ok)

def train(rows,model,rule):
    hs=np.array([r['hetero_score'] for r in rows]); qs=[.50,.65,.80,.90]; grid=[]
    for q in qs:
        th=float(np.quantile(hs,q))
        for hc in (.05,.10):
            rep={'hetero_threshold':th,'tight_harm_cut':hc,'quantile':q}; ev=evaluate(rows,model,rule,rep,24850); grid.append({'repair':rep,'summary':{k:v for k,v in ev.items() if k!='rows'},'qualifies':qualifies(ev)})
    good=[g for g in grid if g['qualifies']]
    if not good: return None,grid
    good.sort(key=lambda g:(-g['summary']['improvement_retained_vs_s46'],g['repair']['hetero_threshold'],g['repair']['tight_harm_cut']))
    return good[0]['repair'],grid

if __name__=='__main__':
    model,rule=load_anchor(); tr=generate(74601,48); rep,grid=train(tr,model,rule); out={'training':{'selected_repair':rep,'grid':grid,'mechanics_ok':mechanics(tr,48)}}
    if rep is None or not mechanics(tr,48): out['disposition']='FALSIFIED_AT_TRAINING' if rep is None else 'BLOCKED_MECHANICS'
    else:
        va=generate(75001,24); ve=evaluate(va,model,rule,rep,24851); out['validation']={k:v for k,v in ve.items() if k!='rows'}
        if not mechanics(va,24) or not qualifies(ve): out['disposition']='FALSIFIED_ON_VALIDATION'
        else:
            co=generate(75401,48); ce=evaluate(co,model,rule,rep,24852); out['confirmation']={k:v for k,v in ce.items() if k!='rows'}; out['disposition']='TARGETED_HETEROSKEDASTIC_REPAIR_SUPPORTED' if mechanics(co,48) and qualifies(ce,True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
