# EXP-002S53 — Calibrated Residual-State Terminal Model Averaging

## Motivation
EXP-002S51 established nonzero heteroskedastic specialist headroom but weak scalar discrimination. EXP-002S52 replaced the scalar signal with a 42-feature cross-fitted latent residual-state representation. On its frozen training set, the latent model achieved useful specialist-win discrimination (AUC about 0.836; Brier about 0.124 versus constant-prevalence Brier about 0.166), yet every preregistered hard-selection rule selected the specialist zero times and therefore failed the training gate. This is a hard-decision failure, not evidence that the latent representation is useless.

## Hypothesis
A bounded, continuous terminal-only model average driven by the frozen S52 latent residual-state predictions can exploit specialist headroom without the brittle zero-use behavior of hard selection and without repeating S50's scalar variance-evidence mixture.

## Frozen architecture
- Planning policy: unchanged baseline planner, intervention budget 15.
- Outer promotion/adjudication: frozen S46 continuous-risk gate.
- Anchor posterior: frozen S30 terminal posterior.
- Specialist posterior: frozen S49 heteroskedastic likelihood posterior.
- Residual representation/model: frozen S52 feature map and S52 training-model coefficients from `EXP-002S52_TRAINING_RESULT.json`.
- No validation or confirmation ground truth may influence rule selection.

## Candidate mechanism
For each world, S52 produces predicted specialist-win probability `p` and predicted specialist gain `g` using observable terminal features only. Define continuous specialist mass

`w = cap * p^gamma * sigmoid(g / gain_scale)`

and terminal posterior

`P53 = (1-w) * P30 + w * P_HET`.

This differs materially from:
- S50: scalar `q_het`-driven mixture;
- S52: hard specialist selection using fixed probability/gain cutoffs.

Frozen training grid:
- `cap ∈ {0.10, 0.20, 0.30, 0.40}`
- `gamma ∈ {0.5, 1.0, 2.0}`
- `gain_scale ∈ {0.05, 0.10, 0.20}`

Tie-break toward lower cap, then higher gamma, then larger gain scale when candidates are within 0.01 heteroskedastic edge delta.

## Prospective splits
Fresh external-seed namespaces, disjoint from S52:
- Mechanics: 2 linear + 2 heteroskedastic worlds.
- Training: 64 linear + 64 heteroskedastic worlds.
- Validation: 32 linear + 32 heteroskedastic worlds.
- Held-out confirmation: 64 linear + 64 heteroskedastic worlds.

## Matched control
Frozen S46 outer promotion with S30 as the terminal posterior on the exact same worlds, interventions, RNG-isolated traces, and budget.

## Metrics
- paired hybrid terminal edge-error difference candidate minus frozen control;
- bootstrap 95% interval of paired difference;
- hybrid Brier delta versus baseline;
- promoted large harms (>0.50 edge-error increase);
- linear and heteroskedastic regime-specific edge deltas;
- mean specialist mixture weight overall and by regime;
- coverage under the unchanged S46 gate.

## Training qualification
A candidate qualifies only if:
1. mechanics pass and S46 traces remain identical;
2. mean specialist weight is between 0.01 and 0.20;
3. candidate hybrid mean edge delta is no worse than control by >0.01;
4. heteroskedastic candidate edge delta improves control by at least 0.02;
5. linear candidate edge delta is no worse than control by >0.02;
6. candidate promoted large harms do not exceed control;
7. candidate hybrid mean Brier delta <= 0.005.

## Validation qualification
All training criteria plus:
- paired mean edge difference <= 0;
- heteroskedastic paired mean difference <= -0.01.

## Confirmation success
All validation criteria plus:
- bootstrap 95% upper bound of paired edge difference < 0;
- no increase in promoted large harms;
- heteroskedastic paired mean edge difference < -0.02.

## Falsification redirects
- No training candidate qualifies: latent residual-state soft averaging is falsified; next experiment must change the specialist representation/likelihood or use nodewise posterior composition, not retune caps/temperatures.
- Training passes but validation fails: test nodewise/localized residual-process composition.
- Confirmation fails: preserve as negative transfer and redirect to explicit posterior uncertainty over residual process classes.
- Confirmation succeeds: freeze S53 and test breadth transfer across weak-effect, compound nonlinear/heavy-tail, topology, and joint regimes without retuning.
