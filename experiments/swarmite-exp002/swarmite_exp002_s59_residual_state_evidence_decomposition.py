import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s58_intervention_conditional_residual_process as s58

REGIMES=('linear','heteroskedastic')
EPS=1e-12


def true_parent_mask(true_mask,v):
    pm=0
    for k,(u,w) in enumerate(b.EDGES):
        if w==v and ((int(true_mask)>>k)&1): pm |= 1<<u
    return pm


def family_adjustments(data,targets):
    fs,models=b.build_family_models(data,targets)
    cs=fs.copy(); node_adjs={v:[] for v in range(b.N)}
    targets=np.asarray(targets,dtype=object)
    finite=True
    for v in range(b.N):
        keep=np.asarray([t!=v for t in targets],bool); y=np.asarray(data[keep,v],float); labs=targets[keep]; n=len(y)
        if n<8: continue
        for pm in range(1<<b.N):
            if (pm>>v)&1: continue
            cols,mu,_=models[(v,pm)]
            X=data[keep][:,cols] if cols else np.empty((n,0)); Xd=np.column_stack([np.ones(n),X]); pred=Xd@mu; res=y-pred
            sg=s58.robust_scale(res); ll0=s58.t_loglik(res,np.full(n,sg)); scale=np.full(n,sg,float); extra=0
            unique_labs=[]
            for lab in labs.tolist():
                if not any((lab is x) or (lab==x) for x in unique_labs): unique_labs.append(lab)
            for lab in unique_labs:
                idx=np.asarray([(x is lab) or (x==lab) for x in labs],bool); ng=int(idx.sum())
                if ng<3: continue
                sl=s58.robust_scale(res[idx]); w=ng/(ng+s58.SHRINK_K)
                logs=(1-w)*math.log(sg)+w*math.log(sl); scale[idx]=math.exp(logs); extra+=1
            ll1=s58.t_loglik(res,scale); penalty=0.5*max(extra-1,0)*math.log(max(n,2))
            adj=float(np.clip(ll1-ll0-penalty,-s58.ADJ_CLIP,s58.ADJ_CLIP))
            cs[v,pm]=fs[v,pm]+adj; node_adjs[v].append((pm,adj)); finite=finite and math.isfinite(adj)
    return fs,cs,node_adjs,bool(finite)


def margin(scores,v,tpm):
    vals=[]
    for pm in range(1<<b.N):
        if (pm>>v)&1 or pm==tpm: continue
        vals.append(float(scores[v,pm]))
    return float(scores[v,tpm]-max(vals))


def node_rows(external_seed):
    base=s54.world_base(external_seed); reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,cs,node_adjs,ok=family_adjustments(data,targets)
    out=[]
    for v in range(b.N):
        tpm=true_parent_mask(base['true_mask'],v)
        a0=margin(fs,v,tpm); a1=margin(cs,v,tpm); ad=np.asarray([x[1] for x in node_adjs[v]],float)
        if len(ad)==0: ad=np.asarray([0.0])
        out.append({
            'external_seed':int(external_seed),'regime':reg,'node':int(v),'true_parent_mask':int(tpm),
            'anchor_margin':a0,'anchor_rank_error':bool(a0<0),'s58_margin':a1,'correction_delta':float(a1-a0),
            's58_repaired':bool(a0<0 and a1>=0),'mean_abs_adjustment':float(np.mean(np.abs(ad))),
            'std_adjustment':float(np.std(ad)),'range_adjustment':float(np.max(ad)-np.min(ad)),
            'fraction_abs_adjustment_ge_002':float(np.mean(np.abs(ad)>=.02)),
            'trace_identical':bool(base['trace_identical']),'spend':int(base['spend']),'finite':bool(base['finite'] and ok)
        })
    return out


def selected(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return seeds


def generate(start,n_each):
    rows=[]
    for s in selected(start,n_each): rows += node_rows(s)
    return rows


def mechanics(rows,n_each):
    expected=n_each*2*b.N
    return len(rows)==expected and all(r['trace_identical'] and r['spend']<=15 and r['finite'] for r in rows)


def auc(y,s):
    y=np.asarray(y,bool); s=np.asarray(s,float); pos=np.where(y)[0]; neg=np.where(~y)[0]
    if len(pos)==0 or len(neg)==0: return float('nan')
    wins=0.0
    for i in pos:
        wins += float(np.sum(s[i]>s[neg])) + .5*float(np.sum(s[i]==s[neg]))
    return float(wins/(len(pos)*len(neg)))


def corr(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    if len(x)<2 or np.std(x)<EPS or np.std(y)<EPS: return 0.0
    return float(np.corrcoef(x,y)[0,1])


def bootstrap_metric(rows,key,reps=4000,seed=25959):
    rr=np.random.default_rng(seed); n=len(rows); vals=[]
    for _ in range(reps):
        samp=[rows[i] for i in rr.integers(0,n,n)]
        if key=='best_auc':
            y=[r['anchor_rank_error'] for r in samp]
            aa=[auc(y,[r[k] for r in samp]) for k in ('mean_abs_adjustment','std_adjustment','range_adjustment','fraction_abs_adjustment_ge_002')]
            vals.append(np.nanmax(aa))
        elif key=='error_delta':
            er=[r['correction_delta'] for r in samp if r['anchor_rank_error']]
            if er: vals.append(float(np.mean(er)))
    if not vals: return [float('nan'),float('nan')]
    return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]


def summarize(rows):
    y=[r['anchor_rank_error'] for r in rows]; severity=[-r['anchor_margin'] for r in rows]
    feats=('mean_abs_adjustment','std_adjustment','range_adjustment','fraction_abs_adjustment_ge_002')
    aucs={k:auc(y,[r[k] for r in rows]) for k in feats}; cors={k:corr([r[k] for r in rows],severity) for k in feats}
    errs=[r for r in rows if r['anchor_rank_error']]
    best=max((v,k) for k,v in aucs.items() if math.isfinite(v)) if any(math.isfinite(v) for v in aucs.values()) else (float('nan'),None)
    out={
        'n_nodes':len(rows),'n_anchor_rank_errors':len(errs),'anchor_rank_error_rate':float(np.mean(y)),
        'feature_auc':aucs,'feature_severity_correlation':cors,'best_auc':float(best[0]),'best_feature':best[1],
        'best_auc_bootstrap95':bootstrap_metric(rows,'best_auc'),
        'mean_correction_delta_error_nodes':float(np.mean([r['correction_delta'] for r in errs])) if errs else float('nan'),
        'correction_delta_error_nodes_bootstrap95':bootstrap_metric(rows,'error_delta'),
        'fraction_positive_correction_error_nodes':float(np.mean([r['correction_delta']>0 for r in errs])) if errs else float('nan'),
        'fraction_repaired_error_nodes':float(np.mean([r['s58_repaired'] for r in errs])) if errs else float('nan')
    }
    return out


def evaluate(rows):
    overall=summarize(rows); by={}
    for rg in REGIMES: by[rg]=summarize([r for r in rows if r['regime']==rg])
    overall['by_regime']=by; return overall


def disposition(ev):
    a=ev['best_auc']; d=ev['mean_correction_delta_error_nodes']; p=ev['fraction_positive_correction_error_nodes']; repaired=ev['fraction_repaired_error_nodes']
    if not math.isfinite(a) or a<.65: return 'EVIDENCE_NOT_ALIGNED'
    if d<=0 or p<.55: return 'EVIDENCE_ALIGNED_DIRECTION_WRONG'
    if repaired>=.50: return 'EVIDENCE_ALIGNED_CORRECTION_SUPPORTED'
    return 'EVIDENCE_ALIGNED_PARTIAL_CORRECTION'

if __name__=='__main__':
    me=generate(92001,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        rows=generate(92101,64); ev=evaluate(rows); out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))
