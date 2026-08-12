import json, math, numpy as np
from pathlib import Path
import swarmite_benchmark_v2 as b
import swarmite_exp002_s46_continuous_risk as s46
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s48_hetero_repair as s48
import swarmite_exp002_s49_hetero_likelihood as s49
import swarmite_exp002_s52_latent_residual_state as s52

REGIMES=('linear','heteroskedastic')
CAPS=(0.10,0.20,0.30,0.40)
GAMMAS=(0.5,1.0,2.0)
GAIN_SCALES=(0.05,0.10,0.20)


def sigmoid(x):
    return 1.0/(1.0+math.exp(-max(-40.0,min(40.0,float(x)))))


def load_s52_model():
    p=Path(__file__).with_name('EXP-002S52_TRAINING_RESULT.json')
    x=json.loads(p.read_text())
    if not x.get('mechanics_ok') or not x.get('model'):
        raise RuntimeError('S52 frozen training model unavailable')
    return x['model']


def setting_key(cap,gamma,gain_scale):
    return f'c{cap:.2f}_g{gamma:.1f}_s{gain_scale:.2f}'


def weight_from_prediction(p,g,cap,gamma,gain_scale):
    return float(cap*(max(0.0,min(1.0,float(p)))**gamma)*sigmoid(float(g)/gain_scale))


def world_row(external_seed, model):
    # S52 provides the frozen observable latent representation and predictions.
    base=s52.world_row(external_seed)
    pred=s52.predict([base],model)[0]
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    if reg not in REGIMES: raise ValueError(reg)
    ps30,ok30=s49.s30_posterior(data,targets,p0)
    phet,okh=s49.hetero_posterior(data,targets)
    bm=b.posterior_metrics(p0,w.dag_mask)
    cand={}
    for cap in CAPS:
        for gamma in GAMMAS:
            for scale in GAIN_SCALES:
                wt=weight_from_prediction(pred['pred_specialist_win_prob'],pred['pred_specialist_gain'],cap,gamma,scale)
                pp=(1-wt)*ps30+wt*phet; pp/=pp.sum()
                mm=b.posterior_metrics(pp,w.dag_mask)
                cand[setting_key(cap,gamma,scale)]={
                    'weight':wt,
                    'edge_delta':float(mm['edge_error']-bm['edge_error']),
                    'brier_delta':float(mm['brier']-bm['brier']),
                    'large_harm':int(mm['edge_error']-bm['edge_error']>.50)
                }
    out=dict(base)
    out.update({
        'pred_specialist_win_prob':float(pred['pred_specialist_win_prob']),
        'pred_specialist_gain':float(pred['pred_specialist_gain']),
        'candidate':cand,
        'posterior_mechanics_ok':bool(base['posterior_mechanics_ok'] and ok30 and okh and np.isfinite(ps30).all() and np.isfinite(phet).all()),
        's30_sum':float(ps30.sum()),'phet_sum':float(phet.sum())
    })
    return out


def generate(start,n_each,model):
    seeds=[]
    for rg in REGIMES:
        seeds += s48.selected_external_seeds(start,rg,n_each)
    return [world_row(s,model) for s in seeds]


def mechanics(rows,n_each):
    return all(sum(r['regime']==rg for r in rows)==n_each for rg in REGIMES) and all(
        r['spend']<=15 and r['trace_identical'] and r['finite'] and r['posterior_mechanics_ok'] and
        0<=r['pred_specialist_win_prob']<=1 and np.isfinite(r['pred_specialist_gain']) and
        abs(r['s30_sum']-1)<1e-8 and abs(r['phet_sum']-1)<1e-8
        for r in rows)


def boot(x,reps=10000,seed=25353):
    x=np.asarray(x,float); rr=np.random.default_rng(seed)
    mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]


def evaluate(rows,setting,seed):
    cap,gamma,scale=setting
    key=setting_key(cap,gamma,scale)
    outer=np.array([r['outer_promote'] for r in rows],bool)
    s30e=np.array([r['s30_edge_delta_vs_baseline'] for r in rows],float)
    s30b=np.array([r['s30_brier_delta_vs_baseline'] for r in rows],float)
    ce=np.array([r['candidate'][key]['edge_delta'] for r in rows],float)
    cb=np.array([r['candidate'][key]['brier_delta'] for r in rows],float)
    ww=np.array([r['candidate'][key]['weight'] for r in rows],float)
    control=np.where(outer,s30e,0.0); candidate=np.where(outer,ce,0.0); diff=candidate-control
    control_b=np.where(outer,s30b,0.0); candidate_b=np.where(outer,cb,0.0)
    harms_control=int(np.sum(outer & (s30e>.50))); harms_candidate=int(np.sum(outer & (ce>.50)))
    by={}
    for rg in REGIMES:
        idx=np.array([r['regime']==rg for r in rows],bool)
        by[rg]={
            'n':int(idx.sum()),'coverage':float(np.mean(outer[idx])),
            'control_hybrid_mean_edge_delta':float(np.mean(control[idx])),
            'candidate_hybrid_mean_edge_delta':float(np.mean(candidate[idx])),
            'paired_mean_edge_difference':float(np.mean(diff[idx])),
            'mean_specialist_weight':float(np.mean(ww[idx]))
        }
    return {
        'setting':{'cap':cap,'gamma':gamma,'gain_scale':scale},
        'coverage':float(np.mean(outer)),
        'mean_specialist_weight':float(np.mean(ww)),
        'control_hybrid_mean_edge_delta':float(np.mean(control)),
        'candidate_hybrid_mean_edge_delta':float(np.mean(candidate)),
        'paired_mean_edge_difference':float(np.mean(diff)),
        'bootstrap95_paired_edge_difference':boot(diff,seed=seed),
        'control_hybrid_mean_brier_delta':float(np.mean(control_b)),
        'candidate_hybrid_mean_brier_delta':float(np.mean(candidate_b)),
        'control_promoted_large_harms':harms_control,
        'candidate_promoted_large_harms':harms_candidate,
        'by_regime':by,
        'mechanics_ok':mechanics(rows,int(len(rows)/2))
    }


def qualifies(ev,validation=False,confirmation=False):
    lin=ev['by_regime']['linear']; het=ev['by_regime']['heteroskedastic']
    ok=(ev['mechanics_ok'] and .01<=ev['mean_specialist_weight']<=.20 and
        ev['candidate_hybrid_mean_edge_delta']<=ev['control_hybrid_mean_edge_delta']+.01 and
        het['candidate_hybrid_mean_edge_delta']<=het['control_hybrid_mean_edge_delta']-.02 and
        lin['candidate_hybrid_mean_edge_delta']<=lin['control_hybrid_mean_edge_delta']+.02 and
        ev['candidate_promoted_large_harms']<=ev['control_promoted_large_harms'] and
        ev['candidate_hybrid_mean_brier_delta']<=.005)
    if validation or confirmation:
        ok=ok and ev['paired_mean_edge_difference']<=0 and het['paired_mean_edge_difference']<=-.01
    if confirmation:
        ok=ok and ev['bootstrap95_paired_edge_difference'][1]<0 and het['paired_mean_edge_difference']<-.02
    return bool(ok)


def select_setting(rows):
    grid=[]
    for cap in CAPS:
        for gamma in GAMMAS:
            for scale in GAIN_SCALES:
                ev=evaluate(rows,(cap,gamma,scale),25354)
                grid.append({'setting':ev['setting'],'qualifies':qualifies(ev),'summary':ev})
    good=[x for x in grid if x['qualifies']]
    if not good: return None,grid
    good.sort(key=lambda x:(x['summary']['by_regime']['heteroskedastic']['candidate_hybrid_mean_edge_delta'],x['setting']['cap'],-x['setting']['gamma'],-x['setting']['gain_scale']))
    best=good[0]
    besthet=best['summary']['by_regime']['heteroskedastic']['candidate_hybrid_mean_edge_delta']
    near=[x for x in good if x['summary']['by_regime']['heteroskedastic']['candidate_hybrid_mean_edge_delta']<=besthet+.01]
    near.sort(key=lambda x:(x['setting']['cap'],-x['setting']['gamma'],-x['setting']['gain_scale']))
    s=near[0]['setting']
    return (float(s['cap']),float(s['gamma']),float(s['gain_scale'])),grid


if __name__=='__main__':
    model=load_s52_model(); me=generate(80501,2,model)
    out={'mechanics':{'passed':mechanics(me,2)}}
    if not out['mechanics']['passed']:
        out['disposition']='BLOCKED_MECHANICS'
    else:
        tr=generate(80601,64,model); setting,grid=select_setting(tr)
        out['training']={'selected_setting':setting,'grid':grid,'mechanics_ok':mechanics(tr,64)}
        if setting is None or not mechanics(tr,64):
            out['disposition']='FALSIFIED_AT_TRAINING' if setting is None else 'BLOCKED_MECHANICS'
        else:
            va=generate(81001,32,model); ev=evaluate(va,setting,25355); out['validation']=ev
            if not mechanics(va,32) or not qualifies(ev,validation=True):
                out['disposition']='FALSIFIED_ON_VALIDATION'
            else:
                co=generate(81501,64,model); ce=evaluate(co,setting,25356); out['confirmation']=ce
                out['disposition']='SUPPORTED' if mechanics(co,64) and qualifies(ce,validation=True,confirmation=True) else 'FALSIFIED_ON_CONFIRMATION'
    print(json.dumps(out,separators=(',',':')))
