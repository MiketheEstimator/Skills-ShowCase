import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s59_residual_state_evidence_decomposition as s59
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60

REGIMES=('linear','heteroskedastic')
FEATURES=('mean_js','max_js','anchor_mass_drop','competitor_mean_mass','competitor_vote_share','switch_rate','margin_erosion','mean_entropy')
EPS=1e-12


def legal_pms(v): return s60.legal_pms(v)

def hamming(a,c): return int((int(a)^int(c)).bit_count())


def softmax_scores(fs,v,pms):
    z=np.asarray([float(fs[v,pm]) for pm in pms],float)
    finite=np.isfinite(z)
    if not finite.any(): return np.ones(len(pms))/len(pms)
    floor=float(np.min(z[finite])-100.0); z=np.where(finite,z,floor); z-=np.max(z)
    q=np.exp(np.clip(z,-80,0)); q/=q.sum(); return q


def js_div(p,q):
    p=np.clip(np.asarray(p,float),EPS,1); q=np.clip(np.asarray(q,float),EPS,1); m=.5*(p+q)
    return float(.5*np.sum(p*np.log(p/m))+.5*np.sum(q*np.log(q/m)))


def entropy(q):
    q=np.clip(np.asarray(q,float),EPS,1)
    return float(-np.sum(q*np.log(q))/max(math.log(len(q)),EPS))


def node_diagnostic(data,targets,fs,v):
    pms=legal_pms(v); qfull=softmax_scores(fs,v,pms); sel=pms[int(np.argmax(qfull))]; sel_idx=pms.index(sel)
    idx=np.asarray([i for i,t in enumerate(targets) if not (isinstance(t,(int,np.integer)) and int(t)==v)],int)
    labs=[]
    for i in idx:
        lab=s60.key_lab(targets[i])
        if lab not in labs: labs.append(lab)
    qs=[]; maps=[]; margins=[]
    for lab in labs:
        tr=np.asarray([i for i in idx if s60.key_lab(targets[i])!=lab],int)
        if len(tr)<8: continue
        d=np.asarray(data[tr],float); tt=np.asarray(targets,dtype=object)[tr]
        try: fsi,_=b.build_family_models(d,tt)
        except Exception: continue
        qi=softmax_scores(fsi,v,pms)
        if not np.all(np.isfinite(qi)): continue
        qs.append(qi); maps.append(pms[int(np.argmax(qi))])
        ss=np.sort(qi); margins.append(float(ss[-1]-ss[-2]) if len(ss)>=2 else 0.0)
    if not qs:
        qs=[qfull.copy()]; maps=[sel]; margins=[0.0]
    Q=np.asarray(qs,float); qbar=Q.mean(0); non=[i for i,pm in enumerate(pms) if pm!=sel]
    ci=max(non,key=lambda i:float(qbar[i])) if non else sel_idx; comp=pms[ci]
    js=np.asarray([js_div(q,qfull) for q in Q],float); full_sorted=np.sort(qfull); full_margin=float(full_sorted[-1]-full_sorted[-2]) if len(full_sorted)>=2 else 0.0
    feat={
      'mean_js':float(np.mean(js)),'max_js':float(np.max(js)),
      'anchor_mass_drop':float(max(0.0,qfull[sel_idx]-qbar[sel_idx])),
      'competitor_mean_mass':float(qbar[ci]),
      'competitor_vote_share':float(np.mean([m==comp for m in maps])),
      'switch_rate':float(np.mean([m!=sel for m in maps])),
      'margin_erosion':float(max(0.0,full_margin-float(np.mean(margins)))),
      'mean_entropy':float(np.mean([entropy(q) for q in Q])),
      'n_refits':int(len(Q))
    }
    return int(sel),int(comp),feat


def node_rows(external_seed):
    base=s54.world_base(external_seed); reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed); fs,_=b.build_family_models(data,targets)
    out=[]
    for v in range(b.N):
        truth=s59.true_parent_mask(base['true_mask'],v); margin=s59.margin(fs,v,truth); sel,comp,feat=node_diagnostic(data,targets,fs,v)
        row={'external_seed':int(external_seed),'regime':reg,'node':int(v),'true_parent_mask':int(truth),
             'anchor_selected_parent_mask':sel,'competitor_parent_mask':comp,'anchor_margin':float(margin),
             'anchor_rank_error':bool(margin<0),'competitor_better_than_selected':bool(hamming(comp,truth)<hamming(sel,truth)),
             'competitor_exact_truth':bool(comp==truth),'trace_identical':bool(base['trace_identical']),'spend':int(base['spend']),'finite':bool(base['finite'])}
        row.update(feat); row['finite']=bool(row['finite'] and all(math.isfinite(float(row[k])) for k in FEATURES))
        out.append(row)
    return out


def selected(start,n_each): return s60.selected(start,n_each)

def generate(start,n_each):
    rows=[]
    for seed in selected(start,n_each): rows.extend(node_rows(seed))
    return rows


def mechanics(rows,n_each):
    return len(rows)==2*n_each*b.N and all(sum(r['regime']==rg for r in rows)==n_each*b.N for rg in REGIMES) and all(r['trace_identical'] and r['spend']<=15 and r['finite'] and r['n_refits']>=1 for r in rows)


def summarize(rows):
    y=[r['anchor_rank_error'] for r in rows]; aucs={k:s60.auc(y,[r[k] for r in rows]) for k in FEATURES}; finite=[(v,k) for k,v in aucs.items() if math.isfinite(v)]; best=max(finite) if finite else (float('nan'),None)
    er=[r for r in rows if r['anchor_rank_error']]
    return {'n_nodes':len(rows),'n_anchor_rank_errors':len(er),'anchor_rank_error_rate':float(np.mean(y)) if y else float('nan'),
            'feature_auc':aucs,'best_auc':float(best[0]),'best_feature':best[1],
            'competitor_useful_fraction_on_error_nodes':float(np.mean([r['competitor_better_than_selected'] for r in er])) if er else float('nan'),
            'competitor_exact_truth_fraction_on_error_nodes':float(np.mean([r['competitor_exact_truth'] for r in er])) if er else float('nan'),
            'mean_refits':float(np.mean([r['n_refits'] for r in rows])) if rows else 0.0}


def bootstrap_best_auc(rows,reps=3000,seed=26262):
    rr=np.random.default_rng(seed); n=len(rows); vals=[]
    for _ in range(reps):
        samp=[rows[i] for i in rr.integers(0,n,n)]; y=[r['anchor_rank_error'] for r in samp]; aa=[s60.auc(y,[r[k] for r in samp]) for k in FEATURES]; aa=[x for x in aa if math.isfinite(x)]
        if aa: vals.append(max(aa))
    return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))] if vals else [float('nan'),float('nan')]


def evaluate(rows):
    ev=summarize(rows); ev['best_auc_bootstrap95']=bootstrap_best_auc(rows); ev['by_regime']={rg:summarize([r for r in rows if r['regime']==rg]) for rg in REGIMES}; return ev


def disposition(ev):
    auc=float(ev['best_auc']); lo=float(ev['best_auc_bootstrap95'][0]); useful=float(ev['competitor_useful_fraction_on_error_nodes'])
    loc=math.isfinite(auc) and auc>=.60 and math.isfinite(lo) and lo>=.55; prop=math.isfinite(useful) and useful>.50
    if loc and prop: return 'POSTERIOR_DISAGREEMENT_ALIGNED'
    if loc: return 'ERROR_LOCALIZATION_ONLY'
    if prop: return 'PROPOSAL_ONLY'
    return 'POSTERIOR_DISAGREEMENT_NOT_ALIGNED'


if __name__=='__main__':
    me=generate(95201,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        rows=generate(95301,64); ev=evaluate(rows); out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))
