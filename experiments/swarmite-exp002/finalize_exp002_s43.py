import json
from pathlib import Path
import swarmite_exp002_s43_classaware as s43

ep=Path('.')
qp=Path('../swarmite-queue/QUEUE.json')
q=json.loads(qp.read_text())
item=next(x for x in q['queue'] if x['id']=='EXP-002S43')
item.update({'status':'RUNNING','protocol':'experiments/swarmite-exp002/EXP-002S43_CLASS_AWARE_DECISION_PROTOCOL.md','runner':'experiments/swarmite-exp002/swarmite_exp002_s43_classaware.py','runner_commit':'eeaab00cb078f1656649a26041e3cbcbb7a2395e','checkpoint':{'state':'protocol_frozen','next_stage':'training_then_validation','training_seeds':[73101,73148],'validation_seeds':[73161,73196],'confirmation_seeds':[73201,73248]}})
q['version']='8.8'; qp.write_text(json.dumps(q,indent=2))
out=s43.run(); (ep/'EXP-002S43_RESULT.json').write_text(json.dumps(out,indent=2)); disp=out['disposition']; item['result_artifact']='experiments/swarmite-exp002/EXP-002S43_RESULT.json'; item['result_summary']=out; item['checkpoint']={'state':'complete','disposition':disp}
if disp=='CLASS_AWARE_DECISION_SUPPORTED':
    item['status']='COMPLETE_SUPPORTED'; succ={'id':'EXP-002S44','title':'Joint class-aware decision transfer under topology plus heteroskedastic shift','priority':50.0,'status':'PENDING','depends_on':['EXP-002S43'],'rationale':'S43 supported explicit topology-class utility propagation; test the frozen class-aware decision under combined topology and heteroskedastic observation shift before reference promotion.'}
elif disp=='BLOCKED_MECHANICS':
    item['status']='BLOCKED_EXECUTION_MECHANICS'; succ={'id':'EXP-002S44','title':'Class-aware decision mechanics recovery','priority':50.0,'status':'PENDING','depends_on':['EXP-002S43'],'rationale':'Repair mechanics without changing the class-aware utility hypothesis.'}
else:
    item['status']='COMPLETE_FALSIFIED_'+disp; succ={'id':'EXP-002S44','title':'Joint mechanism-noise-topology world-class uncertainty','priority':50.0,'status':'PENDING','depends_on':['EXP-002S43'],'rationale':'Topology-class uncertainty alone did not yield a safe utility decision; expand the latent world class to mechanism, noise, and topology rather than returning to scalar gates.'}
if not any(x.get('id')=='EXP-002S44' for x in q['queue']): q['queue'].append(succ)
sm=out.get('confirmation') or out.get('validation') or {}; ca=sm.get('class_aware',{}); ctrl=sm.get('s39_control',{}); finding=f"S43 {disp}: class-aware coverage {ca.get('coverage',float('nan')):.3f}, hybrid edge delta {ca.get('hybrid_mean_edge_delta',float('nan')):.3f}, S39 control {ctrl.get('hybrid_mean_edge_delta',float('nan')):.3f}, harm rate {ca.get('promoted_large_harm_rate',float('nan')):.3f}."
if finding not in q['established_findings']: q['established_findings'].append(finding)
q['version']='8.9'; qp.write_text(json.dumps(q,indent=2))
lines=['# EXP-002S43 Evaluation','',f'**Disposition:** {disp}']
if 'training' in out: lines += ['',f"Training class parameters: **{out['training']['params']}**"]
for name in ('validation','confirmation'):
 if name in out:
  s=out[name]; a=s['class_aware']; c=s['s39_control']; lines += ['',f'## {name.title()}',f"Class-aware coverage: **{a['coverage']:.3f}**",f"Class-aware edge delta: **{a['hybrid_mean_edge_delta']:.3f}**",f"Class-aware harm rate: **{a['promoted_large_harm_rate']:.3f}**",f"Improvement retained: **{a['improvement_retained']:.3f}**",f"S39 control edge delta: **{c['hybrid_mean_edge_delta']:.3f}**"]
lines += ['', '## Next',succ['rationale']]
(ep/'EXP-002S43_EVALUATION.md').write_text('\n'.join(lines)); item['evaluation_artifact']='experiments/swarmite-exp002/EXP-002S43_EVALUATION.md'; qp.write_text(json.dumps(q,indent=2))
