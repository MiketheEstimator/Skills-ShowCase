# EXP-002S30 — Continuous Posterior-Combination Utility Screen

## Status
Protocol frozen before any S30 world is executed.

## Motivation
S29 found direct predictive adequacy meaningfully related to robust-posterior utility but insufficient for reliable hard switching (AUC 0.697). S30 changes the decision mechanism: instead of selecting one posterior, continuously combine the baseline and robust science posteriors with a weight derived only from direct out-of-sample model adequacy.

## Hypothesis
Soft model averaging can preserve part of the robust posterior's shifted-regime benefit while reducing catastrophic or in-distribution harms caused by all-or-nothing posterior selection.

## Frozen architecture
Planning is unchanged and uses the exact baseline posterior/controller. Terminal science inference computes:
- baseline posterior `p0`;
- frozen S23 robust posterior `pr`;
- direct predictive adequacy `ADEQ` exactly as S29: robust minus baseline 5-fold held-out log score;
- robust weight `alpha = sigmoid(ADEQ / T)`;
- combined science posterior `pmix = (1-alpha)*p0 + alpha*pr`.

The posterior mixture is normalized by construction. No ground truth, regime label, seed modulo, edge error, or Brier score enters alpha at deployment.

## Frozen temperature grid
Training may select only `T in {5, 10, 20, 40}`. No offset, threshold, clipping rule, extra feature, or alternate functional form may be tuned.

## Fresh worlds
- Training: seeds 71400-71447 (48 worlds, 12 per S25 regime).
- Validation: seeds 71500-71547 (48 worlds, 12 per regime).
- Held-out confirmation: seeds 71600-71695 (96 worlds, 24 per regime).
- All S26-S29 worlds are excluded.

## Controls
Matched baseline posterior and always-robust S23 posterior are recorded for every world. All three terminal posteriors share the identical baseline intervention trace and budget.

## Mechanics invariants
- exact 29,281-DAG support;
- spend <=15;
- baseline planning reconstruction max error <=1e-10;
- p0, pr, and pmix finite and normalized;
- ADEQ finite;
- identical action trace across terminal inference modes.

## Training qualification
A temperature qualifies only if:
1. overall mean mixed edge delta vs baseline <= -0.10;
2. overall mean mixed Brier delta <= +0.005;
3. <=5/48 mixed worlds worsen by >0.50 edge-error units;
4. linear-Gaussian mean mixed edge delta <= +0.10 and Brier <= +0.010;
5. each shifted regime mean mixed edge delta <= 0 and Brier <= +0.005.

Select the qualifying T with lowest overall mean mixed edge delta. Ties within 0.01 edge-error units choose the larger T, favoring smoother combination.
Persist the complete training grid and selected T before validation exposure.

## Validation
Advance only if the frozen selected T satisfies all training qualification conditions unchanged on seeds 71500-71547.

## Held-out confirmation promotion
Promote only if all hold on seeds 71600-71695:
1. overall mean mixed edge delta <= -0.10;
2. paired bootstrap 95% upper bound < 0;
3. overall mean mixed Brier delta <= +0.005;
4. <=8/96 large harms;
5. linear-Gaussian mean mixed edge delta <= +0.05 and Brier <= +0.005;
6. each shifted regime mean mixed edge delta < 0 with bootstrap 95% upper bound <0 and Brier <= +0.005.

## Redirect
If S30 fails, do not tune more temperatures or add ADEQ thresholds. Diagnose whether the baseline/robust posterior pair itself is insufficient as a model set; the next mechanism should expand or restructure terminal model uncertainty rather than further tune the mixing rule.
