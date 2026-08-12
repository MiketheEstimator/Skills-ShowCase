import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s40_hetero as s40
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s49_hetero_likelihood as s49
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s65_decision_theoretic_local_structural_action as s65

REGIMES=('linear','heteroskedastic')


def seeds(start,n):
    out=[]
    for rg in REGIMES:
        out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out


def generate_rows(start,n):
    return [s54.world_base(x) for x in seeds(start,n)]


def mechanics(rows,n):
    return len(rows)==2*n and all(sum(r['regime']==rg for r in rows)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in rows)


def envrow(reg,w,seed,step,target,setpoint,meta):
    rr=b.rng_for('s66','acq',seed,step,target,setpoint)
    if reg=='heteroskedastic':
        return s40.env(w,rr,1,target,setpoint,meta['mechanism'])[0]
    return b.env_sample(w,rr,1,target,setpoint)[0]


def s30_after(data,targets,p0):
    ps,ok=s49.s30_posterior(data,targets,p0)
    return np.asarray(ps,float),bool(ok and np.isfinite(ps).all() and abs(float(np.sum(ps))-1)<1e-8)


def acquisition_values(external_seed,row):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    current=np.asarray(row['ps30'],float); cur=float(b.posterior_metrics(current,w.dag_mask)['edge_error'])
    vals=[]
    for v in range(b.N):
        gg=[]
        for j,sp in enumerate((-2.0,2.0)):
            x=envrow(reg,w,seed,j,v,sp,meta)
            nd=np.vstack([data,x]); nt=list(targets)+[v]
            fs,_=b.build_family_models(nd,nt); np0=b.posterior_from_fs(fs); ps,ok=s30_after(nd,nt,np0)
            if not ok: return None
            ee=float(b.posterior_metrics(ps,w.dag_mask)['edge_error']); gg.append((cur-ee)/float(b.COSTS[v]))
        vals.append(float(np.mean(gg)))
    return vals


def eig_target(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets)
    aff=b.proposals(p0,seed,999,0)
    scores=[b.eig_score(p0,models,a,seed,999,i) for i,a in enumerate(aff)]
    return int(aff[int(np.argmax(scores))][1])


def spearman(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<3 or np.std(x)<1e-12 or np.std(y)<1e-12: return 0.0
    rx=np.argsort(np.argsort(x)).astype(float); ry=np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx,ry)[0,1])


def evaluate(rows,model):
    probs=[]; vals=[]; ev=[]; cv=[]; wins=[]; regs=[]; finite=True
    by={rg:{'evidence':[],'eig':[]} for rg in REGIMES}
    for r in rows:
        pe=s65.predictions(r,model); av=acquisition_values(r['external_seed'],r)
        if av is None: finite=False; continue
        av=np.asarray(av,float); probs.extend(pe.tolist()); vals.extend(av.tolist())
        score=pe/np.asarray(b.COSTS,float); et=int(np.argmax(score)); ct=eig_target(r['external_seed'])
        e=float(av[et]); c=float(av[ct]); ev.append(e); cv.append(c); wins.append(e>c); regs.append(r['regime']); by[r['regime']]['evidence'].append(e); by[r['regime']]['eig'].append(c)
    y=np.asarray(vals)>0; auc=s60.auc(y,np.asarray(probs)); rho=spearman(probs,vals)
    bout={}
    for rg in REGIMES:
        a=np.asarray(by[rg]['evidence'],float); c=np.asarray(by[rg]['eig'],float)
        bout[rg]={'n':int(len(a)),'evidence_mean_value_per_cost':float(np.mean(a)),'eig_mean_value_per_cost':float(np.mean(c)),'paired_difference':float(np.mean(a-c))}
    return {'n_worlds':len(rows),'finite':bool(finite),'positive_value_auc':auc,'spearman_probability_vs_value':rho,'evidence_mean_value_per_cost':float(np.mean(ev)),'eig_mean_value_per_cost':float(np.mean(cv)),'paired_mean_difference':float(np.mean(np.asarray(ev)-np.asarray(cv))),'evidence_beats_eig_fraction':float(np.mean(wins)),'by_regime':bout}


def disposition(e):
    if not e['finite'] or e['positive_value_auc'] is None: return 'BLOCKED_EXECUTION_NONFINITE'
    regime_ok=all(v['paired_difference']>=-.02 for v in e['by_regime'].values())
    if e['positive_value_auc']>=.60 and e['spearman_probability_vs_value']>=.10 and e['evidence_mean_value_per_cost']>=e['eig_mean_value_per_cost'] and regime_ok: return 'ALLOCATION_SIGNAL_ALIGNED'
    if e['positive_value_auc']>=.56: return 'ALLOCATION_SIGNAL_WEAK'
    return 'ALLOCATION_SIGNAL_FALSIFIED'


if __name__=='__main__':
    me=generate_rows(99201,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        tr=generate_rows(99301,64); model=s65.train_model(tr); dg=generate_rows(99701,64); ev=evaluate(dg,model); out['model']=model; out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))
