import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s64_constrained_local_posterior_projection as s64
import swarmite_exp002_s66_evidence_guided_intervention_allocation as s66

REGIMES=('linear','heteroskedastic')
SIMS=12


def seeds(start,n):
    out=[]
    for rg in REGIMES:
        out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out


def generate_rows(start,n):
    return [s64.world_base(x) for x in seeds(start,n)]


def mechanics(rows,n):
    return len(rows)==2*n and all(sum(r['regime']==rg for r in rows)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] and 'external_seed' in r for r in rows)


def disagreement_scores(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets)
    p=b.posterior_from_fs(fs)
    scores=[]
    for target in range(b.N):
        means=[]; within=[]
        for spi,sp in enumerate((-2.0,2.0)):
            ems=[]
            rr=b.rng_for('s67','response-disagreement',seed,target,spi)
            for _ in range(SIMS):
                row=b.sim_row_from_posterior(p,models,target,sp,rr)
                q=b.update_p_with_row(p,models,row,target)
                if not np.isfinite(q).all() or abs(float(np.sum(q))-1.0)>1e-8:
                    return None
                ems.append(b.edge_marginals(q))
            a=np.asarray(ems,float)
            means.append(np.mean(a,axis=0))
            within.append(float(np.mean(np.var(a,axis=0))))
        separation=float(np.mean(np.abs(means[0]-means[1])))
        dispersion=float(np.mean(within))
        scores.append((dispersion+separation)/float(b.COSTS[target]))
    return np.asarray(scores,float)


def spearman(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<3 or np.std(x)<1e-12 or np.std(y)<1e-12: return 0.0
    rx=np.argsort(np.argsort(x)).astype(float); ry=np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx,ry)[0,1])


def evaluate(rows):
    sc=[]; vals=[]; dv=[]; cv=[]; wins=[]; finite=True
    by={rg:{'disagreement':[],'eig':[]} for rg in REGIMES}
    for r in rows:
        s=disagreement_scores(r['external_seed'])
        av=s66.acquisition_values(r['external_seed'],r)
        if s is None or av is None:
            finite=False; continue
        av=np.asarray(av,float)
        sc.extend(s.tolist()); vals.extend(av.tolist())
        dt=int(np.argmax(s)); ct=s66.eig_target(r['external_seed'])
        d=float(av[dt]); c=float(av[ct])
        dv.append(d); cv.append(c); wins.append(d>c)
        by[r['regime']]['disagreement'].append(d); by[r['regime']]['eig'].append(c)
    y=np.asarray(vals)>0
    auc=s60.auc(y,np.asarray(sc))
    rho=spearman(sc,vals)
    bout={}
    for rg in REGIMES:
        a=np.asarray(by[rg]['disagreement'],float); c=np.asarray(by[rg]['eig'],float)
        bout[rg]={'n':int(len(a)),'disagreement_mean_value_per_cost':float(np.mean(a)),'eig_mean_value_per_cost':float(np.mean(c)),'paired_difference':float(np.mean(a-c))}
    return {'n_worlds':len(rows),'finite':bool(finite),'positive_value_auc':auc,'spearman_score_vs_value':rho,'disagreement_mean_value_per_cost':float(np.mean(dv)),'eig_mean_value_per_cost':float(np.mean(cv)),'paired_mean_difference':float(np.mean(np.asarray(dv)-np.asarray(cv))),'disagreement_beats_eig_fraction':float(np.mean(wins)),'by_regime':bout}


def disposition(e):
    if not e['finite'] or e['positive_value_auc'] is None: return 'BLOCKED_EXECUTION_NONFINITE'
    regime_ok=all(v['paired_difference']>=-.02 for v in e['by_regime'].values())
    if e['positive_value_auc']>=.60 and e['spearman_score_vs_value']>=.10 and e['disagreement_mean_value_per_cost']>=e['eig_mean_value_per_cost'] and regime_ok:
        return 'RESPONSE_DISAGREEMENT_ALIGNED'
    if e['positive_value_auc']>=.56:
        return 'RESPONSE_DISAGREEMENT_WEAK'
    return 'RESPONSE_DISAGREEMENT_FALSIFIED'


if __name__=='__main__':
    me=generate_rows(100201,2)
    out={'mechanics':{'passed':mechanics(me,2)},'sims_per_setpoint':SIMS}
    if not out['mechanics']['passed']:
        out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        dg=generate_rows(100401,64)
        ev=evaluate(dg)
        out['diagnostic']=ev
        out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))