# EXP-002S35 — Structural-Utility Stacking Without Predictive-Score Weights

## Status
PENDING until execution marks RUNNING.

## Rationale
S34 found that the seven S33 mechanism×noise classes contain useful structural solutions on every screen world, but five-fold predictive scores misrank structural utility (mean within-world Spearman -0.217; top-weight/oracle match 8.3%). This falsifies predictive fit as the weighting objective for this model set. S35 therefore removes per-world predictive weighting entirely.

## Hypothesis
A single frozen convex combination of the seven terminal science posteriors, learned only on separated training worlds to optimize worst-regime terminal structural quality, will generalize better than the frozen S30 two-class mixture without any truth-dependent deployment decision.

## Frozen model classes
Identical to S33: `LG, TG, TT, SG, ST, AG, AT`. Planning remains the benchmark-v2 linear-Gaussian posterior. Model classes affect terminal science inference only.

## Training objective
Training worlds: seeds **72201–72248** (48 worlds, deterministically balanced across the six S32 mechanism×noise cells).

Generate a deterministic candidate simplex set containing:
- all seven one-hot vertices;
- equal weights;
- 20,000 Dirichlet(1,...,1) draws from RNG namespace/seed `S35-weight-search/35235`.

For each candidate weight vector, compute class-mixture edge error using the linearity of edge marginals under posterior mixing. Select weights lexicographically by:
1. minimum **worst-cell mean edge-error delta versus frozen S30**;
2. minimum overall mean edge-error delta versus S30;
3. minimum L2 norm (prefers less concentrated mixtures on exact ties).

The selected weights are persisted before validation is exposed. Ground truth is permitted only for this training optimization.

## Validation
Validation worlds: seeds **72261–72296** (36 fresh worlds, six per factorial cell). Frozen weights only.

Advance to confirmation only if all hold:
1. mean edge-error delta stacked minus S30 <= -0.10;
2. paired bootstrap 95% upper bound < 0;
3. mean Brier delta versus S30 <= +0.005;
4. <=2/36 worlds worsen edge error by >0.50 versus S30;
5. no factorial cell has mean edge-error delta versus S30 > +0.05;
6. mechanics invariants pass.

## Held-out confirmation
Only if validation passes: seeds **72301–72372** (72 fresh balanced worlds). Promotion requires:
1. mean edge delta versus S30 <= -0.10;
2. bootstrap 95% upper bound < 0;
3. mean Brier delta <= +0.005;
4. <=4/72 large harms versus S30;
5. no cell mean edge delta > +0.05.

## Controls and invariants
- Frozen S30 two-class continuous mixture is the primary strong control.
- Baseline posterior remains secondary control.
- Same intervention traces and budgets across all terminal inference arms.
- No predictive-score weighting in the S35 treatment.
- No per-world model selector.
- Selected global weights are frozen before validation.
- Confirmation seeds remain unexecuted unless validation passes.
- Negative results are preserved; no post-hoc temperature or weight retuning.
- Google Drive remains strictly read-only.
