# EXP-002S42 — Explicit Topology World-Class Uncertainty

## Motivation
S41 falsified transfer of the scalar S39 credal-width gate under graph-density shift because it abstained too aggressively from beneficial S30 outputs. Safety remained acceptable, but only 45.4% of S30 improvement was retained. The next mechanism must therefore represent the shifted topology class explicitly rather than retune a scalar disagreement threshold.

## Hypothesis
A latent sparse-vs-dense world-class posterior derived from the observed interventional dataset can identify topology regime more faithfully than the S39 scalar disagreement score. If topology class is inferable without ground-truth leakage, a later decision rule can condition uncertainty handling on that posterior while retaining S30 as the point-estimate anchor.

## Frozen world-class model
Use two generator-informed edge-count evidence classes over the exact 29,281 DAG support:
- sparse class prior weight proportional to `0.15^k * 0.85^(10-k)`,
- dense class prior weight proportional to `0.55^k * 0.45^(10-k)`,
where `k` is DAG edge count.

For each class, combine this prior with the committed family marginal-likelihood scores from the terminal observational/interventional dataset and compute class log evidence by log-sum-exp over DAGs. Use equal 0.5/0.5 class prior and normalize to obtain `P(dense | data)`. This posterior is used only as a world-class uncertainty representation; it does not alter the S30 point posterior.

## Matched control
The control topology signal is the already-frozen S39 `mean_credal_width` score computed from S30 and six specialist posteriors. Compare world-class discrimination using ROC AUC. No control threshold is retuned.

## Prospective data
Generate fresh balanced sparse/dense worlds with edge probabilities 0.15 and 0.55 using the S41 graph generator and the committed S32 six mechanism/noise cells.

Training/diagnostic seeds: 72901–72948 (48).
Validation seeds: 72961–73008 (48), exposed only after mechanics pass.

No parameter is learned from training; the training split exists to verify mechanics and preregistered direction before validation.

## Success criteria
Mechanics must hold: finite normalized class posterior, no use of true density label inside class evidence, exact DAG support, budget <=15, and S30 point posterior unchanged.

Validation supports explicit topology uncertainty only if all hold:
- density-class ROC AUC >= 0.75,
- binary Brier score <= 0.20,
- classification accuracy at posterior 0.5 >= 0.70,
- AUC improvement over S39 mean-credal-width control >= 0.10.

## Interpretation
Success establishes an observable latent topology-class signal and enqueues a class-aware uncertainty decision experiment. Failure falsifies this edge-count-evidence representation and redirects to richer world-class models (mechanism × noise × topology), not another scalar credal threshold.