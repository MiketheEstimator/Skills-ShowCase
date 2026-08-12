# EXP-002S43 — Class-Aware Uncertainty Decision over S30 Anchor

## Motivation
S41 showed that the scalar S39 gate remains safe under graph-density shift but over-abstains, retaining only 45.4% of S30 benefit. S42 then established a validated observable sparse-vs-dense world-class posterior that discriminates topology materially better than scalar credal width.

## Hypothesis
A decision rule that propagates explicit topology-class uncertainty into expected S30 utility can recover the benefit lost by the scalar gate while preserving its harm guardrail. The S30 point posterior remains unchanged; only the publish-vs-fallback decision changes.

## Frozen architecture
For each world compute `q = P(dense | data)` using the exact S42 edge-count evidence posterior. S30 remains the science point posterior. Baseline remains the abstention fallback.

Training estimates only four class-level quantities from ground-truth evaluation on training worlds:
- mean S30 edge delta vs baseline in sparse worlds,
- mean S30 edge delta vs baseline in dense worlds,
- S30 large-harm rate (`edge delta > 0.50`) in sparse worlds,
- S30 large-harm rate in dense worlds.

At deployment calculate:
`expected_delta = (1-q)*mu_sparse + q*mu_dense`
`expected_harm = (1-q)*h_sparse + q*h_dense`

Promote S30 iff `expected_delta < 0` and `expected_harm <= 0.05`; otherwise fall back to baseline. There is no threshold search.

## Matched control
Evaluate the exact frozen S39 rule (`mean_credal_width <= 0.2692013432171404`) on the same worlds.

## Prospective splits
Training seeds: 73101–73148 (48 balanced sparse/dense × S32 cells).
Validation seeds: 73161–73196 (36), unavailable to training estimates.
Confirmation seeds: 73201–73248 (48), exposed only after validation passes.

## Validation success
- mechanics invariants hold,
- class-aware coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta vs baseline < 0,
- hybrid Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.70,
- class-aware hybrid mean edge delta is no worse than frozen S39 control by >0.02.

## Confirmation promotion
Require all validation criteria plus bootstrap 95% upper bound for class-aware hybrid edge delta < 0.

## Interpretation
Success supports explicit world-class uncertainty as a decision layer around the S30 anchor. Failure means topology class alone is insufficient for safe utility prediction and redirects to a joint mechanism-noise-topology latent class model, not another scalar gate.