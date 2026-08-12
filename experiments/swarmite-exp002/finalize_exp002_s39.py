import json
from pathlib import Path
import swarmite_exp002_s39_credal as s39

ep=Path('.')
qp=Path('../swarmite-queue/QUEUE.json')
q=json.loads(qp.read_text())
item=next(x for x in q['queue'] if x['id']=='EXP-002S39')
item.update({
    'status':'RUNNING',
    'protocol':'experiments/swarmite-exp002/EXP-002S39_CREDAL_DISAGREEMENT_PROTOCOL.md',
    'runner':'experiments/swarmite-exp002/swarmite_exp002_s39_credal.py',
    'runner_commit':'38e838524c9a44d486247a09eeee7ca1d4836a37',
    'checkpoint':{'state':'executing_frozen_design','training_seeds':[72301,72348],'validation_seeds':[72361,72396],'confirmation_seeds':[72401,72448]}
})
q['version']='8.0'
qp.write_text(json.dumps(q,indent=2))

out=s39.run()
(ep/'EXP-002S39_RESULT.json').write_text(json.dumps(out,indent=2))
disp=out['disposition']
item['result_artifact']='experiments/swarmite-exp002/EXP-002S39_RESULT.json'
item['result_summary']={
    'disposition':disp,
    'selected':out['training']['fit'].get('selected'),
    'validation':out.get('validation'),
    'confirmation':out.get('confirmation')
}
item['checkpoint']={'state':'complete','disposition':disp}
if disp=='CREDAL_ABSTENTION_SUPPORTED':
    item['status']='COMPLETE_SUPPORTED'
    succ={'id':'EXP-002S40','title':'Credal abstention transfer under unseen heteroskedastic mechanism shift','priority':51.0,'status':'PENDING','depends_on':['EXP-002S39'],'rationale':'S39 supported specialist disagreement as uncertainty while preserving S30 point inference; freeze the gate and test transfer under a new heteroskedastic nonlinear world family before architectural promotion.'}
else:
    item['status']='COMPLETE_FALSIFIED_'+disp
    succ={'id':'EXP-002S40','title':'Explicit world-class uncertainty over science posteriors','priority':51.0,'status':'PENDING','depends_on':['EXP-002S39'],'rationale':'S39 falsified thresholded specialist-disagreement abstention; replace scalar disagreement geometry with an explicit latent world-class uncertainty representation while retaining S30 as the control anchor.'}
if not any(x.get('id')=='EXP-002S40' for x in q['queue']): q['queue'].append(succ)
sel=out['training']['fit'].get('selected')
if sel:
    finding=f"S39 {disp}: mean credal-width threshold {sel['threshold']:.6f}; confirmation coverage {out.get('confirmation',{}).get('metrics',{}).get('coverage',float('nan')):.3f}, hybrid edge delta {out.get('confirmation',{}).get('metrics',{}).get('hybrid_mean_edge_delta',float('nan')):.3f}, promoted large-harm rate {out.get('confirmation',{}).get('metrics',{}).get('promoted_large_harm_rate',float('nan')):.3f}."
else:
    finding=f"S39 {disp}: no eligible credal disagreement gate."
if finding not in q['established_findings']: q['established_findings'].append(finding)
q['version']='8.1'
lines=['# EXP-002S39 Evaluation','',f'**Disposition:** {disp}','']
if sel:
    lines += [f"Selected score: **{sel['score']}**",f"Frozen threshold: **{sel['threshold']:.6f}**",f"Training coverage: **{sel['metrics']['coverage']:.3f}**",f"Training promoted large-harm rate: **{sel['metrics']['promoted_large_harm_rate']:.3f}**"]
if 'validation' in out:
    v=out['validation']['metrics']; lines += ['', '## Validation',f"Coverage: **{v['coverage']:.3f}**",f"Hybrid edge delta vs baseline: **{v['hybrid_mean_edge_delta']:.3f}**",f"Promoted large-harm rate: **{v['promoted_large_harm_rate']:.3f}**",f"Brier delta: **{v['hybrid_mean_brier_delta']:.4f}**"]
if 'confirmation' in out:
    c=out['confirmation']['metrics']; lines += ['', '## Confirmation',f"Coverage: **{c['coverage']:.3f}**",f"Hybrid edge delta vs baseline: **{c['hybrid_mean_edge_delta']:.3f}**",f"95% bootstrap: **{c['bootstrap95_hybrid_edge_delta']}**",f"Promoted large-harm rate: **{c['promoted_large_harm_rate']:.3f}**",f"Brier delta: **{c['hybrid_mean_brier_delta']:.4f}**"]
lines += ['', '## Next',succ['rationale']]
(ep/'EXP-002S39_EVALUATION.md').write_text('\n'.join(lines))
item['evaluation_artifact']='experiments/swarmite-exp002/EXP-002S39_EVALUATION.md'
qp.write_text(json.dumps(q,indent=2))
