# EXP-002S21 — Model-Class Mixture Evidence-Dominance Diagnostic

Status: RUNNING after protocol freeze.

## Why this diagnostic is next
S20 was mechanically valid but failed decisively at its prospective screen. The equal-prior Bayesian mixture assigned 92.2% mean weight to the nonlocal-tanh class and simultaneously produced severe terminal harm. Before adding a new class or altering combination weights, determine whether the failure is primarily (A) marginal-evidence selection of the wrong available class or (B) shared inadequacy of all represented classes.

## Frozen diagnostic questions
On fresh compound-shift worlds, using the exact S17 environment and exact unchanged planning controller:
1. How concentrated are posterior model-class weights?
2. How often is the highest-evidence class also the truth-evaluated best structural class?
3. What is the structural regret of evidence selection and of the S20 mixture relative to the best represented class?
4. Do class weights correlate with mixture harm?
5. Does the dominant class exhibit systematic graph-density error relative to truth?

Ground truth is used only for this across-world diagnostic. It may not influence model weights, intervention actions, or any future promotion rule.

## Data
Fresh diagnostic seeds 70051-70074 (n=24). Do not tune or promote a policy on these worlds.

## Recorded per world
- exact planning trace and spend;
- each class posterior weight and log evidence;
- each class edge error, Brier, expected edge count, MAP correctness, and true-DAG mass;
- S20 mixture metrics;
- true edge count;
- evidence-selected class index;
- truth-evaluated best represented class index;
- evidence-selection regret = selected class edge error minus best-class edge error;
- mixture regret = mixture edge error minus best-class edge error;
- mixture harm versus planning control.

## Diagnostic interpretation, frozen before execution
Classify `EVIDENCE_DOMINANCE_FAILURE` if all hold:
- evidence-selected class is truth-best in < 50% of worlds;
- mean oracle-best represented-class edge delta versus planning control <= -0.10;
- mean evidence-selection regret >= +0.20.

Classify `SHARED_MODEL_CLASS_FAILURE` if mean oracle-best represented-class edge delta versus planning control > -0.10.

Otherwise classify `MIXED_FAILURE_MODE`.

If evidence dominance is supported, the next experiment must change evidence combination/aggregation without oracle tuning (for example robust posterior aggregation or predictive stacking trained on separate worlds). If shared model-class failure is supported, the next experiment must add a materially different likelihood/mechanism class, specifically addressing heavy-tailed nonlinear residuals. Do not return to abstention-threshold tuning.
