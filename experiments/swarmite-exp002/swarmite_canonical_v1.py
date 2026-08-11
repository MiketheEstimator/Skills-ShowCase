import json, math, time, hashlib
from dataclasses import dataclass
import numpy as np

N=5
EDGES=[(i,j) for i in range(N) for j in range(N) if i!=j]
EDGE_INDEX={e:k for k,e in enumerate(EDGES)}


def is_dag_mask(mask:int)->bool:
    indeg=[0]*N; out=[0]*N
    for k,(u,v) in enumerate(EDGES):
        if mask>>k & 1:
            out[u] |= 1<<v; indeg[v]+=1
    q=[i for i,d in enumerate(indeg) if d==0]; seen=0
    while q:
        u=q.pop(); seen+=1
        bits=out[u]
        while bits:
            l=bits & -bits; v=l.bit_length()-1; bits-=l
            indeg[v]-=1
            if indeg[v]==0:q.append(v)
    return seen==N

def enumerate_dags():
    masks=[]
    for m in range(1<<len(EDGES)):
        if is_dag_mask(m): masks.append(m)
    arr=np.array(masks,dtype=np.uint32)
    parents=np.zeros((len(arr),N),dtype=np.uint8)
    for gi,m in enumerate(arr):
        for k,(u,v) in enumerate(EDGES):
            if int(m)>>k & 1: parents[gi,v] |= 1<<u
    return arr,parents


def seed_int(*parts):
    s='|'.join(map(str,parts)).encode(); return int.from_bytes(hashlib.sha256(s).digest()[:8],'little')

def rng_for(*parts): return np.random.default_rng(seed_int(*parts))

@dataclass
class World:
    dag_mask:int
    W:np.ndarray
    order:list


def gen_world(seed):
    r=rng_for('world',seed)
    order=list(r.permutation(N)); W=np.zeros((N,N)); mask=0
    for a in range(N):
        for b in range(a+1,N):
            u,v=order[a],order[b]
            if r.random()<0.35:
                mag=r.uniform(.4,.9); sign=-1 if r.random()<.5 else 1
                W[u,v]=sign*mag; mask |= 1<<EDGE_INDEX[(u,v)]
    if mask.bit_count()<2:
        for a,b in [(0,1),(1,2)]:
            u,v=order[a],order[b]
            if W[u,v]==0:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9); mask |= 1<<EDGE_INDEX[(u,v)]
    return World(mask,W,order)

def sample(world,r,n=1,target=None,setpoint=None,soft=None):
    X=np.zeros((n,N))
    for i in range(n):
        for v in world.order:
            natural=float(X[i]@world.W[:,v] + r.normal())
            if target==v:
                if soft is None: X[i,v]=setpoint+r.normal(scale=.15)
                else: X[i,v]=soft*natural+(1-soft)*setpoint+r.normal(scale=.15)
            else:X[i,v]=natural
    return X

def log_ml(y,X,tau2=4.0):
    n=len(y)
    if n==0:return 0.0
    X=np.column_stack([np.ones(n),X])
    A=np.eye(X.shape[1])/tau2 + X.T@X
    sign,ld=np.linalg.slogdet(A)
    if sign<=0:return -1e100
    rhs=X.T@y
    quad=y@y-rhs@np.linalg.solve(A,rhs)
    logdetC=ld + X.shape[1]*math.log(tau2)
    return -0.5*(n*math.log(2*math.pi)+logdetC+quad)

def family_scores(data,targets):
    fs=np.full((N,1<<N),-1e100)
    for v in range(N):
        keep=np.array([t!=v for t in targets],bool)
        y=data[keep,v]
        for pm in range(1<<N):
            if pm>>v & 1: continue
            cols=[u for u in range(N) if pm>>u & 1]
            X=data[keep][:,cols] if cols else np.empty((len(y),0))
            fs[v,pm]=log_ml(y,X)
    return fs

def posterior(data,targets,dags,parent_masks):
    fs=family_scores(data,targets)
    ls=np.zeros(len(dags))
    for v in range(N): ls += fs[v,parent_masks[:,v]]
    ls-=ls.max(); p=np.exp(ls); p/=p.sum(); return p

def edge_marginals(p,dags):
    out=np.zeros(len(EDGES))
    for k in range(len(EDGES)): out[k]=p[((dags>>k)&1).astype(bool)].sum()
    return out

def metrics(p,dags,true_mask):
    em=edge_marginals(p,dags)
    truth=np.array([(true_mask>>k)&1 for k in range(len(EDGES))])
    edge=float(np.where(truth,1-em,em).sum())
    idx=int(np.argmax(p)); return {'edge_error':edge,'true_mass':float(p[dags==true_mask].sum()),'map':int(int(dags[idx])==true_mask),'entropy':float(-(p*np.log(p+1e-300)).sum())}

def proposals(p,dags,seed,step,swarm):
    em=edge_marginals(p,dags); unc=1-np.abs(em-.5)*2
    rin=rng_for('proposal',seed,step,swarm)
    cand=[]
    inc=[sum(unc[k] for k,(u,v) in enumerate(EDGES) if u==n or v==n) for n in range(N)]
    n=int(np.argmax(np.array(inc)+rin.normal(0,.03,N))); cand.append(('INFOGAIN',n,float(rin.choice([-2,2]))))
    k=int(np.argmax(unc+rin.normal(0,.02,len(unc)))); cand.append(('FALSIFY',EDGES[k][0],float(rin.choice([-2,2]))))
    cand.append(('CHEAPEST',int(rin.integers(N)),float(rin.choice([-1,1]))))
    mapm=int(dags[int(np.argmax(p))]); mapedges=np.array([(mapm>>kk)&1 for kk in range(len(EDGES))])
    k=int(np.argmax(np.abs(mapedges-em)+rin.normal(0,.01,len(em)))); cand.append(('RIVAL',EDGES[k][0],float(rin.choice([-2,2]))))
    score=[sum(unc[k]*(1-abs(em[k]-.5)) for k,(u,v) in enumerate(EDGES) if u==n or v==n) for n in range(N)]
    n=int(np.argmax(np.array(score)+rin.normal(0,.03,N))); cand.append(('WEAKTIE',n,float(rin.choice([-2,2]))))
    return cand

def candidate_score(p,dags,action,seed,step,cid,sims=3):
    em=edge_marginals(p,dags); _,node,val=action
    outunc=sum(4*em[k]*(1-em[k]) for k,(u,v) in enumerate(EDGES) if u==node)
    incunc=sum(4*em[k]*(1-em[k]) for k,(u,v) in enumerate(EDGES) if v==node)
    jitter=rng_for('planner',seed,step,cid).normal(0,.01)
    return outunc + .25*incunc + .03*abs(val) + jitter

def run_arm(world,seed,width,dags,parent_masks,budget=10,obs_n=30,soft=None):
    env=rng_for('envinit',seed)
    data=sample(world,env,obs_n); targets=[None]*obs_n
    p=posterior(data,targets,dags,parent_masks)
    spend=0; trace=[]
    while spend+1<=budget:
        step=len(trace); allc=[]
        for sw in range(width): allc += proposals(p,dags,seed,step,sw)
        scored=[candidate_score(p,dags,a,seed,step,i) for i,a in enumerate(allc)]
        pick=int(np.argmax(scored)); role,target,setpoint=allc[pick]
        er=rng_for('environment',seed,step,target,setpoint)
        new=sample(world,er,1,target,setpoint,soft=soft)
        data=np.vstack([data,new]); targets.append(target); spend+=1
        p=posterior(data,targets,dags,parent_masks)
        trace.append({'step':step,'role':role,'target':target,'setpoint':setpoint,'score':float(scored[pick])})
    m=metrics(p,dags,world.dag_mask); m.update({'spend':spend,'trace':trace}); return m

def self_test(dags,parent_masks):
    assert len(dags)==29281
    assert len(set(map(int,dags)))==29281
    for i in [0,1,100,1000,29280]:
        m=0
        for v in range(N):
            pm=int(parent_masks[i,v])
            for u in range(N):
                if pm>>u&1:m|=1<<EDGE_INDEX[(u,v)]
        assert m==int(dags[i])
    return True

def main(n=8,soft=None):
    t=time.time(); dags,pm=enumerate_dags(); enum_s=time.time()-t; self_test(dags,pm)
    rows=[]
    for seed in range(1000,1000+n):
        w=gen_world(seed)
        a=run_arm(w,seed,1,dags,pm,soft=soft); b=run_arm(w,seed,2,dags,pm,soft=soft)
        rows.append({'seed':seed,'true_mask':w.dag_mask,'w1':{k:v for k,v in a.items() if k!='trace'},'w2':{k:v for k,v in b.items() if k!='trace'},'delta_edge':b['edge_error']-a['edge_error'],'trace_w1':a['trace'],'trace_w2':b['trace']})
        print(seed, rows[-1]['delta_edge'])
    de=np.array([r['delta_edge'] for r in rows])
    out={'engine':'swarmite_canonical_v1','n':n,'soft':soft,'dag_count':len(dags),'enumeration_seconds':enum_s,'mean_edge_w1':float(np.mean([r['w1']['edge_error'] for r in rows])),'mean_edge_w2':float(np.mean([r['w2']['edge_error'] for r in rows])),'mean_delta':float(de.mean()),'map_w1':float(np.mean([r['w1']['map'] for r in rows])),'map_w2':float(np.mean([r['w2']['map'] for r in rows])),'rows':rows}
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
    open('/tmp/canonical_v1_pilot.json','w').write(json.dumps(out,indent=2))
if __name__=='__main__': main()
