import json, numpy as np
from scipy.optimize import linprog
import swarmite_exp002_s35_stack as s35
import swarmite_exp002_s32_modelset_diag as s32

CLASSES=s35.CLASSES


def dataset(seeds):
    rows=[]
    for seed in seeds:
        r=s35.components(seed)
        rows.append({'seed':r['seed'],'cell':r['cell'],'class_edge':{n:float(r['class_metrics'][n]['edge_error']) for n in CLASSES},'s30_edge':float(r['s30']['edge_error'])})
    return rows


def exact_minimax(rows):
    cells=s32.CELLS; A=[]
    for cell in cells:
        z=[r for r in rows if r['cell']==cell]
        d=np.array([np.mean([r['class_edge'][n]-r['s30_edge'] for r in z]) for n in CLASSES],float)
        # d @ w - t <= 0
        A.append(np.r_[d,-1.0])
    c=np.r_[np.zeros(len(CLASSES)),1.0]
    Aeq=np.zeros((1,len(CLASSES)+1)); Aeq[0,:len(CLASSES)]=1.0
    res=linprog(c,A_ub=np.asarray(A),b_ub=np.zeros(len(A)),A_eq=Aeq,b_eq=np.array([1.0]),bounds=[(0,None)]*len(CLASSES)+[(None,None)],method='highs')
    if not res.success: raise RuntimeError(res.message)
    w=res.x[:len(CLASSES)]; weights={n:float(w[i]) for i,n in enumerate(CLASSES)}
    ev=evaluate_weights(rows,weights)
    return {'weights':weights,'lp_worst_cell_delta':float(res.x[-1]),**ev}


def evaluate_weights(rows,weights):
    vals=[]; by={}
    for r in rows:
        d=sum(weights[n]*(r['class_edge'][n]-r['s30_edge']) for n in CLASSES); vals.append(float(d))
    for cell in s32.CELLS:
        z=[v for v,r in zip(vals,rows) if r['cell']==cell]; by[cell]=float(np.mean(z))
    return {'mean_delta':float(np.mean(vals)),'worst_cell_delta':float(max(by.values())),'by_cell_delta':by}


def cell_best(rows):
    out={}
    for cell in s32.CELLS:
        z=[r for r in rows if r['cell']==cell]
        means={n:float(np.mean([r['class_edge'][n]-r['s30_edge'] for r in z])) for n in CLASSES}
        best=min(means,key=means.get); out[cell]={'best_class':best,'best_mean_delta':means[best],'all_class_mean_delta':means}
    return out


def oracle_coverage(rows):
    return float(np.mean([any(r['class_edge'][n] < r['s30_edge'] for n in CLASSES) for r in rows]))


def run():
    tr=dataset(range(72201,72249)); va=dataset(range(72261,72297))
    tmm=exact_minimax(tr); vmm=exact_minimax(va); tcross=evaluate_weights(va,tmm['weights']); vcross=evaluate_weights(tr,vmm['weights']); tb=cell_best(tr); vb=cell_best(va); toc=oracle_coverage(tr); voc=oracle_coverage(va)
    approx=json.load(open('EXP-002S35_TRAINING_RESULT.json'))['objective']['worst_cell_delta']
    every_cell_neg=all(tb[c]['best_mean_delta']<0 and vb[c]['best_mean_delta']<0 for c in s32.CELLS)
    if tmm['worst_cell_delta']<0 and approx>=0: disp='APPROXIMATE_SEARCH_FAILURE'
    elif tmm['worst_cell_delta']<0 and vmm['worst_cell_delta']<0 and tcross['worst_cell_delta']>0.05: disp='TRAIN_DISTRIBUTION_INSTABILITY'
    elif tmm['worst_cell_delta']>=0 and vmm['worst_cell_delta']>=0 and every_cell_neg and toc>=0.80 and voc>=0.80: disp='REGIME_HETEROGENEITY_FIXED_STACK_INSUFFICIENT'
    elif toc<0.80 or voc<0.80 or not every_cell_neg: disp='MODEL_SET_INSUFFICIENCY'
    else: disp='MIXED_FAILURE'
    return {'training_exact':tmm,'validation_exact':vmm,'training_weights_on_validation':tcross,'validation_weights_on_training':vcross,'training_cell_best':tb,'validation_cell_best':vb,'training_oracle_coverage':toc,'validation_oracle_coverage':voc,'s35_approx_training_worst_cell_delta':float(approx),'every_cell_has_negative_class_both_splits':bool(every_cell_neg),'disposition':disp}

if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
