import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s25_heterogeneous as s25

FOLDS=5

def auc(y,s):
    y=np.asarray(y,int); s=np.asarray(s,float); pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
    if len(pos)==0 or len(neg)==0: return float('nan')
    z=0.0
    for i in pos:
      for j in neg: z += 1.0 if s[i]>s[j] else (0.5 if s[i]==s[j] else 0.0)
    return float(z/(len(pos)*len(neg)))

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

def baseline_fit_score(data,targets,v,pm,indices):
    idx=[i for i in indices if targets[i]!=v]; y=data[idx,v]; cols=[u for u in range(b.N) if pm>>u&1]
    X=data[idx][:,cols] if cols else np.empty((len(y),0)); Xd=np.column_stack([np.ones(len(y)),X]); A=np.eye(Xd.shape[1])/b.TAU2+Xd.T@Xd; Ainv=np.linalg.inv(A); rhs=Xd.T@y; mu=Ainv@rhs
    quad=float(y@y-rhs@mu); _,ld=np.linalg.slogdet(A); logdetC=float(ld+Xd.shape[1]*math.log(b.TAU2)); sc=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad)
    return float(sc),(cols,mu,Ainv)

def baseline_logpred(model,row,v):
    cols,mu,Ainv=model; x=np.array([1.0]+[row[u] for u in cols]); mean=float(x@mu); var=max(1e-12,float(1+x@Ainv@x)); z=float(row[v]-mean); return -0.5*(math.log(2*math.pi*var)+z*z/var)

def robust_fit_score(data,targets,v,pm,indices):
    idx=[i for i in indices if targets[i]!=v]; y=data[idx,v]; cols=[u for u in range(b.N) if pm>>u&1]; X=np.tanh(data[idx][:,cols]) if cols else np.empty((len(y),0)); X=np.column_stack([np.ones(len(y)),X]); sc,beta=s23.fit_score(X,y); return float(sc),(cols,beta)

def robust_logpred(model,row,v):
    cols,beta=model; x=np.array([1.0]+[math.tanh(row[u]) for u in cols]); r=float(row[v]-x@beta); return float(s23.t_logpdf(np.array([r]))[0])

def world_adequacy(seed):
    w=b.gen_world(seed); c,data,targets,p0,reg=s25.run_control(w,seed); n=len(data); base_total=0.0; robust_total=0.0
    all_idx=list(range(n))
    for fold in range(FOLDS):
      te=[i for i in all_idx if i%FOLDS==fold]; tr=[i for i in all_idx if i%FOLDS!=fold]
      for v in range(b.N):
        pms=[pm for pm in range(1<<b.N) if not (pm>>v&1)]
        bs=[]; bm=[]; rs=[]; rm=[]
        for pm in pms:
          sc,m=baseline_fit_score(data,targets,v,pm,tr); bs.append(sc); bm.append(m)
          sc2,m2=robust_fit_score(data,targets,v,pm,tr); rs.append(sc2); rm.append(m2)
        ib=int(np.argmax(bs)); ir=int(np.argmax(rs)); mb=bm[ib]; mr=rm[ir]
        for i in te:
          if targets[i]==v: continue
          base_total += baseline_logpred(mb,data[i],v); robust_total += robust_logpred(mr,data[i],v)
    return {'seed':int(seed),'regime':reg,'baseline_cv_logscore':float(base_total),'robust_cv_logscore':float(robust_total),'ADEQ':float(robust_total-base_total),'spend':int(c['spend']),'posterior_sum':float(p0.sum())}

def run():
    ref=json.loads(Path('EXP-002S27_CONFIRMATION_RESULT.json').read_text()); truth={int(r['seed']):r for r in ref['rows']}; rows=[]
    for seed in range(71300,71396):
      a=world_adequacy(seed); rr=truth[seed]; a.update({'edge_delta':float(rr['edge_delta']),'brier_delta':float(rr['brier_delta']),'robust_beneficial':int(rr['edge_delta']<0),'robust_large_harm':int(rr['edge_delta']>0.50)}); rows.append(a)
    y=[r['robust_beneficial'] for r in rows]; score=[r['ADEQ'] for r in rows]; pred=[int(x>0) for x in score]; tp=sum(p==1 and yy==1 for p,yy in zip(pred,y)); tn=sum(p==0 and yy==0 for p,yy in zip(pred,y)); fp=sum(p==1 and yy==0 for p,yy in zip(pred,y)); fn=sum(p==0 and yy==1 for p,yy in zip(pred,y)); bal=.5*(tp/max(1,tp+fn)+tn/max(1,tn+fp))
    by={}
    for reg in s25.REGIMES:
      z=[r for r in rows if r['regime']==reg]; by[reg]={'n':len(z),'median_ADEQ':float(np.median([r['ADEQ'] for r in z])),'mean_ADEQ':float(np.mean([r['ADEQ'] for r in z])),'beneficial':sum(r['robust_beneficial'] for r in z),'zero_rule_fp':sum(r['ADEQ']>0 and not r['robust_beneficial'] for r in z),'zero_rule_fn':sum(r['ADEQ']<=0 and r['robust_beneficial'] for r in z)}
    sm={'n':len(rows),'auc':auc(y,score),'balanced_accuracy_zero':float(bal),'tp':tp,'tn':tn,'fp':fp,'fn':fn,'spearman_ADEQ_edge_delta':spearman(score,[r['edge_delta'] for r in rows]),'all_finite':all(np.isfinite(r['ADEQ']) for r in rows),'spend_ok':all(r['spend']<=15 for r in rows),'posterior_normalized':all(abs(r['posterior_sum']-1)<1e-8 for r in rows),'by_regime':by}
    sm['promising']=bool(sm['auc']>=.70 and sm['balanced_accuracy_zero']>=.65 and sm['all_finite'] and sm['spend_ok'] and sm['posterior_normalized'])
    return {'rows':rows,'summary':sm}

if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
