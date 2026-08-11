import json
from pathlib import Path
import swarmite_exp002_s41_density as s41

ep=Path('.')
qp=Path('../swarmite-queue/QUEUE.json')
q=json.loads(qp.read_text())
item=next(x for x in q['queue'] if x['id']=='EXP-002S41')
item.update({'status':'RUNNING','protocol':'experiments/swarmite-exp002/EXP-002S41_GRAPH_DENSITY_TRANSFER_PROTOCOL.md','runner':'experiments/swarmite-exp002/swarmite_exp002_s41_density.py','runner_commit':'c160b389bea84467e316a5fe1cbdd26d5722e068','checkpoint':{'state':'protocol_frozen','next_stage':'mechanics_then_screen','mechanics_seeds':[72701,72704],'screen_seeds':[72711,72734],'confirmation_seeds':[72801,72848],'frozen_score':'mean_credal_width','frozen_threshold':0.2692013432171404}})
q['version']='8.4'; qp.write_text(json.dumps(q,indent=2))
out=s41.run(); (ep/'EXP-002S41_RESULT.json').write_text(json.dumps(out,indent=2)); disp=out['disposition']; item['result_artifact']='experiments/swarmite-exp002/EXP-002S41_RESULT.json'; item['result_summary']=out; item['checkpoint']={'state':'complete','disposition':disp}
if disp=='GRAPH_DENSITY_TRANSFER_SUPPORTED':
    item['status']='COMPLETE_TRANSFER_SUPPORTED'; succ={'id':'EXP-002S42','title':'Credal architecture promotion stress under combined topology and observation shift','priority':50.5,'status':'PENDING','depends_on':['EXP-002S41'],'rationale':'S39-S41 support the frozen credal layer across benchmark, heteroskedastic observation shift, and graph-density shift; run one preregistered compound stress before promoting it as reference architecture.'}
elif disp=='BLOCKED_MECHANICS':
    item['status']='BLOCKED_EXECUTION_MECHANICS'; succ={'id':'EXP-002S42','title':'Graph-density transfer mechanics recovery','priority':50.5,'status':'PENDING','depends_on':['EXP-002S41'],'rationale':'Repair the execution mechanism without changing the frozen S39 gate or scientific hypothesis.'}
else:
    item['status']='COMPLETE_FALSIFIED_'+disp; succ={'id':'EXP-002S42','title':'Topology-aware world-class uncertainty over science posteriors','priority':50.5,'status':'PENDING','depends_on':['EXP-002S41'],'rationale':'The frozen scalar credal-width gate failed topology shift; replace scalar disagreement with explicit topology/world-class uncertainty while retaining S30 as anchor.'}
if not any(x.get('id')=='EXP-002S42' for x in q['queue']): q['queue'].append(succ)
sm=out.get('confirmation') or out.get('screen') or {}; finding=f"S41 {disp}: frozen S39 gate under sparse/dense graph shift; coverage {sm.get('coverage',float('nan')):.3f}, hybrid edge delta {sm.get('hybrid_mean_edge_delta',float('nan')):.3f}, promoted large-harm rate {sm.get('promoted_large_harm_rate',float('nan')):.3f}."
if finding not in q['established_findings']: q['established_findings'].append(finding)
q['version']='8.5'; qp.write_text(json.dumps(q,indent=2))
lines=['# EXP-002S41 Evaluation','',f'**Disposition:** {disp}','', 'Frozen S39 gate: `mean_credal_width <= 0.2692013432171404`']
if 'screen' in out:
 s=out['screen']; lines += ['', '## Screen',f"Coverage: **{s['coverage']:.3f}**",f"Hybrid edge delta: **{s['hybrid_mean_edge_delta']:.3f}**",f"Promoted large-harm rate: **{s['promoted_large_harm_rate']:.3f}**",f"By density: **{s['by_density']}**"]
if 'confirmation' in out:
 c=out['confirmation']; lines += ['', '## Confirmation',f"Coverage: **{c['coverage']:.3f}**",f"Hybrid edge delta: **{c['hybrid_mean_edge_delta']:.3f}**",f"95% bootstrap: **{c['bootstrap95_hybrid_edge_delta']}**",f"Promoted large-harm rate: **{c['promoted_large_harm_rate']:.3f}**",f"Brier delta: **{c['hybrid_mean_brier_delta']:.4f}**",f"By density: **{c['by_density']}**"]
lines += ['', '## Next',succ['rationale']]
(ep/'EXP-002S41_EVALUATION.md').write_text('\n'.join(lines)); item['evaluation_artifact']='experiments/swarmite-exp002/EXP-002S41_EVALUATION.md'; qp.write_text(json.dumps(q,indent=2))
