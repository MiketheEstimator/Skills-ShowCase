import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s49_hetero_likelihood as s49
import swarmite_exp002_s50_world_model_mixture as s50

REGIMES=('linear','heteroskedastic')


def ranks(x):
    x=np.asarray(x,float)
    order=np.argsort(x,kind='mergesort')
    r=np.empty(len(x),float)
    i=0
    while i<len(x):
        j=i+1
        while j<len(x) and x[order[j]]==x[order[i]]: j+=1
        val=(i+j-1)/2.0+1.0
        r[order[i:j]]=val
        i=j
    return r


def auc(scores, labels):
    s=np.asarray(scores,float); y=np.asarray(labels,bool)
    n1=int(y.sum()); n0=len(y)-n1
    if n1==0 or n0==0: return None
    rr=ranks(s)
    return float((rr[y].sum()-n1*(n1+1)/2)/(n1*n0))


def rank_corr(x,y):
    if len(x)<3: return None
    rx=ranks(x); ry=ranks(y)
    if np.std(rx)==0 or np.std(ry)==0: return None
    return float(np.corrcoef(rx,ry)[0,1])


def boot_mean(x,reps=10000,seed=25151):
    x=np.asarray(x,float)
    if len(x)==0: return [None,None]
    rr=np.random.default_rng(seed)
    mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def world_row(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s49.s30_posterior(data,targets,p0)
    phet,okh=s49.hetero_posterior(data,targets)
    dvar,qhet,nscore,oke=s50.cv_variance_evidence(data,targets)
    bm=b.posterior_metrics(p0,w.dag_mask); sm=b.posterior_metrics(ps30,w.dag_mask); hm=b.posterior_metrics(phet,w.dag_mask)
    base=s48.world_row(external_seed)
    model,rule=s48.load_anchor()
    pred=s46.predict([base],model)[0]
    promote=bool(pred['pred_edge_delta']<=rule['edge_cut'] and pred['pred_harm_prob']<=rule['harm_cut'])
    s30d=float(sm['edge_error']-bm['edge_error']); phetd=float(hm['edge_error']-bm['edge_error'])
    gain=float(sm['edge_error']-hm['edge_error']); oracle=max(0.0,gain)
    out=dict(base)
    out.update({
        'd_var':float(dvar),'q_het':float(qhet),'variance_score_n':int(nscore),
        'baseline_edge_error':float(bm['edge_error']),'baseline_brier':float(bm['brier']),
        's30_edge_error':float(sm['edge_error']),'s30_brier':float(sm['brier']),
        'phet_edge_error':float(hm['edge_error']),'phet_brier':float(hm['brier']),
        's30_edge_delta_vs_baseline':s30d,'phet_edge_delta_vs_baseline':phetd,
        'specialist_gain_over_s30':gain,'oracle_two_posterior_headroom':oracle,
        'specialist_beats_s30':bool(gain>0),'s30_large_harm':bool(s30d>.50),
        'pred_edge_delta':float(pred['pred_edge_delta']),'pred_harm_prob':float(pred['pred_harm_prob']),'promote':promote,
        'posterior_mechanics_ok':bool(ok30 and okh and oke and np.isfinite(ps30).all() and np.isfinite(phet).all()),
        's30_sum':float(ps30.sum()),'phet_sum':float(phet.sum())
    })
    return out


def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(
        r['spend']<=15 and r['trace_identical'] and r['finite'] and r['posterior_mechanics_ok'] and r['variance_score_n']>0 and
        0<=r['q_het']<=1 and abs(r['s30_sum']-1)<1e-8 and abs(r['phet_sum']-1)<1e-8
        for r in rows)


def subset_stats(rows, seed=25151):
    s30=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float)
    ph=np.array([r['phet_edge_delta_vs_baseline'] for r in rows],float)
    gain=np.array([r['specialist_gain_over_s30'] for r in rows],float)
    oracle=np.array([r['oracle_two_posterior_headroom'] for r in rows],float)
    labels=np.array([r['specialist_beats_s30'] for r in rows],bool)
    q=np.array([r['q_het'] for r in rows],float)
    promote=np.array([r['promote'] for r in rows],bool)
    harm=np.array([r['s30_large_harm'] for r in rows],bool)
    return {
        'n':len(rows),
        'mean_s30_edge_delta_vs_baseline':float(np.mean(s30)),
        'mean_phet_edge_delta_vs_baseline':float(np.mean(ph)),
        'specialist_win_rate':float(np.mean(labels)),
        'mean_specialist_gain_over_s30':float(np.mean(gain)),
        'mean_oracle_two_posterior_headroom':float(np.mean(oracle)),
        'oracle_headroom_bootstrap95':boot_mean(oracle,seed=seed),
        's30_large_harm_rate':float(np.mean(harm)),
        's46_promoted_large_harm_rate_all':float(np.mean(harm & promote)),
        's46_promoted_large_harm_rate_among_promoted':float(np.sum(harm & promote)/max(1,promote.sum())),
        'promotion_coverage':float(np.mean(promote)),
        'qhet_auc_for_specialist_win':auc(q,labels),
        'qhet_rank_corr_with_specialist_gain':rank_corr(q,gain),
        'mean_qhet':float(np.mean(q))
    }


def diagnose(rows):
    by={rg:subset_stats([r for r in rows if r['regime']==rg],25151+i) for i,rg in enumerate(REGIMES)}
    overall=subset_stats(rows,25160)
    h=by['heteroskedastic']; lo,hi=h['oracle_headroom_bootstrap95']; a=h['qhet_auc_for_specialist_win']
    if h['mean_oracle_two_posterior_headroom']>=.10 and lo is not None and lo>0 and (a is None or a<.65): cls='ADJUDICATION_DOMINANT'
    elif h['mean_oracle_two_posterior_headroom']<.05 or (hi is not None and hi<=.05): cls='POINT_ESTIMATE_DOMINANT'
    else: cls='MIXED'
    return {'classification':cls,'overall':overall,'by_regime':by}

if __name__=='__main__':
    me=generate(78101,2); out={'mechanics':{'passed':mechanics(me,2),'rows':me}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        rows=generate(78201,48); dg=diagnose(rows); out['diagnostic']=dg; out['rows']=rows
        out['disposition']='COMPLETE_DIAGNOSTIC_'+dg['classification'] if mechanics(rows,48) else 'BLOCKED_MECHANICS'
    print(json.dumps(out,separators=(',',':')))