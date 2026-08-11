import argparse, json, math, random, statistics
ROLES=('info','falsify','cheap','novel')

def entropy(p):
    p=min(.999999,max(.000001,p)); return -(p*math.log2(p)+(1-p)*math.log2(1-p))
def sigmoid(x): return 1/(1+math.exp(-x))
def make_world(seed,n):
    rng=random.Random(seed); edges={}
    for i in range(n):
        for j in range(i+1,n):
            if rng.random()<min(.28,2.2/n): edges[(i,j)]=(-1 if rng.random()<.5 else 1)*(0.6+rng.random()*1.4)
    return edges

def candidate_score(node,beliefs,role,visits):
    cost=1+.08*node; score=0
    for (a,b),p in beliefs.items():
        if a!=node: continue
        h=entropy(p)
        if role=='info': score+=h/cost
        elif role=='falsify': score+=h*(0.75+abs(.5-p))/cost
        elif role=='cheap': score+=h/(cost*cost)
        elif role=='novel': score+=h/(cost*math.sqrt(1+visits.get(node,0)))
    return score

def run_episode(seed,n,budget,role_selector):
    rng=random.Random(seed+99991); truth=make_world(seed,n); beliefs={(i,j):.5 for i in range(n) for j in range(i+1,n)}; visits={}; info=spent=0; role_rewards=[]
    for step in range(budget):
        role=role_selector(step, role_rewards)
        if role=='random': node=rng.randrange(n)
        else: node=max(range(n),key=lambda k:candidate_score(k,beliefs,role,visits)+rng.random()*.01)
        visits[node]=visits.get(node,0)+1; cost=1+.08*node
        before=sum(entropy(p) for p in beliefs.values())
        for (a,b),old in list(beliefs.items()):
            if a!=node: continue
            present=(a,b) in truth; signal=(1 if present else -1)*1.5+rng.gauss(0,.65)
            beliefs[(a,b)]=sigmoid(math.log(old/(1-old))+signal)
        after=sum(entropy(p) for p in beliefs.values()); gain=max(0,before-after); reward=gain/cost
        role_rewards.append((role,reward)); info+=gain; spent+=cost
        if sum(.2<p<.8 for p in beliefs.values())<max(2,n/2): break
    acc=sum(((p>=.5)==((a,b) in truth)) for (a,b),p in beliefs.items())/len(beliefs)
    return {'accuracy':acc,'efficiency':info/max(.001,spent),'steps':step+1,'role_rewards':role_rewards}

def fixed(role): return lambda step,hist: role

def train_bandit(seeds,n,budget):
    stats={r:{'n':0,'sum':0.0} for r in ROLES}
    def selector(step,hist):
        total=sum(v['n'] for v in stats.values())
        untried=[r for r,v in stats.items() if v['n']==0]
        if untried: return untried[0]
        return max(ROLES,key=lambda r:stats[r]['sum']/stats[r]['n'] + 0.35*math.sqrt(math.log(total+1)/stats[r]['n']))
    rows=[]
    for s in seeds:
        row=run_episode(s,n,budget,selector); rows.append(row)
        for r,reward in row['role_rewards']:
            stats[r]['n']+=1; stats[r]['sum']+=reward
    means={r:(stats[r]['sum']/stats[r]['n'] if stats[r]['n'] else 0) for r in ROLES}
    best=max(means,key=means.get)
    return best,means,stats,rows

def summarize(rows):
    return {k:statistics.mean(r[k] for r in rows) for k in ('accuracy','efficiency','steps')}

def experiment(train_worlds,test_worlds,n,budget,seed):
    train_seeds=list(range(seed,seed+train_worlds)); test_seeds=list(range(seed+100000,seed+100000+test_worlds))
    best,means,stats,train_rows=train_bandit(train_seeds,n,budget)
    out={'meta_train':{'selected_role':best,'role_reward_means':means,'role_counts':{r:stats[r]['n'] for r in ROLES},'performance':summarize(train_rows)},'held_out':{}}
    for role in ('random','info','falsify','cheap','novel',best):
        label='adaptive_frozen' if role==best and 'adaptive_frozen' not in out['held_out'] else role
        rows=[run_episode(s,n,budget,fixed(role)) for s in test_seeds]
        out['held_out'][label]=summarize(rows)
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--train-worlds',type=int,default=150); ap.add_argument('--test-worlds',type=int,default=100); ap.add_argument('--variables',type=int,default=10); ap.add_argument('--budget',type=int,default=20); ap.add_argument('--seed',type=int,default=1000); ap.add_argument('--out',default='pilot_results_v2.json'); a=ap.parse_args()
    res=experiment(a.train_worlds,a.test_worlds,a.variables,a.budget,a.seed)
    with open(a.out,'w') as f: json.dump(res,f,indent=2)
    print(json.dumps(res,indent=2))
