# EXP-002S55 — Explicit Residual-Process Class Posterior

## Motivation
S54 preserved prospective nodewise specialist-win discrimination (training AUC 0.652; Brier 0.203 versus constant-prevalence Brier 0.216) but its deterministic local Bernoulli composition failed the frozen training qualification despite improving the paired hybrid edge metric. The justified next change is the composition semantics, not another weight threshold, cap, or temperature.

## Hypothesis
The latent residual process for each target node should remain uncertain at terminal inference. Marginalizing over discrete anchor-like versus heteroskedastic residual-process class assignments can preserve multimodality that is destroyed when S54 first averages edge marginals and then reconstructs a single pseudo-posterior. Exact class marginalization over node assignments may exploit the observable S54 discrimination while avoiding deterministic local collapse.

## Frozen architecture
- Planning remains the baseline planner with intervention budget 15.
- Outer promotion/adjudication remains the frozen S46 continuous-risk gate.
- Structural anchor remains the frozen S30 posterior.
- Heteroskedastic specialist remains the frozen S49 posterior.
- Observable node representation and its training-only ridge/logistic fitting remain frozen from S54.
- Candidate DAG universe, scoring, metrics, and matched-world RNG isolation remain benchmark v2.
- No threshold grid, cap grid, temperature tuning, or hard class selection is permitted.
- Validation and confirmation truth remain unopened until preceding gates pass.

## Explicit residual-process class posterior
For target node v, let q_v be the S54 training-only logistic estimate that the heteroskedastic specialist has lower incoming-edge error than S30.

Introduce latent class z_v in {A,H}, where A uses S30 incoming-edge marginals and H uses P_HET incoming-edge marginals. Assume the terminal class posterior factorizes across target nodes only for the class prior:

`q(z) = product_v q_v^(I[z_v=H]) (1-q_v)^(I[z_v=A])`.

For each of the 2^N residual-class assignments z, construct a normalized DAG pseudo-posterior using the selected model's incoming-edge marginals for each target node:

`P(G | z) proportional to product_(u->v) m_(z_v,uv)^I_G (1-m_(z_v,uv))^(1-I_G)`.

The S55 terminal posterior is the exact finite mixture:

`P55(G) = sum_z q(z) P(G | z)`.

This differs materially from S54. S54 forms one deterministic averaged edge-marginal field before DAG reconstruction. S55 retains discrete residual-process uncertainty through DAG reconstruction and marginalizes only afterward.

## Prospective splits
Fresh external-seed namespaces disjoint from S54:
- Mechanics: 2 linear + 2 heteroskedastic worlds.
- Training: 64 linear + 64 heteroskedastic worlds.
- Validation: 32 linear + 32 heteroskedastic worlds.
- Held-out confirmation: 64 linear + 64 heteroskedastic worlds.

## Matched control
Frozen S46 outer gate with S30 terminal posterior on the identical world, data, planner trace, interventions, RNG-isolated observations, and budget.

## Metrics
- paired hybrid terminal edge-error difference, S55 minus control;
- bootstrap 95% interval for paired edge difference;
- hybrid Brier delta;
- promoted large harms (>0.50 edge-error increase);
- linear and heteroskedastic regime-specific paired differences;
- mean posterior heteroskedastic class mass and mean class entropy;
- node specialist-win AUC and Brier using the frozen S54 observable representation;
- outer coverage and trace identity.

## Training qualification
All must hold:
1. mechanics and trace identity pass;
2. mean posterior heteroskedastic class mass is in [0.05, 0.50], proving the explicit uncertainty mechanism is active;
3. candidate hybrid mean edge delta <= control + 0.01;
4. heteroskedastic candidate edge delta <= control - 0.02;
5. linear candidate edge delta <= control + 0.02;
6. candidate promoted large harms <= control;
7. candidate hybrid mean Brier delta <= 0.005;
8. node specialist-win AUC >= 0.60 and node Brier <= constant-prevalence Brier.

## Validation qualification
Training criteria plus paired mean edge difference <= 0 and heteroskedastic paired mean edge difference <= -0.01.

## Confirmation success
Validation criteria plus bootstrap 95% upper bound < 0, no increase in promoted large harms, and heteroskedastic paired mean edge difference < -0.02.

## Falsification redirects
- If class discrimination remains adequate but explicit class marginalization fails structurally, do not tune q_v. The next experiment must change the residual likelihood family itself, e.g. a continuous variance-process or heavy-tail/heteroskedastic joint class.
- If discrimination collapses prospectively (AUC < 0.60 or Brier worse than constant), the next experiment must improve observable residual-state representation rather than another mixture rule.
- If validation or confirmation fails after training passes, preserve the result as negative transfer and test a richer residual-process class family without retuning S55.
- If confirmation succeeds, freeze S55 and run breadth transfer across weak-effect, nonlinear/heavy-tail, topology, joint, and heteroskedastic regimes without retuning.
