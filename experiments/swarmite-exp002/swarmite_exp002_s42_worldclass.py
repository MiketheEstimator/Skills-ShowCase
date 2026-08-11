import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s32_modelset_diag as s32
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s41_density as s41

SPECIALISTS=s39.SPECIALISTS
EDGECOUNTS=np.array([int(x).bit_count() for x in b.dags],float)

def logsumexp(x):
    m=float(np.max(x)); return m+math.log(float(np.exp(x-m).sum()))

def auc(y,s):
    y=np.asarray(y,int); s=np.asarray(s,float); pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
    if not len(pos) or not len(neg): return float('nan')
    wins=0.0
    for i in pos:
        for j in neg:
            wins += 1.0 if s[i]>s[j] else (0.5 if s[i]==s[j] else 0.0)
    return float(wins/(len(pos)*len(neg)))

def class_logevidence(fs,p):
    ll=np.zeros(len(b.dags))
    for v in range(b.N): ll += fs[v,b.parents[:,v]]
    lp=EDGECOUNTS*math.log(p)+(10-EDGECOUNTS)*math.log(1-p)
    return logsumexp(ll+lp)

def row(seed):
    w,den=s41.gen_world(seed); c,data,targets,p0,cell=s32.run_control(w,seed); fs,_=b.build_family_models(data,targets)
    es=class_logevidence(fs,.15); ed=class_logevidence(fs,.55); m=max(es,ed); qs=math.exp(es-m); qd=math.exp(ed-m); qdense=float(qd/(qs+qd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); allm=np.vstack([em0,ems]); widths=np.max(allm,axis=0)-np.min(allm,axis=0); credal=float(np.mean(widths))
    return {'seed':int(seed),'density':den,'truth_dense':int(den=='dense'),'cell':cell,'p_dense':qdense,'credal_width':credal,'spend':int(c['spend']),'finite':bool(finite and np.isfinite(es) and np.isfinite(ed) and np.isfinite(qdense)),'s30_sum':float(ps30.sum()),'dag_count':len(b.dags)}

def summarize(rows):
    y=np.array([r['truth_dense'] for r in rows],int); q=np.array([r['p_dense'] for r in rows],float); cw=np.array([r['credal_width'] for r in rows],float)
    a=auc(y,q); ac=auc(y,cw); br=float(np.mean((q-y)**2)); acc=float(np.mean((q>=.5)==y)); mech=all(r['spend']<=15 and r['finite'] and abs(r['s30_sum']-1)<1e-8 and r['dag_count']==29281 and 0<=r['p_dense']<=1 for r in rows)
    return {'n':len(rows),'auc_worldclass':a,'auc_credal_control':ac,'auc_gain':float(a-ac),'brier':br,'accuracy':acc,'mean_p_dense_sparse':float(np.mean(q[y==0])),'mean_p_dense_dense':float(np.mean(q[y==1])),'mechanics_ok':mech}

def run():
    tr=[row(s) for s in range(72901,72949)]; ts=summarize(tr); out={'training':ts}
    if not ts['mechanics_ok']: out['disposition']='BLOCKED_MECHANICS'; return out
    va=[row(s) for s in range(72961,73009)]; vs=summarize(va); out['validation']=vs
    ok=vs['mechanics_ok'] and vs['auc_worldclass']>=.75 and vs['brier']<=.20 and vs['accuracy']>=.70 and vs['auc_gain']>=.10
    out['disposition']='TOPOLOGY_WORLDCLASS_SUPPORTED' if ok else 'FALSIFIED_ON_VALIDATION'; return out
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
