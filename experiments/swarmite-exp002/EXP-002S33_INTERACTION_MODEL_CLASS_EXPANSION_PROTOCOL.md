# EXP-002S33 — Mechanism×Noise Interaction Model-Class Expansion Screen

## Status
PENDING until execution workflow atomically marks RUNNING.

## Rationale
S31 falsified transfer of the frozen S30 baseline+tanh-robust continuous posterior mixture. S32 then factorized the failure across tanh/sin/asinh mechanisms and Gaussian/t7 noise and found no single mechanism or noise marginal sufficient to explain the boundary. This supports a model-set insufficiency hypothesis at the mechanism×noise interaction level rather than another selector or threshold tweak.

## Hypothesis
A small terminal-only model set that explicitly spans nonlinear mechanism shape and residual family will improve terminal structural inference over the frozen S30 two-class mixture on fresh heterogeneous worlds, without changing planning actions.

## Frozen terminal model set
All worlds use the committed benchmark-v2 baseline posterior for planning. Terminal science inference computes seven posteriors from the exact same accumulated evidence:

1. `LG`: linear + Gaussian likelihood (baseline science posterior)
2. `TG`: tanh features + Gaussian likelihood
3. `TT`: tanh features + Student-t3 robust likelihood (S23 class)
4. `SG`: sin features + Gaussian likelihood
5. `ST`: sin features + Student-t3 robust likelihood
6. `AG`: asinh features + Gaussian likelihood
7. `AT`: asinh features + Student-t3 robust likelihood

For each class, a five-fold out-of-sample predictive log score is computed using only observed data and intervention-target masking. The seven terminal posteriors are combined with softmax weights `w_c ∝ exp(score_c / T)` using **T=5.0**, frozen from S30. No truth labels or regime labels enter weighting.

## Strong controls
- **Baseline control:** committed benchmark-v2 linear-Gaussian posterior and planner.
- **S30 control:** frozen two-class continuous mixture of `LG` and `TT`, with `alpha=sigmoid((score_TT-score_LG)/5)`.
- All three outputs share exactly the same intervention trace and budget.

## Worlds and stage separation
- Mechanics gate: seeds **72101–72104**. Used only to verify exact 29,281-DAG support, planning reconstruction, finite class scores, normalized posteriors, valid weights, and identical traces.
- Prospective screen: seeds **72111–72146** (36 worlds; six S32 factorial cells assigned deterministically by seed modulo six, six worlds per cell).
- No confirmation worlds are exposed unless the screen promotes.

## Primary screen criteria
S33 is `COMPLETE_SUPPORTED_SCREEN` only if all hold:
1. Mean edge-error delta **expanded minus S30 <= -0.10**.
2. Paired bootstrap 95% upper bound for expanded-minus-S30 edge delta **< 0**.
3. Mean Brier delta expanded-minus-S30 **<= +0.005**.
4. No more than **2/36** worlds worsen edge error by >0.50 versus S30.
5. Expanded mixture mean edge-error delta versus baseline is < 0.
6. Mechanics gate passes completely.

Otherwise scientific falsification is a valid completion. The successor must diagnose the observed failure mode rather than retune T or repeat hard selection.

## Scientific invariants
- Ground truth is terminal-evaluation only.
- Planning is frozen to the baseline posterior.
- Intervention budget, proposals, EIG simulations, environment RNG namespaces, and observations are matched.
- All class weights are observable-data functions only.
- Negative results and per-world class weights are preserved.
- Google Drive remains read-only.
