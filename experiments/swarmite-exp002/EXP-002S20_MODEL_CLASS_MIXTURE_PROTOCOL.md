# EXP-002S20 — Explicit Model-Class Uncertainty / Mixture Terminal Inference

Status: RUNNING after protocol freeze.

## Rationale
S17 showed that the fixed nonlocal science posterior retains structural gains under compound nonlinear + heavy-tail shift but violates calibration. S18 and S19 then falsified increasingly elaborate abstention gates; S19 specifically missed its preregistered held-out coverage requirement. The next justified mechanism is therefore not another threshold. It is explicit uncertainty over competing structural world-model classes while preserving the supported planning/science separation invariant.

## Hypothesis
A full-coverage Bayesian mixture over distinct terminal science model classes can retain useful structural gains while reducing the calibration damage caused by committing to a single misspecified science model.

## Frozen architecture
Use the exact S17 compound-shift environment and exact baseline Gaussian planning posterior/controller. No science-posterior quantity may influence intervention selection. Reconstruct terminal science inference only after the intervention trace is complete.

At terminal inference compute three DAG posteriors from the same frozen data:
1. `M0 baseline-linear`: benchmark-v2 Gaussian linear family evidence with the committed broad coefficient prior.
2. `M1 nonlocal-linear`: the frozen S5 nonlocal coefficient prior on linear parent effects.
3. `M2 nonlocal-tanh`: the same frozen S5 nonlocal coefficient prior, but each candidate parent enters the regression as `tanh(parent_value)`.

Assign equal model-class prior probability 1/3. For each class, compute its marginal evidence by summing the unnormalized DAG evidence over the exact 29,281-DAG support under a uniform DAG prior. Normalize those three class evidences to obtain posterior model-class weights. The terminal mixture posterior is the weighted sum of the three normalized DAG posteriors. This mixture is used only for terminal structural output.

No gate, abstention threshold, oracle label, or ground-truth quantity participates in model weighting.

## Controls and metrics
Mandatory matched controls on every world:
- planning control: exact terminal baseline posterior produced by the unchanged planner;
- fixed-science control: frozen S5 nonlocal-linear terminal posterior;
- treatment: S20 model-class mixture posterior.

Record edge error, Brier, true-DAG mass, MAP recovery, entropy, model-class weights, exact action trace, spend, posterior normalization, and paired deltas treatment-minus-planning-control and treatment-minus-fixed-science.

## Mechanics gate
Fresh seeds 69901-69904. Must establish before efficacy exposure:
- exact planning trace identity by construction;
- spend <= 15;
- all three class posteriors and mixture posterior finite and normalized;
- class weights finite, nonnegative, sum to 1;
- exact DAG support count 29,281.

## Prospective screen
Only after mechanics pass: fresh seeds 69911-69922 (n=12).
Advance only if all are true:
- mean mixture edge delta vs planning control <= -0.10;
- mean mixture Brier delta vs planning control <= +0.005;
- no more than 2/12 worlds have edge harm > +0.50 vs planning control;
- mixture mean Brier is no worse than fixed S5 by more than +0.002;
- exact planning-trace identity and mechanics invariants hold.

## Held-out confirmation
Only if screen passes: fresh seeds 70001-70036 (n=36).
Promotion requires all:
- mean mixture edge delta vs planning control <= -0.10;
- paired bootstrap 95% upper bound for mixture edge delta vs planning control < 0;
- mean mixture Brier delta vs planning control <= +0.005;
- no more than 4/36 worlds have edge harm > +0.50 vs planning control;
- mixture mean Brier is no worse than fixed S5 by more than +0.002;
- 100% coverage, exact planning-trace identity, and all mechanics invariants.

## Falsification / redirect
If the mixture fails, do not tune class weights on the same worlds. Diagnose whether failure is due to model-evidence domination, insufficient model-class diversity, or shared likelihood misspecification. A successor must materially change the represented model class or evidence-combination mechanism, not add another abstention threshold.
