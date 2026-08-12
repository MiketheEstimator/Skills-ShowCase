# EXP-002S71 Observable Response-State Conditional Calibration Diagnostic

## Hypothesis
S70 failed because predictive dispersion alone aliases distinct intervention-response states. A richer deployment-observable state can condition predictive bias and scale without hidden regime labels.

## Frozen representation
For each target/setpoint/response cell, construct only truth-free features available before observing the new intervention response: log posterior-predictive SD, absolute predictive mean, signed setpoint, target index, response index, and posterior graph entropy. No regime label or realized response enters the feature vector.

## Calibration mechanism
Fit regularized linear bias and log-scale models on standardized residuals. Bias is ridge regression of z. Scale is ridge regression of log squared bias-corrected residual with clipping to [0.5,2.0]. Standardize continuous features using training-only moments. Four-fold world-level cross-fitting measures training generalization.

## Prospective splits
Mechanics: 2+2 fresh worlds. Calibration/training: 64+64 fresh worlds. Held-out evaluation: disjoint 64+64 fresh worlds. S69/S70 seed namespaces are not reused.

## Matched control
Raw uncalibrated posterior-predictive response distribution from the frozen S69 simulator.

## Success criteria
On held-out worlds: mean nominal coverage error across 80% and 95% intervals improves by >=20%; neither regime's coverage error worsens by >0.02; each regime has 80% coverage in [0.74,0.86], 95% coverage in [0.91,0.98], and standardized-residual RMS in [0.85,1.15].

## Falsification redirect
If unsupported, do not tune ridge strength, clipping, or feature subsets. Redirect from moment calibration toward distributional/non-Gaussian predictive calibration or empirical conformal response sets. If supported, freeze the calibrator and retest branch-aware planning against EIG without retuning.
