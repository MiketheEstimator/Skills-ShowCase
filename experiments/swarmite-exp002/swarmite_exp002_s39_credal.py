import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s35_stack as s35

SPECIALISTS=('TG','TT','SG','ST','AG','AT')
SCORES=('mean_credal_width','max_credal_width','mean_l1_from_s30')
QUANTILES=(0.50,0.60,0.70,0.80,0.90)

def edge_marginals(p): return b.edge_marginals(p)

def row(seed):
    r=s35.components(seed)
    s30p=(1-r['alpha'])*r['posts']['LG']+r['alpha']*r['posts']['TT']; s30p/=s30p.sum()
    em0=edge_marginals(s30p)
    ems=np.vstack([edge_marginals(r['posts'][n]) for n in SPECIALISTS])
    allm=np.vstack([em0,ems])
    widths=np.max(allm,axis=0)-np.min(allm,axis=0)
    scores={
      'mean_credal_width':float(np.mean(widths)),
      'max_credal_width':float(np.max(widths)),
      'mean_l1_from_s30':float(np.mean(np.abs(ems-em0)))
    }
    ed=float(r['s30']['edge_error']-r['base']['edge_error'])
    bd=float(r['s30']['brier']-r['base']['brier'])
    return {'seed':int(seed),'cell':r['cell'],'scores':scores,'s30_edge_delta_vs_baseline':ed,'s30_brier_delta_vs_baseline':bd,'s30_large_harm':int(ed>0.50),'spend':int(r['spend']),'trace_identical':bool(r['trace_identical']),'finite':bool(r['finite']),'s30_sum':float(s30p.sum())}

def boot(x,reps=10000,seed=23939):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]

def metrics(rows,score,thr):
    promote=np.array([r['scores'][score]<=thr for r in rows],bool)
    ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float)
    bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows],float)
    hybrid_ed=np.where(promote,ed,0.0); hybrid_bd=np.where(promote,bd,0.0)
    cov=float(np.mean(promote)); npr=int(np.sum(promote)); harms=int(np.sum((ed>0.50)&promote)); harm_rate=float(harms/max(1,npr))
    always=float(np.mean(ed)); hybrid=float(np.mean(hybrid_ed))
    retained=float(abs(hybrid)/abs(always)) if always<0 else 1.0
    return {'n':len(rows),'n_promoted':npr,'coverage':cov,'promoted_large_harms':harms,'promoted_large_harm_rate':harm_rate,'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hybrid,'bootstrap95_hybrid_edge_delta':boot(hybrid_ed,seed=23939+len(rows)),'hybrid_mean_brier_delta':float(np.mean(hybrid_bd)),'improvement_retained':retained}

def mechanics(rows):
    return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and all(np.isfinite(v) for v in r['scores'].values()) for r in rows)

def train(rows):
    candidates=[]; rank={s:i for i,s in enumerate(SCORES)}
    for s in SCORES:
        vals=np.array([r['scores'][s] for r in rows],float)
        for q in QUANTILES:
            thr=float(np.quantile(vals,q)); m=metrics(rows,s,thr)
            eligible=(m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70))
            candidates.append({'score':s,'quantile':q,'threshold':thr,'metrics':m,'eligible':eligible})
    elig=[c for c in candidates if c['eligible']]
    if not elig: return {'selected':None,'candidates':candidates,'disposition':'FALSIFIED_NO_ELIGIBLE_TRAINING_GATE'}
    elig.sort(key=lambda c:(c['metrics']['promoted_large_harms'],c['metrics']['hybrid_mean_edge_delta'],-c['metrics']['coverage'],rank[c['score']],c['threshold']))
    return {'selected':elig[0],'candidates':candidates,'disposition':'GATE_SELECTED'}

def validate(rows,selected):
    m=metrics(rows,selected['score'],selected['threshold'])
    passed=(m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70) and m['hybrid_mean_edge_delta']<=0 and mechanics(rows))
    return {'score':selected['score'],'threshold':selected['threshold'],'metrics':m,'mechanics_ok':mechanics(rows),'passed':passed}

def confirm(rows,selected):
    m=metrics(rows,selected['score'],selected['threshold']); ci=m['bootstrap95_hybrid_edge_delta']
    passed=(m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and ci[1]<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70) and mechanics(rows))
    return {'score':selected['score'],'threshold':selected['threshold'],'metrics':m,'mechanics_ok':mechanics(rows),'passed':passed}

def run():
    tr=[row(s) for s in range(72301,72349)]; tf=train(tr)
    out={'training':{'mechanics_ok':mechanics(tr),'fit':tf}}
    if tf['selected'] is None: out['disposition']='FALSIFIED_AT_TRAINING'; return out
    sel=tf['selected']; va=[row(s) for s in range(72361,72397)]; vv=validate(va,sel); out['validation']=vv
    if not vv['passed']: out['disposition']='FALSIFIED_ON_VALIDATION'; return out
    co=[row(s) for s in range(72401,72449)]; cc=confirm(co,sel); out['confirmation']=cc; out['disposition']='CREDAL_ABSTENTION_SUPPORTED' if cc['passed'] else 'FALSIFIED_ON_CONFIRMATION'; return out

if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
