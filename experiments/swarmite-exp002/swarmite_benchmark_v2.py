import numpy as np, math, hashlib, time, json, textwrap, os, statistics
N=5
EDGES=[(i,j) for i in range(N) for j in range(N) if i!=j]
EDGE_INDEX={e:k for k,e in enumerate(EDGES)}
def is_dag_mask(mask):
    indeg=[0]*N; out=[0]*N
    for k,(u,v) in enumerate(EDGES):
        if mask>>k&1:
            out[u]|=1<<v; indeg[v]+=1
    q=[i for i,d in enumerate(indeg) if d==0]; seen=0
    while q:
        u=q.pop(); seen+=1; bits=out[u]
        while bits:
            l=bits&-bits; v=l.bit_length()-1; bits-=l
            indeg[v]-=1
            if indeg[v]==0:q.append(v)
    return seen==N

def enumerate_dags():
    masks=[]
    for m in range(1<<len(EDGES)):
        if is_dag_mask(m): masks.append(m)
    return masks

masks=enumerate_dags()
dags=np.array(masks,dtype=np.uint32)
parents=np.zeros((len(dags),N),dtype=np.uint8)
for gi,m in enumerate(dags):
    mm=int(m)
    for k,(u,v) in enumerate(EDGES):
        if mm>>k&1: parents[gi,v]|=1<<u

def topo_from_mask(mask):
    indeg=[0]*N; out=[[] for _ in range(N)]
    for k,(u,v) in enumerate(EDGES):
        if mask>>k&1: out[u].append(v); indeg[v]+=1
    q=[i for i,d in enumerate(indeg) if d==0]; order=[]
    while q:
        u=min(q); q.remove(u); order.append(u)
        for v in out[u]:
            indeg[v]-=1
            if indeg[v]==0:q.append(v)
    return order

COSTS=np.array([1,1,2,2,3],dtype=int)
TAU2=4.0
OBS_N=30
BUDGET=15
EIG_SIMS=3

def seed_int(*parts):
    s='|'.join(map(str,parts)).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8],'little')
def rng_for(*parts): return np.random.default_rng(seed_int(*parts))

class World:
    def __init__(self, dag_mask,W,order,seed):
        self.dag_mask=int(dag_mask); self.W=W; self.order=order; self.seed=seed

def gen_world(seed):
    r=rng_for('v2','world',seed)
    order=list(map(int,r.permutation(N))); W=np.zeros((N,N)); mask=0
    for a in range(N):
        for b in range(a+1,N):
            u,v=order[a],order[b]
            if r.random()<0.35:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9)
                mask|=1<<EDGE_INDEX[(u,v)]
    if int(mask).bit_count()<2:
        for a,b in [(0,1),(1,2)]:
            u,v=order[a],order[b]
            if W[u,v]==0:
                W[u,v]=r.choice([-1,1])*r.uniform(.4,.9)
                mask|=1<<EDGE_INDEX[(u,v)]
    return World(mask,W,order,seed)

def env_sample(world,r,n,target=None,setpoint=None):
    X=np.zeros((n,N))
    for i in range(n):
        for v in world.order:
            if target==v:
                X[i,v]=setpoint
            else:
                X[i,v]=float(X[i]@world.W[:,v]+r.normal())
    return X

def build_family_models(data,targets):
    fs=np.full((N,1<<N),-1e100)
    models={}
    for v in range(N):
        keep=np.array([t!=v for t in targets],dtype=bool)
        y=data[keep,v]
        for pm in range(1<<N):
            if pm>>v&1: continue
            cols=[u for u in range(N) if pm>>u&1]
            X=data[keep][:,cols] if cols else np.empty((len(y),0))
            Xd=np.column_stack([np.ones(len(y)),X])
            A=np.eye(Xd.shape[1])/TAU2+Xd.T@Xd
            Ainv=np.linalg.inv(A)
            rhs=Xd.T@y
            mu=Ainv@rhs
            quad=float(y@y-rhs@mu)
            sign,ld=np.linalg.slogdet(A)
            logdetC=float(ld+Xd.shape[1]*math.log(TAU2))
            fs[v,pm]=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad)
            models[(v,pm)]=(cols,mu,Ainv)
    return fs,models

def posterior_from_fs(fs):
    ls=np.zeros(len(dags))
    for v in range(N): ls += fs[v,parents[:,v]]
    ls-=ls.max(); p=np.exp(ls); p/=p.sum(); return p

def edge_marginals(p):
    return np.array([p[((dags>>k)&1).astype(bool)].sum() for k in range(len(EDGES))])

def entropy(p): return float(-(p*np.log(p+1e-300)).sum())

def posterior_metrics(p,true_mask):
    em=edge_marginals(p)
    truth=np.array([(true_mask>>k)&1 for k in range(len(EDGES))])
    edge=float(np.where(truth,1-em,em).sum())
    mapmask=int(dags[int(np.argmax(p))])
    brier=float(np.mean((em-truth)**2))
    return {'edge_error':edge,'true_mass':float(p[dags==true_mask].sum()),'map':int(mapmask==true_mask),'entropy':entropy(p),'brier':brier}

def pred_params(models,v,pm,row):
    cols,mu,Ainv=models[(v,pm)]
    x=np.array([1.0]+[row[u] for u in cols])
    mean=float(x@mu); var=float(1.0+x@Ainv@x)
    return mean,max(var,1e-12)

def sim_row_from_posterior(p,models,target,setpoint,r):
    gi=int(r.choice(len(dags),p=p)); mask=int(dags[gi]); order=topo_from_mask(mask)
    row=np.zeros(N)
    for v in order:
        if v==target: row[v]=setpoint
        else:
            pm=int(parents[gi,v]); mean,var=pred_params(models,v,pm,row)
            row[v]=r.normal(mean,math.sqrt(var))
    return row

def predictive_increment(models,row,target):
    incfs=np.zeros((N,1<<N))
    for v in range(N):
        if v==target: continue
        for pm in range(1<<N):
            if pm>>v&1: continue
            mean,var=pred_params(models,v,pm,row)
            z=row[v]-mean
            incfs[v,pm]=-0.5*(math.log(2*math.pi*var)+z*z/var)
    inc=np.zeros(len(dags))
    for v in range(N):
        if v!=target: inc+=incfs[v,parents[:,v]]
    return inc

def update_p_with_row(p,models,row,target):
    inc=predictive_increment(models,row,target)
    lw=np.log(p+1e-300)+inc
    lw-=lw.max(); q=np.exp(lw); q/=q.sum(); return q

def proposals(p,seed,step,swarm):
    em=edge_marginals(p); unc=4*em*(1-em)
    r=rng_for('v2','proposal',seed,step,swarm)
    c=[]
    incident=np.array([sum(unc[k] for k,(u,v) in enumerate(EDGES) if u==n or v==n) for n in range(N)])
    n=int(np.argmax(incident+r.normal(0,1e-9,N))); c.append(('INFOGAIN',n,float(r.choice([-2,2]))))
    k=int(np.argmax(unc+r.normal(0,1e-9,len(unc)))); c.append(('FALSIFY',EDGES[k][0],float(r.choice([-2,2]))))
    cheap=np.where(COSTS==COSTS.min())[0]; n=int(r.choice(cheap)); c.append(('CHEAPEST',n,float(r.choice([-1,1]))))
    mapm=int(dags[int(np.argmax(p))]); mapedges=np.array([(mapm>>kk)&1 for kk in range(len(EDGES))])
    k=int(np.argmax(np.abs(mapedges-em)+r.normal(0,1e-9,len(em)))); c.append(('RIVAL',EDGES[k][0],float(r.choice([-2,2]))))
    outunc=np.array([sum(unc[k] for k,(u,v) in enumerate(EDGES) if u==n) for n in range(N)])
    n=int(np.argmax(outunc+r.normal(0,1e-9,N))); c.append(('WEAKTIE',n,float(r.choice([-2,2]))))
    return c

def eig_score(p,models,action,seed,step,cid,sims=EIG_SIMS):
    _,target,setpoint=action
    h0=entropy(p); hs=[]
    r=rng_for('v2','planner',seed,step,cid)
    for s in range(sims):
        row=sim_row_from_posterior(p,models,target,setpoint,r)
        q=update_p_with_row(p,models,row,target)
        hs.append(entropy(q))
    return (h0-float(np.mean(hs)))/COSTS[target]

def run_arm(world,seed,width,controller='portfolio'):
    robs=rng_for('v2','obs',seed)
    data=env_sample(world,robs,OBS_N); targets=[None]*OBS_N
    fs,models=build_family_models(data,targets); p=posterior_from_fs(fs)
    spend=0; trace=[]; planner_sims=0
    while True:
        step=len(trace)
        if controller=='portfolio':
            allc=[]
            for sw in range(width): allc+=proposals(p,seed,step,sw)
        elif controller=='INFOGAIN': allc=[proposals(p,seed,step,0)[0]]
        elif controller=='CHEAPEST': allc=[proposals(p,seed,step,0)[2]]
        elif controller=='RANDOM':
            rr=rng_for('v2','random-controller',seed,step)
            affordable=np.where(COSTS<=BUDGET-spend)[0]
            if not len(affordable): break
            n=int(rr.choice(affordable)); allc=[('RANDOM',n,float(rr.choice([-2,-1,1,2])))]
        else: raise ValueError(controller)
        affordable=[a for a in allc if COSTS[a[1]]<=BUDGET-spend]
        if not affordable: break
        scores=[]
        for cid,a in enumerate(affordable):
            scores.append(eig_score(p,models,a,seed,step,cid)); planner_sims+=EIG_SIMS
        pick=int(np.argmax(scores)); role,target,setpoint=affordable[pick]
        renv=rng_for('v2','env',seed,step,target,setpoint)
        row=env_sample(world,renv,1,target,setpoint)[0]
        data=np.vstack([data,row]); targets.append(target); spend+=int(COSTS[target])
        fs,models=build_family_models(data,targets); p=posterior_from_fs(fs)
        trace.append({'step':step,'role':role,'target':int(target),'setpoint':setpoint,'cost':int(COSTS[target]),'eig_per_cost':float(scores[pick]),'spend':spend})
        if min(COSTS)>BUDGET-spend: break
    m=posterior_metrics(p,world.dag_mask)
    m.update({'spend':spend,'interventions':len(trace),'planner_sims':planner_sims,'trace':trace})
    return m
