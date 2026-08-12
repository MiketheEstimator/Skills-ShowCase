import importlib.util, statistics, json, random
from pathlib import Path
spec=importlib.util.spec_from_file_location('v7',Path(__file__).with_name('ensemble_planner_v7.py')); v7=importlib.util.module_from_spec(spec); spec.loader.exec_module(v7)

def run(seed,n,budget,transfer,noisy_threshold=.55,coverage_threshold=.70):
    truth,costs=v7.make_world(seed,n,transfer); rng=random.Random(seed+99991)
    beliefs={(i,j):.5 for i in range(n) for j in range(i+1,n)}; mw={m:1/len(v7.MODELS) for m in v7.MODELS}; visits={}; info=spent=0.0; switches=0; modes=[]
    for step in range(budget):
        scores=v7.node_scores(n,beliefs,mw,visits,costs)
        noisy=mw['noisy_weak']+mw['very_noisy']; coverage=sum(1 for i in range(n-1) if visits.get(i,0)>0)/max(1,n-1)
        policy='info' if noisy>=noisy_threshold and coverage>=coverage_threshold else 'novel'
        if modes and modes[-1]!=policy: switches+=1
        modes.append(policy)
        node=max(range(n),key=lambda k:scores[k][policy]+rng.random()*1e-8)
        visits[node]=visits.get(node,0)+1; before=sum(v7.H(p) for p in beliefs.values())
        obs=v7.observe(truth,node,n,rng,transfer); beliefs,mw=v7.bayes_update(beliefs,mw,obs)
        after=sum(v7.H(p) for p in beliefs.values()); info+=max(0,before-after); spent+=costs[node]
        if sum(.12<p<.88 for p in beliefs.values())<max(2,n/3): break
    mm=v7.metrics(truth,beliefs); mm.update({'efficiency':info/max(spent,1e-9),'steps':step+1,'switches':switches,'final_noisy_mass':mw['noisy_weak']+mw['very_noisy']})
    return mm
