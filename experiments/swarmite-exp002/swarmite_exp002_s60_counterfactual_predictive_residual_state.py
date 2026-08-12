import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s58_intervention_conditional_residual_process as s58
import swarmite_exp002_s59_residual_state_evidence_decomposition as s59

REGIMES=('linear','heteroskedastic')
EPS=1e-12
FEATURES=(
    'selected_cv_mean_loss','selected_cv_std_loss','selected_cv_worst_loss',
    'cv_rank_volatility','cv_competitor_advantage','state_loss_range'
)


def legal_pms(v):
    return [pm for pm in range(1<<b.N) if not ((pm>>v)&1)]


def key_lab(x):
    if x is None: return 'OBS'
    if isinstance(x,(int,np.integer)): return 'I:'+str(int(x))
    if isinstance(x,(float,np.floating)) and np.isnan(x): return 'OBS'
    return 'L:'+repr(x)


def fit_loss(data, y, rows_train, rows_test, pm, v):
    cols=[u for u in range(b.N) if ((pm>>u)&1) and u!=v]
    Xt=data[rows_train][:,cols] if cols else np.empty((int(np.sum(rows_train)),0))
    Xh=data[rows_test][:,cols] if cols else np.empty((int(np.sum(rows_test)),0))
    yt=y[rows_train]; yh=y[rows_test]
    if len(yt)<5 or len(yh)<1: return float('nan')
    A=np.column_stack([np.ones(len(yt)),Xt]); Ah=np.column_stack([np.ones(len(yh)),Xh])
    try:
        coef=np.linalg.lstsq(A,yt,rcond=None)[0]
    except np.linalg.LinAlgError:
        return float('nan')
    rtr=yt-A@coef; scale=max(float(s58.robust_scale(rtr)),1e-6)
    rh=yh-Ah@coef
    z=np.clip(rh/scale,-20.0,20.0)
    return float(np.mean(z*z))


def predictive_features(data,targets,fs,v):
    targets=np.asarray(targets,dtype=object)
    keep_global=np.asarray([not ((t==v) if isinstance(t,(int,np.integer)) else False) for t in targets],bool)
    idx_global=np.where(keep_global)[0]
    y_all=np.asarray(data[:,v],float)
    labs=[key_lab(targets[i]) for i in idx_global]
    groups=[]
    for lab in labs:
        if lab not in groups: groups.append(lab)
    pms=legal_pms(v)
    sel=max(pms,key=lambda pm: float(fs[v,pm]))
    selected_losses=[]; rank_disagree=[]; comp_adv=[]
    for lab in groups:
        test_idx=np.asarray([i for i in idx_global if key_lab(targets[i])==lab],dtype=int)
        train_idx=np.asarray([i for i in idx_global if key_lab(targets[i])!=lab],dtype=int)
        if len(test_idx)<1 or len(train_idx)<8: continue
        train_mask=np.zeros(len(data),bool); train_mask[train_idx]=True
        test_mask=np.zeros(len(data),bool); test_mask[test_idx]=True
        losses={}
        for pm in pms:
            ll=fit_loss(data,y_all,train_mask,test_mask,pm,v)
            if math.isfinite(ll): losses[pm]=ll
        if sel not in losses or len(losses)<2: continue
        sl=losses[sel]
        others=[x for pm,x in losses.items() if pm!=sel]
        best_other=min(others) if others else sl
        selected_losses.append(sl)
        rank_disagree.append(float(best_other < sl))
        comp_adv.append(max(0.0,sl-best_other))
    if not selected_losses:
        selected_losses=[0.0]; rank_disagree=[0.0]; comp_adv=[0.0]
    a=np.asarray(selected_losses,float)
    return sel,{
        'selected_cv_mean_loss':float(np.mean(a)),
        'selected_cv_std_loss':float(np.std(a)),
        'selected_cv_worst_loss':float(np.max(a)),
        'cv_rank_volatility':float(np.mean(rank_disagree)),
        'cv_competitor_advantage':float(np.mean(comp_adv)),
        'state_loss_range':float(np.max(a)-np.min(a)),
        'n_cv_states':int(len(a)),
    }


def node_rows(external_seed):
    base=s54.world_base(external_seed)
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,_=b.build_family_models(data,targets)
    out=[]
    for v in range(b.N):
        tpm=s59.true_parent_mask(base['true_mask'],v)
        am=s59.margin(fs,v,tpm)
        sel,feat=predictive_features(data,targets,fs,v)
        row={
            'external_seed':int(external_seed),'regime':reg,'node':int(v),
            'true_parent_mask':int(tpm),'anchor_selected_parent_mask':int(sel),
            'anchor_margin':float(am),'anchor_rank_error':bool(am<0),
            'trace_identical':bool(base['trace_identical']),'spend':int(base['spend']),
            'finite':bool(base['finite'])
        }
        row.update(feat)
        row['finite']=bool(row['finite'] and all(math.isfinite(float(row[k])) for k in FEATURES))
        out.append(row)
    return out


def selected(start,n_each):
    return s59.selected(start,n_each)


def generate(start,n_each):
    rows=[]
    for seed in selected(start,n_each): rows.extend(node_rows(seed))
    return rows


def mechanics(rows,n_each):
    return len(rows)==n_each*2*b.N and all(r['trace_identical'] and r['spend']<=15 and r['finite'] for r in rows)


def auc(y,s):
    return s59.auc(y,s)


def corr(x,y):
    return s59.corr(x,y)


def summarize(rows):
    y=[r['anchor_rank_error'] for r in rows]
    severity=[-r['anchor_margin'] for r in rows]
    aucs={k:auc(y,[r[k] for r in rows]) for k in FEATURES}
    cors={k:corr([r[k] for r in rows],severity) for k in FEATURES}
    finite=[(v,k) for k,v in aucs.items() if math.isfinite(v)]
    best=max(finite) if finite else (float('nan'),None)
    return {
        'n_nodes':len(rows),'n_anchor_rank_errors':int(sum(y)),
        'anchor_rank_error_rate':float(np.mean(y)) if y else float('nan'),
        'feature_auc':aucs,'feature_severity_correlation':cors,
        'best_auc':float(best[0]),'best_feature':best[1],
        'mean_cv_states':float(np.mean([r['n_cv_states'] for r in rows])) if rows else 0.0,
    }


def bootstrap_best_auc(rows,reps=3000,seed=26060):
    rr=np.random.default_rng(seed); n=len(rows); vals=[]
    for _ in range(reps):
        samp=[rows[i] for i in rr.integers(0,n,n)]
        y=[r['anchor_rank_error'] for r in samp]
        aa=[auc(y,[r[k] for r in samp]) for k in FEATURES]
        aa=[x for x in aa if math.isfinite(x)]
        if aa: vals.append(max(aa))
    if not vals: return [float('nan'),float('nan')]
    return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]


def evaluate(rows):
    overall=summarize(rows)
    overall['best_auc_bootstrap95']=bootstrap_best_auc(rows)
    overall['by_regime']={rg:summarize([r for r in rows if r['regime']==rg]) for rg in REGIMES}
    return overall


def disposition(ev):
    a=float(ev['best_auc']); lo=float(ev['best_auc_bootstrap95'][0])
    if not math.isfinite(a) or a<0.60: return 'PREDICTIVE_STATE_NOT_ALIGNED'
    if a>=0.65 and math.isfinite(lo) and lo>=0.55: return 'PREDICTIVE_STATE_ALIGNED'
    return 'PREDICTIVE_STATE_WEAK_SIGNAL'


if __name__=='__main__':
    me=generate(93001,2)
    out={'mechanics':{'passed':mechanics(me,2)}}
    if out['mechanics']['passed']:
        rows=generate(93101,64); ev=evaluate(rows)
        out['diagnostic']=ev; out['disposition']=disposition(ev)
    else:
        out['disposition']='BLOCKED_MECHANICS'
    print(json.dumps(out,separators=(',',':')))
