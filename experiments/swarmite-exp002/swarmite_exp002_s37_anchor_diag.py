import json, numpy as np
from scipy.optimize import linprog
import swarmite_exp002_s36_stack_diag as s36
import swarmite_exp002_s32_modelset_diag as s32

RAW=s36.CLASSES
EXPERTS=('S30',)+tuple(RAW)

def dataset(seeds): return s36.dataset(seeds)

def exact_anchor(rows):
    cells=s32.CELLS; A=[]
    for cell in cells:
        z=[r for r in rows if r['cell']==cell]
        d=[0.0]+[float(np.mean([r['class_edge'][n]-r['s30_edge'] for r in z])) for n in RAW]
        A.append(np.r_[np.array(d,float),-1.0])
    c=np.r_[np.zeros(len(EXPERTS)),1.0]; Aeq=np.zeros((1,len(EXPERTS)+1)); Aeq[0,:len(EXPERTS)]=1.0
    res=linprog(c,A_ub=np.asarray(A),b_ub=np.zeros(len(A)),A_eq=Aeq,b_eq=np.array([1.0]),bounds=[(0,None)]*len(EXPERTS)+[(None,None)],method='highs')
    if not res.success: raise RuntimeError(res.message)
    w=res.x[:len(EXPERTS)]; weights={n:float(w[i]) for i,n in enumerate(EXPERTS)}; vals=[]; by={}
    for r in rows:
        d=sum(weights[n]*(0.0 if n=='S30' else r['class_edge'][n]-r['s30_edge']) for n in EXPERTS); vals.append(float(d))
    for cell in cells:
        by[cell]=float(np.mean([v for v,r in zip(vals,rows) if r['cell']==cell]))
    return {'weights':weights,'worst_cell_delta':float(max(by.values())),'mean_delta':float(np.mean(vals)),'by_cell_delta':by,'lp_t':float(res.x[-1])}

def run():
    tr=dataset(range(72201,72249)); va=dataset(range(72261,72297)); t=exact_anchor(tr); v=exact_anchor(va)
    if t['worst_cell_delta']<=-0.01 and v['worst_cell_delta']<=-0.01 and t['mean_delta']<0 and v['mean_delta']<0: disp='ANCHOR_RESOLVES_FEASIBILITY'
    elif -0.01<=t['worst_cell_delta']<=0.001 and -0.01<=v['worst_cell_delta']<=0.001 and (t['weights']['S30']>=0.90 or v['weights']['S30']>=0.90): disp='ANCHOR_ONLY_SAFE'
    elif (t['worst_cell_delta']<=-0.01)!=(v['worst_cell_delta']<=-0.01): disp='ANCHOR_TRANSFER_UNSTABLE'
    else: disp='MIXED_ANCHOR_RESULT'
    return {'training':t,'validation':v,'disposition':disp}
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
