import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s54_nodewise_residual_composition as s54

REGIMES=('linear','heteroskedastic')
GAMMAS=np.linspace(-1.5,2.5,17)
PRIOR_SD=1.0
ADJ_CLIP=12.0
EPS=1e-8


def logsumexp(x):
    x=np.asarray(x,float); m=float(np.max(x)); return m+math.log(float(np.sum(np.exp(x-m))))


def continuous_variance_posterior(data,targets):
    fs,models=b.build_family_models(data,targets)
    cs=fs.copy(); adjustments=[]; finite=True
    logprior=-0.5*(GAMMAS/PRIOR_SD)**2
    logprior-=logsumexp(logprior)
    for v in range(b.N):
        keep=np.asarray([t!=v for t in targets],bool)
        y=np.asarray(data[keep,v],float); n=len(y)
        if n<8: continue
        for pm in range(1<<b.N):
            if (pm>>v)&1: continue
            cols,mu,_=models[(v,pm)]
            X=data[keep][:,cols] if cols else np.empty((n,0))
            Xd=np.column_stack([np.ones(n),X]); pred=Xd@mu; res=y-pred
            z=np.log1p(np.abs(pred)); z=(z-z.mean())/(z.std()+1e-8)
            lls=[]
            for g in GAMMAS:
                scale=np.exp(np.clip(g*z,-8,8))
                sig2=max(float(np.mean((res*res)/scale)),EPS)
                var=sig2*scale
                ll=float(-0.5*np.sum(np.log(2*math.pi*var)+(res*res)/var))
                lls.append(ll)
            lls=np.asarray(lls,float)
            base=float(lls[int(np.argmin(np.abs(GAMMAS)))])
            marginal=logsumexp(lls+logprior)
            adj=float(np.clip(marginal-base,-ADJ_CLIP,ADJ_CLIP))
            cs[v,pm]=fs[v,pm]+adj; adjustments.append(adj)
            finite=finite and math.isfinite(adj)
    p=b.posterior_from_fs(cs)
    ok=finite and np.isfinite(p).all() and abs(float(p.sum())-1.0)<1e-8
    a=np.asarray(adjustments,float) if adjustments else np.asarray([0.0])
    diag={'mean_abs_adjustment':float(np.mean(np.abs(a))),'mean_adjustment':float(np.mean(a)),'fraction_abs_adjustment_ge_002':float(np.mean(np.abs(a)>=.02)),'max_abs_adjustment':float(np.max(np.abs(a)))}
    return p,bool(ok),diag


def world_row(external_seed):
    base=s54.world_base(external_seed)
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    p56,ok,diag=continuous_variance_posterior(data,targets)
    bm=b.posterior_metrics(np.asarray(base['p0'],float),base['true_mask']); cm=b.posterior_metrics(p56,base['true_mask'])
    out=dict(base)
    out.update({'p56':p56.tolist(),'p56_edge_delta_vs_baseline':float(cm['edge_error']-bm['edge_error']),'p56_brier_delta_vs_baseline':float(cm['brier']-bm['brier']),'variance_process_diag':diag,'p56_mechanics_ok':ok})
    return out


def generate(start,n_each):
    seeds=[]
    for rg in REGIMES: seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] and r['p56_mechanics_ok'] for r in rows)


def boot(x,reps=10000,seed=25656):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def evaluate(rows,seed):
    control=[]; cand=[]; control_b=[]; cand_b=[]; outer=[]; regs=[]; madj=[]; frac=[]; harms_c=harms_x=0
    for r in rows:
        op=bool(r['outer_promote'])
        c=float(r['s30_edge_delta_vs_baseline']) if op else 0.0; x=float(r['p56_edge_delta_vs_baseline']) if op else 0.0
        cb=float(r['s30_brier_delta_vs_baseline']) if op else 0.0; xb=float(r['p56_brier_delta_vs_baseline']) if op else 0.0
        control.append(c); cand.append(x); control_b.append(cb); cand_b.append(xb); outer.append(op); regs.append(r['regime'])
        madj.append(r['variance_process_diag']['mean_abs_adjustment']); frac.append(r['variance_process_diag']['fraction_abs_adjustment_ge_002'])
        harms_c += int(op and r['s30_edge_delta_vs_baseline']>.50); harms_x += int(op and r['p56_edge_delta_vs_baseline']>.50)
    control=np.asarray(control); cand=np.asarray(cand); diff=cand-control; outer=np.asarray(outer,bool)
    by={}
    for rg in REGIMES:
        idx=np.asarray([x==rg for x in regs],bool)
        by[rg]={'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),'candidate_hybrid_mean_edge_delta':float(np.mean(cand[idx])),'paired_mean_edge_difference':float(np.mean(diff[idx]))}
    return {'coverage':float(np.mean(outer)),'control_hybrid_mean_edge_delta':float(np.mean(control)),'candidate_hybrid_mean_edge_delta':float(np.mean(cand)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':boot(diff,seed=seed),'control_hybrid_mean_brier_delta':float(np.mean(control_b)),'candidate_hybrid_mean_brier_delta':float(np.mean(cand_b)),'control_promoted_large_harms':int(harms_c),'candidate_promoted_large_harms':int(harms_x),'mean_abs_family_score_adjustment':float(np.mean(madj)),'mean_fraction_adjusted_families':float(np.mean(frac)),'by_regime':by,'mechanics_ok':mechanics(rows,int(len(rows)/2))}


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']
    ok=(ev['mechanics_ok'] and ev['mean_abs_family_score_adjustment']>=.02 and ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.01 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.02 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.02 and ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and ev['candidate_hybrid_mean_brier_delta']<=.005)
    if validation or confirmation: ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.01
    if confirmation: ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.02
    return bool(ok)

if __name__=='__main__':
    me=generate(86501,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(86601,64); ev=evaluate(tr,25656); out['training']=ev
        if not qualifies(ev): out['disposition']='FALSIFIED_AT_TRAINING'
        else:
            va=generate(87001,32); vv=evaluate(va,25657); out['validation']=vv
            if not qualifies(vv,validation=True): out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(87501,64); cv=evaluate(co,25658); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,validation=True,confirmation=True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
