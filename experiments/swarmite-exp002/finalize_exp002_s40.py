import json
from pathlib import Path
import swarmite_exp002_s40_hetero as s40

ep=Path('.')
qp=Path('../swarmite-queue/QUEUE.json')
q=json.loads(qp.read_text())
item=next(x for x in q['queue'] if x['id']=='EXP-002S40')
item.update({
    'status':'RUNNING',
    'protocol':'experiments/swarmite-exp002/EXP-002S40_HETEROSKEDASTIC_TRANSFER_PROTOCOL.md',
    'runner':'experiments/swarmite-exp002/swarmite_exp002_s40_hetero.py',
    'runner_commit':'41af5c00afc5c5b097ae07ea9bf7de339d266583',
    'checkpoint':{'state':'protocol_frozen','next_stage':'mechanics_then_screen','mechanics_seeds':[72501,72504],'screen_seeds':[72511,72534],'confirmation_seeds':[72601,72648],'frozen_score':'mean_credal_width','frozen_threshold':0.2692013432171404}
})
q['version']='8.2'; qp.write_text(json.dumps(q,indent=2))
out=s40.run(); (ep/'EXP-002S40_RESULT.json').write_text(json.dumps(out,indent=2)); disp=out['disposition']
item['result_artifact']='experiments/swarmite-exp002/EXP-002S40_RESULT.json'; item['result_summary']=out; item['checkpoint']={'state':'complete','disposition':disp}
if disp=='HETEROSKEDASTIC_TRANSFER_SUPPORTED':
    item['status']='COMPLETE_TRANSFER_SUPPORTED'
    succ={'id':'EXP-002S41','title':'Frozen credal gate under graph-density shift','priority':50.75,'status':'PENDING','depends_on':['EXP-002S40'],'rationale':'S40 supported heteroskedastic transfer without retuning; test whether the frozen S39 uncertainty layer survives sparse/dense topology shift before architectural promotion.'}
elif disp=='BLOCKED_MECHANICS':
    item['status']='BLOCKED_EXECUTION_MECHANICS'
    succ={'id':'EXP-002S41','title':'Heteroskedastic transfer mechanics recovery','priority':50.75,'status':'PENDING','depends_on':['EXP-002S40'],'rationale':'S40 mechanics failed before scientific exposure; repair the execution mechanism without changing the frozen S39 gate or scientific hypothesis.'}
else:
    item['status']='COMPLETE_FALSIFIED_'+disp
    succ={'id':'EXP-002S41','title':'Explicit world-class uncertainty over science posteriors','priority':50.75,'status':'PENDING','depends_on':['EXP-002S40'],'rationale':'The scalar credal-width gate failed transfer under heteroskedastic nonlinear shift; replace threshold geometry with explicit latent world-class uncertainty while retaining S30 as the control anchor.'}
if not any(x.get('id')=='EXP-002S41' for x in q['queue']): q['queue'].append(succ)
sm=out.get('confirmation') or out.get('screen') or {}
finding=f"S40 {disp}: frozen S39 credal gate under heteroskedastic nonlinear shift; coverage {sm.get('coverage',float('nan')):.3f}, hybrid edge delta {sm.get('hybrid_mean_edge_delta',float('nan')):.3f}, promoted large-harm rate {sm.get('promoted_large_harm_rate',float('nan')):.3f}."
if finding not in q['established_findings']: q['established_findings'].append(finding)
q['version']='8.3'; qp.write_text(json.dumps(q,indent=2))
lines=['# EXP-002S40 Evaluation','',f'**Disposition:** {disp}','', 'Frozen S39 gate: `mean_credal_width <= 0.2692013432171404`']
if 'screen' in out:
 s=out['screen']; lines += ['', '## Screen',f"Coverage: **{s['coverage']:.3f}**",f"Hybrid edge delta: **{s['hybrid_mean_edge_delta']:.3f}**",f"Promoted large-harm rate: **{s['promoted_large_harm_rate']:.3f}**",f"Brier delta: **{s['hybrid_mean_brier_delta']:.4f}**"]
if 'confirmation' in out:
 c=out['confirmation']; lines += ['', '## Confirmation',f"Coverage: **{c['coverage']:.3f}**",f"Hybrid edge delta: **{c['hybrid_mean_edge_delta']:.3f}**",f"95% bootstrap: **{c['bootstrap95_hybrid_edge_delta']}**",f"Promoted large-harm rate: **{c['promoted_large_harm_rate']:.3f}**",f"Brier delta: **{c['hybrid_mean_brier_delta']:.4f}**"]
lines += ['', '## Next',succ['rationale']]
(ep/'EXP-002S40_EVALUATION.md').write_text('\n'.join(lines)); item['evaluation_artifact']='experiments/swarmite-exp002/EXP-002S40_EVALUATION.md'; qp.write_text(json.dumps(q,indent=2))
