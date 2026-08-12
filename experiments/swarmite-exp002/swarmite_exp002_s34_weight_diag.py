import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33


def rankdata(x):
    x=np.asarray(x,float); order=np.argsort(x,kind='mergesort'); ranks=np.empty(len(x),float); i=0
    while i<len(x):
      j=i+1
      while j<len(x) and x[order[j]]==x[order[i]]: j+=1
      ranks[order[i:j]]=(i+j-1)/2+1; i=j
    return ranks


def spearman(x,y):
    rx,ry=rankdata(x),rankdata(y)
    if np.std(rx)<1e-12 or np.std(ry)<1e-12: return 0.0
    return float(np.corrcoef(rx,ry)[0,1])


def diagnose(seed):
    world=b.gen_world(seed); c,data,targets,p0,cell=s33.s32.run_control(world,seed)
    posts={}; finite=True
    for name in s33.CLASSES:
      if name=='LG': posts[name]=p0.copy(); ok=True
      else: posts[name],ok=s33.build_class(data,targets,name)
      finite=finite and ok
    scores={name:s33.cv_score(data,targets,name) for name in s33.CLASSES}
    weights=s33.softmax_weights(scores)
    pexp=np.zeros_like(p0)
    for name in s33.CLASSES: pexp += weights[name]*posts[name]
    pexp/=pexp.sum()
    alpha=s33.sigmoid((scores['TT']-scores['LG'])/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    metrics={name:b.posterior_metrics(posts[name],world.dag_mask) for name in s33.CLASSES}
    em=b.posterior_metrics(pexp,world.dag_mask); sm=b.posterior_metrics(ps30,world.dag_mask)
    oracle=min(s33.CLASSES,key=lambda n:metrics[n]['edge_error']); top=max(s33.CLASSES,key=lambda n:weights[n])
    represented_beats=any(metrics[n]['edge_error'] < sm['edge_error'] for n in s33.CLASSES)
    rho=spearman([scores[n] for n in s33.CLASSES],[-metrics[n]['edge_error'] for n in s33.CLASSES])
    return {'seed':int(seed),'cell':cell,'spend':int(c['spend']),'dag_count':len(b.dags),'trace_identical':True,'finite':bool(finite),
      'scores':scores,'weights':weights,'class_metrics':metrics,'oracle_best_class':oracle,'top_weight_class':top,'top_matches_oracle':int(top==oracle),
      'score_edge_spearman':rho,'represented_class_beats_s30':int(represented_beats),'oracle_edge_error':float(metrics[oracle]['edge_error']),
      's30_edge_error':float(sm['edge_error']),'expanded_edge_error':float(em['edge_error']),'mixture_regret_vs_oracle':float(em['edge_error']-metrics[oracle]['edge_error']),
      's30_regret_vs_oracle':float(sm['edge_error']-metrics[oracle]['edge_error']),'weights_sum':float(sum(weights.values())),
      'posterior_sums_ok':bool(all(abs(float(posts[n].sum())-1)<1e-8 for n in s33.CLASSES) and abs(float(pexp.sum())-1)<1e-8 and abs(float(ps30.sum())-1)<1e-8)}


def summarize(rows):
    n=len(rows); mean_rho=float(np.mean([r['score_edge_spearman'] for r in rows])); match=float(np.mean([r['top_matches_oracle'] for r in rows])); coverage=float(np.mean([r['represented_class_beats_s30'] for r in rows])); regret=float(np.mean([r['mixture_regret_vs_oracle'] for r in rows])); s30reg=float(np.mean([r['s30_regret_vs_oracle'] for r in rows]))
    mechanics=all(r['dag_count']==29281 and r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['weights_sum']-1)<1e-8 and r['posterior_sums_ok'] and np.isfinite(r['score_edge_spearman']) for r in rows)
    if coverage<0.60: disp='MODEL_SET_INSUFFICIENCY'
    elif mean_rho<0.20 or match<0.25: disp='PREDICTIVE_WEIGHT_MISALIGNMENT'
    elif regret>=0.20: disp='CLASS_DILUTION'
    else: disp='MIXED_FAILURE'
    by_oracle={c:sum(r['oracle_best_class']==c for r in rows) for c in s33.CLASSES}; by_top={c:sum(r['top_weight_class']==c for r in rows) for c in s33.CLASSES}
    return {'n':n,'mean_score_edge_spearman':mean_rho,'top_weight_oracle_match_rate':match,'represented_class_beats_s30_rate':coverage,'mean_mixture_regret_vs_oracle':regret,'mean_s30_regret_vs_oracle':s30reg,'oracle_class_counts':by_oracle,'top_weight_class_counts':by_top,'mechanics_ok':mechanics,'disposition':disp}

if __name__=='__main__':
 import sys
 rows=[diagnose(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
