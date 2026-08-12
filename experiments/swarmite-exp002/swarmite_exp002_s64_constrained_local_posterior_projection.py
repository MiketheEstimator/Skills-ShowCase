import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s54_nodewise_residual_composition as s54
import swarmite_exp002_s59_residual_state_evidence_decomposition as s59
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s61_bounded_predictive_state_structural_correction as s61
import swarmite_exp002_s62_posterior_disagreement_parent_proposal as s62

REGIMES=('linear','heteroskedastic'); RIDGE=5.; MAX_RHO=.50; CYCLES=40
FEATURES=s62.FEATURES

def dag_pm(mask,v): return s61.dag_parent_mask(mask,v)

def local_marginal(p,v,pms):
    z=np.zeros(len(pms)); ix={pm:i for i,pm in enumerate(pms)}
    for j,d in enumerate(b.dags): z[ix[dag_pm(d,v)]] += p[j]
    z=np.clip(z,1e-12,None); return z/z.sum()

def s62_detail(data,targets,fs,v):
    pms=s62.legal_pms(v); qfull=s62.softmax_scores(fs,v,pms); sel=pms[int(np.argmax(qfull))]
    idx=np.asarray([i for i,t in enumerate(targets) if not (isinstance(t,(int,np.integer)) and int(t)==v)],int); labs=[]
    for i in idx:
        lab=s60.key_lab(targets[i]);
        if lab not in labs: labs.append(lab)
    qs=[]; maps=[]; margins=[]
    for lab in labs:
        tr=np.asarray([i for i in idx if s60.key_lab(targets[i])!=lab],int)
        if len(tr)<8: continue
        try: fsi,_=b.build_family_models(np.asarray(data[tr],float),np.asarray(targets,dtype=object)[tr])
        except Exception: continue
        qi=s62.softmax_scores(fsi,v,pms)
        if not np.all(np.isfinite(qi)): continue
        qs.append(qi); maps.append(pms[int(np.argmax(qi))]); ss=np.sort(qi); margins.append(float(ss[-1]-ss[-2]) if len(ss)>=2 else 0.)
    if not qs: qs=[qfull.copy()]; maps=[sel]; margins=[0.]
    Q=np.asarray(qs); qbar=Q.mean(0); non=[i for i,pm in enumerate(pms) if pm!=sel]; ci=max(non,key=lambda i:float(qbar[i])) if non else pms.index(sel); comp=pms[ci]
    js=np.asarray([s62.js_div(q,qfull) for q in Q]); sf=np.sort(qfull); fm=float(sf[-1]-sf[-2]) if len(sf)>=2 else 0.
    feat={'mean_js':float(np.mean(js)),'max_js':float(np.max(js)),'anchor_mass_drop':float(max(0.,qfull[pms.index(sel)]-qbar[pms.index(sel)])),'competitor_mean_mass':float(qbar[ci]),'competitor_vote_share':float(np.mean([m==comp for m in maps])),'switch_rate':float(np.mean([m!=sel for m in maps])),'margin_erosion':float(max(0.,fm-float(np.mean(margins)))),'mean_entropy':float(np.mean([s62.entropy(q) for q in Q]))}
    return pms,int(sel),int(comp),qbar,feat

def world_base(seedx):
    base=s54.world_base(seedx); reg,seed,w,c,data,targets,p0,meta=s47.state(seedx); fs,_=b.build_family_models(data,targets); nodes=[]
    for v in range(b.N):
        truth=s59.true_parent_mask(base['true_mask'],v); margin=s59.margin(fs,v,truth); pms,sel,comp,qbar,feat=s62_detail(data,targets,fs,v)
        nodes.append({'node':v,'pms':pms,'selected_parent_mask':sel,'competitor_parent_mask':comp,'q62':qbar.tolist(),'anchor_rank_error':bool(margin<0),'competitor_better_than_selected':bool(s62.hamming(comp,truth)<s62.hamming(sel,truth)),'features':[float(feat[k]) for k in FEATURES],'mean_js':feat['mean_js'],'competitor_mean_mass':feat['competitor_mean_mass']})
    base=dict(base); base['nodes']=nodes; base['mechanics_ok']=bool(base['mechanics_ok'] and all(np.all(np.isfinite(n['features'])) and np.all(np.isfinite(n['q62'])) for n in nodes)); return base

def generate(start,n): return [world_base(s) for s in s60.selected(start,n)]
def mechanics(rows,n): return len(rows)==2*n and all(sum(r['regime']==rg for r in rows)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in rows)
def node_matrix(rows,mean=None,std=None):
    Z=np.asarray([n['features'] for r in rows for n in r['nodes']]);
    if mean is None: mean=Z.mean(0)
    if std is None: std=Z.std(0); std=np.where(std<1e-8,1.,std)
    return np.column_stack([np.ones(len(Z)),(Z-mean)/std]),np.asarray(mean),np.asarray(std)
def train_model(rows):
    X,m,s=node_matrix(rows); y=np.asarray([n['anchor_rank_error'] for r in rows for n in r['nodes']],float); beta,prev=s61.fit_logistic(X,y,RIDGE); return {'mean':m.tolist(),'std':s.tolist(),'beta':beta.tolist(),'train_error_prevalence':prev}
def predictions(row,model):
    Z=np.asarray([n['features'] for n in row['nodes']]); X=np.column_stack([np.ones(len(Z)),(Z-np.asarray(model['mean']))/np.asarray(model['std'])]); pe=s61.sigmoid(X@np.asarray(model['beta'])); prev=model['train_error_prevalence']; a=np.clip((pe-prev)/max(1-prev,1e-6),0,1); r=np.asarray([np.clip(n['competitor_mean_mass']*(1-n['mean_js']),0,1) for n in row['nodes']]); return pe,MAX_RHO*a*r
def project(row,model):
    p=np.clip(np.asarray(row['ps30'],float),1e-300,None); p/=p.sum(); pe,rho=predictions(row,model); targets=[]
    for v,n in enumerate(row['nodes']):
        pms=n['pms']; m30=local_marginal(p,v,pms); q=np.asarray(n['q62']); t=(1-rho[v])*m30+rho[v]*q; t=np.clip(t,1e-8,None); t/=t.sum(); targets.append((pms,t))
    residual=0.
    for _ in range(CYCLES):
        residual=0.
        for v,(pms,t) in enumerate(targets):
            cur=local_marginal(p,v,pms); residual=max(residual,float(np.max(np.abs(cur-t)))); ratio=np.clip(t/np.clip(cur,1e-12,None),.25,4.); ix={pm:i for i,pm in enumerate(pms)}; mult=np.asarray([ratio[ix[dag_pm(d,v)]] for d in b.dags]); p*=mult; p=np.clip(p,1e-300,None); p/=p.sum()
        if residual<1e-8: break
    return p,pe,rho,float(residual)
def evaluate(rows,model,seed):
    ctl=[]; can=[]; cb=[]; xb=[]; regs=[]; probs=[]; labels=[]; rhos=[]; residuals=[]; outer=[]; hc=hx=0; err=use=0
    for r in rows:
        pp,pe,rho,res=project(r,model); mm=b.posterior_metrics(pp,r['true_mask']); ed=float(mm['edge_error']-r['baseline_edge_error']); bd=float(mm['brier']-r['baseline_brier']); op=bool(r['outer_promote']); c=float(r['s30_edge_delta_vs_baseline']) if op else 0.; x=ed if op else 0.; cbb=float(r['s30_brier_delta_vs_baseline']) if op else 0.; xbb=bd if op else 0.; ctl.append(c); can.append(x); cb.append(cbb); xb.append(xbb); regs.append(r['regime']); outer.append(op); probs.extend(pe); labels.extend([n['anchor_rank_error'] for n in r['nodes']]); rhos.extend(rho); residuals.append(res); hc+=int(op and r['s30_edge_delta_vs_baseline']>.5); hx+=int(op and ed>.5)
        for n in r['nodes']:
            if n['anchor_rank_error']: err+=1; use+=int(n['competitor_better_than_selected'])
    ctl=np.asarray(ctl); can=np.asarray(can); diff=can-ctl; probs=np.asarray(probs); labels=np.asarray(labels,bool); rhos=np.asarray(rhos); outer=np.asarray(outer,bool); prev=model['train_error_prevalence']; auc=s60.auc(labels,probs); bri=float(np.mean((probs-labels.astype(float))**2)); const=float(np.mean((prev-labels.astype(float))**2)); by={}
    for rg in REGIMES:
        i=np.asarray([z==rg for z in regs]); by[rg]={'n':int(i.sum()),'coverage':float(np.mean(outer[i])),'control_hybrid_mean_edge_delta':float(np.mean(ctl[i])),'candidate_hybrid_mean_edge_delta':float(np.mean(can[i])),'paired_mean_edge_difference':float(np.mean(diff[i]))}
    return {'coverage':float(np.mean(outer)),'mean_projection_fraction':float(np.mean(rhos)),'nonzero_projection_fraction':float(np.mean(rhos>1e-10)),'mean_final_ipf_residual':float(np.mean(residuals)),'control_hybrid_mean_edge_delta':float(np.mean(ctl)),'candidate_hybrid_mean_edge_delta':float(np.mean(can)),'paired_mean_edge_difference':float(np.mean(diff)),'bootstrap95_paired_edge_difference':s61.boot(diff,seed=seed),'control_hybrid_mean_brier_delta':float(np.mean(cb)),'candidate_hybrid_mean_brier_delta':float(np.mean(xb)),'control_promoted_large_harms':hc,'candidate_promoted_large_harms':hx,'error_localization_auc':auc,'error_localization_brier':bri,'constant_prevalence_brier':const,'competitor_useful_fraction_on_error_nodes':float(use/max(1,err)),'by_regime':by,'mechanics_ok':mechanics(rows,len(rows)//2)}
def qualifies(e,val=False,conf=False):
    lin=e['by_regime']['linear']; het=e['by_regime']['heteroskedastic']; ok=e['mechanics_ok'] and e['mean_final_ipf_residual']<=.02 and .02<=e['nonzero_projection_fraction']<=.70 and e['candidate_hybrid_mean_edge_delta']<=e['control_hybrid_mean_edge_delta']+.003 and het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.008 and lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.012 and e['candidate_promoted_large_harms']<=e['control_promoted_large_harms'] and e['candidate_hybrid_mean_brier_delta']<=e['control_hybrid_mean_brier_delta']+.005 and e['error_localization_auc'] is not None and e['error_localization_auc']>=.60 and e['error_localization_brier']<=e['constant_prevalence_brier'] and e['competitor_useful_fraction_on_error_nodes']>.50
    if val: ok=ok and e['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.004
    if conf: ok=ok and e['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.008
    return bool(ok)
def failclass(e): return 'FALSIFIED_EVIDENCE_TRANSFER' if e.get('error_localization_auc') is None or e['error_localization_auc']<.60 or e['competitor_useful_fraction_on_error_nodes']<=.50 else 'FALSIFIED_PROJECTION_GEOMETRY'
if __name__=='__main__':
    me=generate(96801,2); out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(96901,64); model=train_model(tr); ev=evaluate(tr,model,26464); out['training']={'model':model,'evaluation':ev}
        if not qualifies(ev): out['disposition']=failclass(ev)+'_AT_TRAINING'
        else:
            va=generate(97301,32); vv=evaluate(va,model,26465); out['validation']=vv
            if not qualifies(vv,True): out['disposition']=failclass(vv)+'_ON_VALIDATION'
            else:
                co=generate(97601,64); cv=evaluate(co,model,26466); out['confirmation']=cv; out['disposition']='SUPPORTED' if qualifies(cv,True,True) else failclass(cv)+'_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
