import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s64_constrained_local_posterior_projection as s64
import swarmite_exp002_s66_evidence_guided_intervention_allocation as s66
import swarmite_exp002_s67_intervention_response_disagreement as s67

REGIMES=('linear','heteroskedastic'); BRANCHES=8

def seeds(start,n):
    out=[]
    for rg in REGIMES: out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out

def rows(start,n): return [s64.world_base(x) for x in seeds(start,n)]

def mechanics(a,n): return len(a)==2*n and all(sum(r['regime']==rg for r in a)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in a)

def entropy(p):
    p=np.asarray(p,float); p=p[p>0]
    return float(-np.sum(p*np.log(p)))

def branch_scores(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); h0=entropy(p); out=[]
    for target in range(b.N):
        vals=[]
        for spi,sp in enumerate((-2.0,2.0)):
            rr=b.rng_for('s68','branch-voi',seed,target,spi)
            for _ in range(BRANCHES):
                row=b.sim_row_from_posterior(p,models,target,sp,rr); q=b.update_p_with_row(p,models,row,target)
                if not np.isfinite(q).all() or abs(float(np.sum(q))-1)>1e-8: return None
                immediate=max(0.0,h0-entropy(q))/float(b.COSTS[target])
                # Preserve the branch and estimate best second action from the updated posterior.
                best2=0.0
                for t2 in range(b.N):
                    if b.COSTS[target]+b.COSTS[t2]>15: continue
                    hs=[]
                    rr2=b.rng_for('s68','second',seed,target,spi,t2,_)
                    for sp2 in (-2.0,2.0):
                        row2=b.sim_row_from_posterior(q,models,t2,sp2,rr2); q2=b.update_p_with_row(q,models,row2,t2)
                        hs.append(entropy(q2))
                    gain=max(0.0,entropy(q)-float(np.mean(hs)))/float(b.COSTS[t2])
                    best2=max(best2,gain)
                vals.append(immediate+best2)
        out.append(float(np.mean(vals)))
    return np.asarray(out,float)

def evaluate(a):
    sc=[]; vals=[]; cv=[]; dv=[]; wins=[]; finite=True; by={r:{'candidate':[],'eig':[]} for r in REGIMES}
    for r in a:
        s=branch_scores(r['external_seed']); av=s66.acquisition_values(r['external_seed'],r)
        if s is None or av is None: finite=False; continue
        av=np.asarray(av,float); sc.extend(s.tolist()); vals.extend(av.tolist()); dt=int(np.argmax(s)); ct=s66.eig_target(r['external_seed']); d=float(av[dt]); c=float(av[ct]); dv.append(d); cv.append(c); wins.append(d>c); by[r['regime']]['candidate'].append(d); by[r['regime']]['eig'].append(c)
    auc=s60.auc(np.asarray(vals)>0,np.asarray(sc)); rho=s67.spearman(sc,vals); br={}
    for rg in REGIMES:
        d=np.asarray(by[rg]['candidate']); c=np.asarray(by[rg]['eig']); br[rg]={'n':len(d),'candidate_mean_value_per_cost':float(np.mean(d)),'eig_mean_value_per_cost':float(np.mean(c)),'paired_difference':float(np.mean(d-c))}
    return {'n_worlds':len(a),'finite':finite,'positive_value_auc':auc,'spearman_score_vs_value':rho,'candidate_mean_value_per_cost':float(np.mean(dv)),'eig_mean_value_per_cost':float(np.mean(cv)),'paired_mean_difference':float(np.mean(np.asarray(dv)-np.asarray(cv))),'candidate_beats_eig_fraction':float(np.mean(wins)),'by_regime':br}

def disposition(e):
    if not e['finite'] or e['positive_value_auc'] is None: return 'BLOCKED_EXECUTION_NONFINITE'
    rok=all(v['paired_difference']>=-.02 for v in e['by_regime'].values())
    if e['positive_value_auc']>=.60 and e['spearman_score_vs_value']>=.10 and e['candidate_mean_value_per_cost']>=e['eig_mean_value_per_cost'] and rok: return 'BRANCH_VOI_ALIGNED'
    if e['positive_value_auc']>=.56: return 'BRANCH_VOI_WEAK'
    return 'BRANCH_VOI_FALSIFIED'

if __name__=='__main__':
    me=rows(110201,2); out={'mechanics':{'passed':mechanics(me,2)},'branches_per_setpoint':BRANCHES}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        ev=evaluate(rows(110401,64)); out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))