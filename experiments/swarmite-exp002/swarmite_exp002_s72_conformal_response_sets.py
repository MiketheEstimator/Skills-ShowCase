import json, math, numpy as np
from statistics import NormalDist
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s69_predictive_calibration as s69

REGIMES=s69.REGIMES; DRAWS=s69.DRAWS
Z80=NormalDist().inv_cdf(.90); Z95=NormalDist().inv_cdf(.975)


def seeds(start,n):
    out=[]
    for rg in REGIMES:
        out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out


def cells(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets)
    p=b.posterior_from_fs(fs)
    out=[]
    for target in range(b.N):
        for spi,sp in enumerate((-2.,2.)):
            rr=b.rng_for('s72','predictive',seed,target,spi)
            sims=np.asarray([b.sim_row_from_posterior(p,models,target,sp,rr) for _ in range(DRAWS)],float)
            obs=np.asarray(s69.actual(reg,w,seed,target,sp,meta),float)
            for j in range(b.N):
                if j==target: continue
                x=sims[:,j]
                mu=float(np.mean(x)); sd=float(np.std(x,ddof=1))
                if (not np.isfinite(sd)) or sd<=1e-10: return None
                out.append({'regime':reg,'world':external_seed,'sp':float(sp),'logsd':math.log(sd),'mu':mu,'sd':sd,'resid':float(obs[j]-mu)})
    return out


def gather(ss):
    out=[]
    for x in ss:
        q=cells(x)
        if q is None:return None
        out.extend(q)
    return out


def qtile(x,q):
    return float(np.quantile(np.asarray(x,float),q,method='higher'))


def fit(cal):
    model={'edges':{},'groups':{}}
    for sp in (-2.0,2.0):
        sub=[r for r in cal if r['sp']==sp]
        vals=np.asarray([r['logsd'] for r in sub],float)
        edges=np.quantile(vals,[.2,.4,.6,.8]).tolist()
        model['edges'][str(sp)]=edges
        pool=[r['resid'] for r in sub]
        fallback={'.80':[qtile(pool,.10),qtile(pool,.90)],'.95':[qtile(pool,.025),qtile(pool,.975)]}
        for k in range(5):
            lo=-np.inf if k==0 else edges[k-1]; hi=np.inf if k==4 else edges[k]
            rs=[r['resid'] for r in sub if r['logsd']>lo and r['logsd']<=hi]
            if len(rs)<100: qq=fallback
            else: qq={'.80':[qtile(rs,.10),qtile(rs,.90)],'.95':[qtile(rs,.025),qtile(rs,.975)]}
            model['groups'][f'{sp}:{k}']=qq
    return model


def bucket(model,r):
    e=model['edges'][str(r['sp'])]
    return int(np.searchsorted(np.asarray(e,float),r['logsd'],side='left'))


def metrics(rows,model):
    out={}
    for rg in REGIMES:
        sub=[r for r in rows if r['regime']==rg]
        raw80=[];raw95=[];con80=[];con95=[];rw80=[];rw95=[];cw80=[];cw95=[]
        for r in sub:
            a=abs(r['resid']); sd=r['sd']; k=bucket(model,r); qq=model['groups'][f"{r['sp']}:{k}"]
            raw80.append(a<=Z80*sd); raw95.append(a<=Z95*sd)
            rw80.append(2*Z80*sd); rw95.append(2*Z95*sd)
            lo80,hi80=qq['.80']; lo95,hi95=qq['.95']
            con80.append(lo80<=r['resid']<=hi80); con95.append(lo95<=r['resid']<=hi95)
            cw80.append(hi80-lo80); cw95.append(hi95-lo95)
        out[rg]={
            'raw':{'coverage80':float(np.mean(raw80)),'coverage95':float(np.mean(raw95)),'width80':float(np.mean(rw80)),'width95':float(np.mean(rw95))},
            'conformal':{'coverage80':float(np.mean(con80)),'coverage95':float(np.mean(con95)),'width80':float(np.mean(cw80)),'width95':float(np.mean(cw95))}
        }
    return out


def ce(v): return abs(v['coverage80']-.8)+abs(v['coverage95']-.95)


def disposition(m):
    raw=np.mean([ce(m[r]['raw']) for r in REGIMES]); con=np.mean([ce(m[r]['conformal']) for r in REGIMES]); imp=(raw-con)/max(raw,1e-12)
    no_reg=all(ce(m[r]['conformal'])<=ce(m[r]['raw'])+.02 for r in REGIMES)
    bounds=all(.74<=m[r]['conformal']['coverage80']<=.86 and .91<=m[r]['conformal']['coverage95']<=.98 for r in REGIMES)
    wr=np.mean([m[r]['conformal']['width95'] for r in REGIMES])/max(np.mean([m[r]['raw']['width95'] for r in REGIMES]),1e-12)
    ok=imp>=.20 and no_reg and bounds and wr<=1.75
    return ('CONFORMAL_RESPONSE_SETS_SUPPORTED' if ok else 'CONFORMAL_RESPONSE_SETS_FALSIFIED'),raw,con,imp,wr


def main():
    mech=gather(seeds(116001,2)); out={'mechanics':{'passed':bool(mech)}}
    if not mech: out['disposition']='BLOCKED_EXECUTION_MECHANICS'; return out
    cal=gather(seeds(116201,64))
    if cal is None: out['disposition']='BLOCKED_EXECUTION_NONFINITE'; return out
    model=fit(cal)
    test=gather(seeds(117201,64))
    if test is None: out['disposition']='BLOCKED_EXECUTION_NONFINITE'; return out
    hm=metrics(test,model); d,raw,con,imp,wr=disposition(hm)
    out['heldout']=hm; out['coverage_error']={'raw_mean':float(raw),'conformal_mean':float(con),'relative_improvement':float(imp)}; out['width95_ratio']=float(wr); out['disposition']=d
    return out

if __name__=='__main__': print(json.dumps(main(),separators=(',',':')))
