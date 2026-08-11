# EXP-002S40 — Frozen Credal Gate under Heteroskedastic Nonlinear Shift

## Hypothesis
The S39 specialist-disagreement gate captures epistemic instability rather than only the six S32 benchmark cells. Therefore the exact frozen S39 gate should remain useful when noise variance becomes state-dependent, without retuning its score or threshold.

## Frozen treatment
- Point science posterior: S30 exactly.
- Uncertainty score: S39 `mean_credal_width` exactly.
- Frozen threshold: `0.2692013432171404`.
- Promote S30 only when score <= threshold; otherwise abstain and fall back to the committed baseline posterior.
- No specialist posterior may replace or shift S30.

## New world family
Use the committed 5-node DAG generator, intervention budget, candidate proposals, planning posterior, and RNG isolation. Replace the S32 homoskedastic observation noise with state-dependent Gaussian noise while retaining nonlinear mechanisms `tanh`, `sin`, and `asinh`.

For nonintervened node v, let `mu = f(x) @ W[:,v]` and sample noise with standard deviation `sigma = clip(0.55 + 0.35*abs(mu), 0.55, 1.80)`. Then `x_v = mu + Normal(0,sigma^2)`. This heteroskedastic law is not represented by any specialist likelihood used to construct S30 or the disagreement set.

Mechanics seeds: 72501–72504.
Screen seeds: 72511–72534 (24; balanced across tanh/sin/asinh).
Confirmation seeds: 72601–72648 (48; balanced across mechanisms), exposed only if the screen passes.

## Screen gate
The frozen S39 rule advances only if:
- mechanics invariants all pass,
- coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta vs baseline < 0,
- hybrid mean Brier delta vs baseline <= +0.005,
- if always-S30 is beneficial on average, the gate retains >= 0.70 of that improvement.

## Confirmation promotion
Promotion requires:
- coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta vs baseline < 0,
- bootstrap 95% upper bound for hybrid edge delta < 0,
- hybrid mean Brier delta <= +0.005,
- improvement retention >= 0.70 when always-S30 is beneficial,
- all mechanics invariants pass.

## Interpretation
Success supports specialist disagreement as a transferable credal uncertainty layer around S30. Failure falsifies simple transfer of the scalar credal-width gate and redirects to explicit world-class uncertainty, not gate retuning on the heteroskedastic worlds.