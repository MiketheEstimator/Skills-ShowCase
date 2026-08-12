import math, random, statistics, json
from pathlib import Path

MODELS = {
    'clean_strong': {'mu':1.50,'sigma':0.65},
    'moderate': {'mu':1.30,'sigma':0.82},
    'noisy_weak': {'mu':1.15,'sigma':1.00},
    'very_noisy': {'mu':0.95,'sigma':1.20},
}

def H(p):
    p=min(.999999,max(.000001,p)); return -(p*math.log2(p)+(1-p)*math.log2(1-p))
def normpdf(x,mu,s): return math.exp(-0.5*((x-mu)/s)**2)/(s*math.sqrt(2*math.pi))
def normalize(d):
    z=sum(d.values()) or 1.0
    return {k:v/z for k,v in d.items()}

def make_world(seed,n,transfer=False):
    rng=random.Random(seed); edges=set(); p=min(.42,3.5/n) if transfer else min(.28,2.2/n)
    for i in range(n):
        for j in range(i+1,n):
            if rng.random()<p: edges.add((i,j))
    costs=([0.7+random.Random(seed+31337+i).random()*1.5 for i in range(n)] if transfer else [1+.08*i for i in range(n)])
    return edges,costs

def observe(truth,node,n,rng,transfer):
    mu,sig=(1.15,1.0) if transfer else (1.5,.65)
    return {(node,j): ((mu if (node,j) in truth else -mu)+rng.gauss(0,sig)) for j in range(node+1,n)}

def bayes_update(beliefs,mw,obs):
    oldmw=dict(mw); marginal_by_model={m:1.0 for m in mw}
    for e,y in obs.items():
        p=beliefs[e]
        for m,w in mw.items():
            q=MODELS[m]; lp=normpdf(y,q['mu'],q['sigma']); la=normpdf(y,-q['mu'],q['sigma'])
            marginal_by_model[m] *= max(1e-300,p*lp+(1-p)*la)
    logs={m:math.log(max(1e-300,oldmw[m]))+math.log(max(1e-300,marginal_by_model[m])) for m in mw}
    mx=max(logs.values()); mw=normalize({m:math.exp(v-mx) for m,v in logs.items()})
    for e,y in obs.items():
        p=beliefs[e]; lp=sum(mw[m]*normpdf(y,MODELS[m]['mu'],MODELS[m]['sigma']) for m in mw); la=sum(mw[m]*normpdf(y,-MODELS[m]['mu'],MODELS[m]['sigma']) for m in mw)
        beliefs[e]=(p*lp)/max(1e-300,p*lp+(1-p)*la)
    return beliefs,mw

def js_model_entropy(mw): return sum(-w*math.log2(max(w,1e-12)) for w in mw.values())
def expected_edge_entropy_after(p,mw,samples=9):
    reliability=sum(w*(math.tanh(MODELS[m]['mu']/MODELS[m]['sigma']))**2 for m,w in mw.items())
    return H(p)*reliability

def node_scores(n,beliefs,mw,visits,costs):
    out={}; ment=js_model_entropy(mw)/max(1e-9,math.log2(len(mw)))
    for node in range(n):
        edges=[(node,j) for j in range(node+1,n)]
        if not edges: out[node]={'info':0,'novel':0,'robust':0}; continue
        info=sum(expected_edge_entropy_after(beliefs[e],mw) for e in edges)/costs[node]
        novel=info/math.sqrt(1+visits.get(node,0)); disagreement=0.0
        for e in edges:
            p=beliefs[e]; mus=[MODELS[m]['mu']/MODELS[m]['sigma'] for m in mw]
            mean=sum(mw[m]*mus[i] for i,m in enumerate(mw))
            disagreement += sum(mw[m]*(mus[i]-mean)**2 for i,m in enumerate(mw))*4*p*(1-p)
        disagreement=disagreement/max(1,len(edges))/costs[node]
        robust=0.58*info+0.27*novel+0.15*ment*disagreement
        out[node]={'info':info,'novel':novel,'robust':robust}
    return out

def metrics(truth,beliefs):
    pred={e for e,p in beliefs.items() if p>=.5}; tp=len(pred&truth); fp=len(pred-truth); fn=len(truth-pred); tn=len(beliefs)-tp-fp-fn
    acc=(tp+tn)/len(beliefs); prec=tp/max(1,tp+fp); rec=tp/max(1,tp+fn); f1=2*prec*rec/max(1e-12,prec+rec)
    brier=sum((p-(1 if e in truth else 0))**2 for e,p in beliefs.items())/len(beliefs)
    return {'accuracy':acc,'precision':prec,'recall':rec,'f1':f1,'brier':brier}

def run(seed,n,budget,policy,transfer=False):
    truth,costs=make_world(seed,n,transfer); rng=random.Random(seed+99991)
    beliefs={(i,j):.5 for i in range(n) for j in range(i+1,n)}; mw={m:1/len(MODELS) for m in MODELS}; visits={}; info=spent=0.0
    for step in range(budget):
        scores=node_scores(n,beliefs,mw,visits,costs)
        node=rng.randrange(n) if policy=='random' else max(range(n),key=lambda k:scores[k][policy]+rng.random()*1e-8)
        visits[node]=visits.get(node,0)+1; before=sum(H(p) for p in beliefs.values())
        obs=observe(truth,node,n,rng,transfer); beliefs,mw=bayes_update(beliefs,mw,obs)
        after=sum(H(p) for p in beliefs.values()); info+=max(0,before-after); spent+=costs[node]
        if sum(.12<p<.88 for p in beliefs.values())<max(2,n/3): break
    mm=metrics(truth,beliefs); mm.update({'efficiency':info/max(spent,1e-9),'steps':step+1,'model_entropy':js_model_entropy(mw),'model_weights':mw})
    return mm
