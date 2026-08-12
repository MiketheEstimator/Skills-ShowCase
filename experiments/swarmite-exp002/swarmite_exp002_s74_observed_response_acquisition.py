import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s64_constrained_local_posterior_projection as s64
import swarmite_exp002_s66_evidence_guided_intervention_allocation as s66
import swarmite_exp002_s67_intervention_response_disagreement as s67

REGIMES=('linear','heteroskedastic'); LAM=2.0

def seeds(start,n):
    out=[]
    for rg in REGIMES: out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out

def rows(start,n): return [s64.world_base(x) for x in seeds(start,n)]
def mechanics(a,n): return len(a)==2*n and all(sum(r['regime']==rg for r in a)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in a)

def features(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed); x=np.asarray(data,float); t=np.asarray(targets,int); feats=[]
    for v in range(b.N):
        iv=(t==v); nv=~iv; ni=int(iv.sum()); nn=int(nv.sum()); f=[ni/float(max(1,len(t))), float(ni>0)]
        if ni and nn:
            mi=x[iv].mean(0); mn=x[nv].mean(0); vi=x[iv].var(0)+1e-6; vn=x[nv].var(0)+1e-6
            shift=(mi-mn)/np.sqrt(vn); vr=np.log(vi/vn)
            f += [float(shift[v]),float(abs(shift[v])),float(vr[v]),float(np.mean(np.abs(shift))),float(np.max(np.abs(shift))),float(np.mean(np.abs(vr)))]
        else: f += [0.0]*6
        f += [float(b.COSTS[v]),float(v)/max(1,b.N-1)]
        feats.append(f)
    return np.asarray(feats,float)

def fit(train):
    X=[]; y=[]
    for r in train:
        av=s66.acquisition_values(r['external_seed'],r)
        if av is None: continue
        X.append(features(r['external_seed'])); y.extend(av)
    X=np.vstack(X); y=np.asarray(y,float); mu=X.mean(0); sd=X.std(0); sd[sd<1e-8]=1.; Z=(X-mu)/sd; A=Z.T@Z+LAM*np.eye(Z.shape[1]); coef=np.linalg.solve(A,Z.T@y); intercept=float(y.mean()-((X.mean(0)-mu)/sd)@coef)
    return {'mu':mu.tolist(),'sd':sd.tolist(),'coef':coef.tolist(),'intercept':intercept}

def predict(seed,m):
    X=features(seed); mu=np.asarray(m['mu']); sd=np.asarray(m['sd']); co=np.asarray(m['coef']); return m['intercept']+(X-mu)/sd@co

def evaluate(a,m):
    sc=[]; vals=[]; dv=[]; cv=[]; wins=[]; finite=True; by={r:{'candidate':[],'eig':[]} for r in REGIMES}
    for r in a:
        s=predict(r['external_seed'],m); av=s66.acquisition_values(r['external_seed'],r)
        if av is None or not np.isfinite(s).all(): finite=False; continue
        av=np.asarray(av,float); sc.extend(s.tolist()); vals.extend(av.tolist()); dt=int(np.argmax(s)); ct=s66.eig_target(r['external_seed']); d=float(av[dt]); c=float(av[ct]); dv.append(d); cv.append(c); wins.append(d>c); by[r['regime']]['candidate'].append(d); by[r['regime']]['eig'].append(c)
    auc=s60.auc(np.asarray(vals)>0,np.asarray(sc)); rho=s67.spearman(sc,vals); br={}
    for rg in REGIMES:
        d=np.asarray(by[rg]['candidate']); c=np.asarray(by[rg]['eig']); br[rg]={'n':int(len(d)),'candidate_mean_value_per_cost':float(np.mean(d)),'eig_mean_value_per_cost':float(np.mean(c)),'paired_difference':float(np.mean(d-c))}
    return {'n_worlds':len(a),'finite':finite,'positive_value_auc':auc,'spearman_score_vs_value':rho,'candidate_mean_value_per_cost':float(np.mean(dv)),'eig_mean_value_per_cost':float(np.mean(cv)),'paired_mean_difference':float(np.mean(np.asarray(dv)-np.asarray(cv))),'candidate_beats_eig_fraction':float(np.mean(wins)),'by_regime':br}

def disposition(e):
    if not e['finite'] or e['positive_value_auc'] is None: return 'BLOCKED_EXECUTION_NONFINITE'
    rok=all(v['paired_difference']>=-.02 for v in e['by_regime'].values())
    if e['positive_value_auc']>=.60 and e['spearman_score_vs_value']>=.15 and e['candidate_mean_value_per_cost']>=e['eig_mean_value_per_cost'] and rok: return 'OBSERVED_RESPONSE_ACQUISITION_SUPPORTED'
    if e['positive_value_auc']>=.56 or e['spearman_score_vs_value']>=.10: return 'OBSERVED_RESPONSE_ACQUISITION_WEAK'
    return 'OBSERVED_RESPONSE_ACQUISITION_FALSIFIED'

if __name__=='__main__':
    me=rows(120201,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        tr=rows(120401,64); m=fit(tr); ev=evaluate(rows(121401,64),m); out['model']=m; out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))
