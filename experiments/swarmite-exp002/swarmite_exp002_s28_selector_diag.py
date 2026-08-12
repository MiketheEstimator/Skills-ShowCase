import json, math, numpy as np
from pathlib import Path

FEATURES=('D_robust','log_tail','PPC_nonlinear')

def auc(y,s):
    y=np.asarray(y,int); s=np.asarray(s,float); pos=np.where(y==1)[0]; neg=np.where(y==0)[0]
    if len(pos)==0 or len(neg)==0: return float('nan')
    wins=0.0
    for i in pos:
        for j in neg:
            wins += 1.0 if s[i]>s[j] else (0.5 if s[i]==s[j] else 0.0)
    return float(wins/(len(pos)*len(neg)))

def fit_logistic(X,y,iters=3000,lr=.05,l2=.10):
    X=np.asarray(X,float); y=np.asarray(y,float); w=np.zeros(X.shape[1]); b=0.0
    for _ in range(iters):
        z=np.clip(X@w+b,-30,30); p=1/(1+np.exp(-z)); e=p-y
        w -= lr*((X.T@e)/len(y)+l2*w); b -= lr*float(np.mean(e))
    return w,b

def cv_probs(X,y,seeds,folds=8):
    X=np.asarray(X,float); y=np.asarray(y,int); seeds=np.asarray(seeds,int); order=np.argsort(seeds); fold=np.empty(len(y),int)
    for k,idx in enumerate(order): fold[idx]=k%folds
    probs=np.zeros(len(y))
    for f in range(folds):
        tr=fold!=f; te=fold==f; mu=X[tr].mean(axis=0); sd=X[tr].std(axis=0); sd=np.where(sd<1e-12,1.0,sd)
        Xt=(X[tr]-mu)/sd; Xe=(X[te]-mu)/sd; w,b=fit_logistic(Xt,y[tr]); z=np.clip(Xe@w+b,-30,30); probs[te]=1/(1+np.exp(-z))
    return probs

def metrics(y,p):
    y=np.asarray(y,int); p=np.asarray(p,float); pred=(p>=.5).astype(int)
    tp=int(np.sum((pred==1)&(y==1))); tn=int(np.sum((pred==0)&(y==0))); fp=int(np.sum((pred==1)&(y==0))); fn=int(np.sum((pred==0)&(y==1)))
    tpr=tp/max(1,tp+fn); tnr=tn/max(1,tn+fp)
    return {'auc':auc(y,p),'balanced_accuracy':float((tpr+tnr)/2),'tp':tp,'tn':tn,'fp':fp,'fn':fn}

def run(path='EXP-002S27_CONFIRMATION_RESULT.json'):
    obj=json.loads(Path(path).read_text()); rows=obj['rows']; seeds=[r['seed'] for r in rows]; y=np.array([int(r['edge_delta']<0) for r in rows])
    X=np.array([[r['D_robust'],math.log1p(max(0.0,r['PPC_tail'])),r['PPC_nonlinear']] for r in rows],float)
    single={FEATURES[j]:auc(y,X[:,j]) for j in range(3)}
    pt=cv_probs(X[:,1:2],y,seeds); pm=cv_probs(X,y,seeds); mt=metrics(y,pt); mm=metrics(y,pm)
    pred=(pm>=.5).astype(int); strata={}
    for reg in sorted(set(r['regime'] for r in rows)):
        idx=[i for i,r in enumerate(rows) if r['regime']==reg]; yy=y[idx]; pp=pred[idx]
        strata[reg]={'n':len(idx),'beneficial':int(yy.sum()),'false_negative':int(np.sum((pp==0)&(yy==1))),'false_positive':int(np.sum((pp==1)&(yy==0)))}
    groups={}
    for label,val in [('beneficial',1),('not_beneficial',0)]:
        ix=np.where(y==val)[0]; groups[label]={FEATURES[j]:{'median':float(np.median(X[ix,j])),'mean':float(np.mean(X[ix,j]))} for j in range(3)}
    corr=np.corrcoef(X,rowvar=False).tolist()
    promising=bool(mm['auc']>=.70 and mm['auc']>=mt['auc']+.05)
    return {'n':len(rows),'single_feature_auc':single,'tail_only_cv':mt,'multivariate_cv':mm,'auc_gain':float(mm['auc']-mt['auc']),'regime_errors':strata,'feature_groups':groups,'feature_corr':corr,'promising_representation':promising}

if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
