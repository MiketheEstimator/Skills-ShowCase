# EXP-002S23 — Heavy-Tail Nonlinear Structural Likelihood Class

Status: RUNNING after protocol freeze.

## Rationale
S21 showed that useful represented classes existed, but raw model evidence selected the wrong class. S22 then showed that merely tempering those evidence weights could not rescue the represented class set even on separated training worlds. The next mechanism therefore changes the likelihood itself rather than its posterior weight.

## Hypothesis
The compound-shift calibration failure is driven in substantial part by scoring nonlinear, heavy-tailed data with Gaussian linear family evidence. A terminal structural posterior based on `tanh(parent)` regressors and a robust Student-t residual likelihood can recover terminal structural quality and calibration while leaving planning unchanged.

## Frozen treatment
Use the exact S17 compound nonlinear + heavy-tail environment and exact baseline Gaussian planning posterior/controller. Terminal treatment inference occurs only after the baseline planning trace is complete.

For every candidate child/parent family:
- design matrix: intercept plus `tanh(parent_value)` for each parent;
- residual family: Student-t with `nu=3` and scale `1/sqrt(3)` (unit residual variance under the synthetic stress model);
- coefficient prior: zero-centered Gaussian ridge with variance `TAU2=4`, matching the broad baseline prior scale;
- coefficient fit: deterministic Student-t IRLS, maximum 30 iterations, tolerance 1e-8;
- family structural score: fitted Student-t log likelihood + Gaussian log-prior penalty - `0.5 * d * log(n+1)` complexity penalty, where d is the number of fitted coefficients including intercept.

The exact 29,281-DAG posterior is formed by summing these family scores over each DAG and normalizing. This is a preregistered robust quasi-evidence approximation; it is not described as exact conjugate marginal likelihood.

No ground truth, science posterior, or robust-likelihood quantity influences planning actions.

## Mechanics
Fresh seeds 70401-70404. Require exact planning-posterior reconstruction, exact 29,281-DAG support, spend <=15, finite normalized treatment posterior, finite family scores, and unchanged planning trace.

## Prospective screen
Only after mechanics pass: seeds 70411-70422 (n=12).
Advance if:
- mean treatment edge delta vs planning control <= -0.10;
- mean treatment Brier delta vs planning control <= +0.005;
- <=2/12 worlds have edge harm > +0.50;
- exact planning-trace identity and mechanics invariants.

Also report paired performance versus frozen S5 nonlocal-linear terminal inference, but do not use that secondary comparison to override the primary criteria.

## Held-out confirmation
Only if screen passes: seeds 70501-70536 (n=36). Promote if:
- mean edge delta vs planning control <= -0.10;
- paired bootstrap 95% upper bound <0;
- mean Brier delta vs planning control <= +0.005;
- <=4/36 worlds have edge harm > +0.50;
- 100% coverage and all mechanics invariants.

## Redirect rule
If the robust likelihood fails, do not tune df, IRLS tolerance, or complexity penalty on exposed worlds. Diagnose whether failure comes from the tanh functional form, coefficient prior, or quasi-evidence scoring. A successor must change one of those mechanisms or move to nonparametric/ensemble structural evidence; it may not return to abstention thresholds or model-evidence temperature tuning.
