import json
from pathlib import Path
import swarmite_exp002_s42_worldclass as s42

ep=Path('.')
qp=Path('../swarmite-queue/QUEUE.json')
q=json.loads(qp.read_text())
item=next(x for x in q['queue'] if x['id']=='EXP-002S42')
item.update({'status':'RUNNING','protocol':'experiments/swarmite-exp002/EXP-002S42_TOPOLOGY_WORLDCLASS_PROTOCOL.md','runner':'experiments/swarmite-exp002/swarmite_exp002_s42_worldclass.py','runner_commit':'6960722306b4928b8fea93f7c8b1fd31098d4258','checkpoint':{'state':'protocol_frozen','next_stage':'training_then_validation','training_seeds':[72901,72948],'validation_seeds':[72961,73008]}})
q['version']='8.6'; qp.write_text(json.dumps(q,indent=2))
out=s42.run(); (ep/'EXP-002S42_RESULT.json').write_text(json.dumps(out,indent=2)); disp=out['disposition']; item['result_artifact']='experiments/swarmite-exp002/EXP-002S42_RESULT.json'; item['result_summary']=out; item['checkpoint']={'state':'complete','disposition':disp}
if disp=='TOPOLOGY_WORLDCLASS_SUPPORTED':
    item['status']='COMPLETE_DIAGNOSTIC_SUPPORTED'; succ={'id':'EXP-002S43','title':'Class-aware uncertainty decision over S30 anchor','priority':50.25,'status':'PENDING','depends_on':['EXP-002S42'],'rationale':'S42 established an explicit observable topology-class posterior that outperforms scalar credal width for density identification; test a preregistered class-aware uncertainty decision while keeping S30 as point anchor.'}
elif disp=='BLOCKED_MECHANICS':
    item['status']='BLOCKED_EXECUTION_MECHANICS'; succ={'id':'EXP-002S43','title':'Topology world-class mechanics recovery','priority':50.25,'status':'PENDING','depends_on':['EXP-002S42'],'rationale':'Repair mechanics without changing the frozen class-evidence hypothesis.'}
else:
    item['status']='COMPLETE_FALSIFIED_ON_VALIDATION'; succ={'id':'EXP-002S43','title':'Joint mechanism-noise-topology world-class uncertainty','priority':50.25,'status':'PENDING','depends_on':['EXP-002S42'],'rationale':'Edge-count evidence alone failed to identify topology class robustly; expand the latent world-class representation to mechanism, noise, and topology rather than retuning scalar disagreement.'}
if not any(x.get('id')=='EXP-002S43' for x in q['queue']): q['queue'].append(succ)
sm=out.get('validation') or out.get('training') or {}; finding=f"S42 {disp}: topology class AUC {sm.get('auc_worldclass',float('nan')):.3f}, credal control AUC {sm.get('auc_credal_control',float('nan')):.3f}, Brier {sm.get('brier',float('nan')):.3f}, accuracy {sm.get('accuracy',float('nan')):.3f}."
if finding not in q['established_findings']: q['established_findings'].append(finding)
q['version']='8.7'; qp.write_text(json.dumps(q,indent=2))
lines=['# EXP-002S42 Evaluation','',f'**Disposition:** {disp}']
for name in ('training','validation'):
 if name in out:
  s=out[name]; lines += ['',f'## {name.title()}',f"World-class AUC: **{s['auc_worldclass']:.3f}**",f"Credal-width control AUC: **{s['auc_credal_control']:.3f}**",f"AUC gain: **{s['auc_gain']:.3f}**",f"Brier: **{s['brier']:.3f}**",f"Accuracy: **{s['accuracy']:.3f}**"]
lines += ['', '## Next',succ['rationale']]
(ep/'EXP-002S42_EVALUATION.md').write_text('\n'.join(lines)); item['evaluation_artifact']='experiments/swarmite-exp002/EXP-002S42_EVALUATION.md'; qp.write_text(json.dumps(q,indent=2))
