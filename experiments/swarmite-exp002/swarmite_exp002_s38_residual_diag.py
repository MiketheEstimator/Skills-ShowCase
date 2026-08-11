import json, numpy as np
import swarmite_exp002_s35_stack as s35
import swarmite_exp002_s32_modelset_diag as s32

SPECIALISTS=('TG','TT','SG','ST','AG','AT')

def dataset(seeds):
    rows=[]
    for seed in seeds:
        r=s35.components(seed)
        rows.append({'seed':r['seed'],'cell':r['cell'],'s30_edge':float(r['s30']['edge_error']),'class_edge':{n:float(r['class_metrics'][n]['edge_error']) for n in SPECIALISTS}})
    return rows

def stats(rows):
    out={}
    for n in SPECIALISTS:
        d=np.array([r['class_edge'][n]-r['s30_edge'] for r in rows],float); wins=d<0; losses=d>=0; harms=d>0.5
        by={}
        for c in s32.CELLS:
            z=np.array([r['class_edge'][n]-r['s30_edge'] for r in rows if r['cell']==c],float); by[c]=float(np.mean(z))
        lossvals=d[losses]
        out[n]={'mean_edge_delta':float(np.mean(d)),'win_rate':float(np.mean(wins)),'mean_improvement_when_win':float(np.mean(-d[wins])) if np.any(wins) else 0.0,'mean_harm_when_loss':float(np.mean(d[losses])) if np.any(losses) else 0.0,'large_harm_rate':float(np.mean(harms)),'p90_harm_among_losses':float(np.quantile(lossvals,0.9)) if len(lossvals) else 0.0,'by_cell_mean_delta':by}
    oracle=[]; classes=[]
    for r in rows:
        best=min(SPECIALISTS,key=lambda n:r['class_edge'][n]); gain=max(0.0,r['s30_edge']-r['class_edge'][best]); oracle.append(gain); classes.append(best)
    oc={n:classes.count(n) for n in SPECIALISTS}
    return {'specialists':out,'oracle_coverage':float(np.mean(np.array(oracle)>0)),'mean_oracle_improvement':float(np.mean(oracle)),'oracle_class_counts':oc}

def run():
    tr=stats(dataset(range(72201,72249))); va=stats(dataset(range(72261,72297)))
    safe=[]
    for n in SPECIALISTS:
        a,b=tr['specialists'][n],va['specialists'][n]
        if a['mean_edge_delta']<=-0.10 and b['mean_edge_delta']<=-0.10 and a['win_rate']>=0.70 and b['win_rate']>=0.70 and a['large_harm_rate']<=0.05 and b['large_harm_rate']<=0.05: safe.append(n)
    if safe: disp='SAFE_SPECIALIST_IDENTIFIED'
    elif tr['oracle_coverage']>=0.80 and va['oracle_coverage']>=0.80 and tr['mean_oracle_improvement']>=0.20 and va['mean_oracle_improvement']>=0.20: disp='HETEROGENEOUS_RESIDUAL_VALUE'
    elif tr['oracle_coverage']<0.80 or va['oracle_coverage']<0.80 or tr['mean_oracle_improvement']<0.20 or va['mean_oracle_improvement']<0.20: disp='LOW_RESIDUAL_VALUE'
    else: disp='MIXED_RESIDUAL_VALUE'
    return {'training':tr,'validation':va,'safe_specialists':safe,'disposition':disp}
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
