# EXP-002S70 — Cross-Fitted Intervention-Response Calibration Layer

## Hypothesis
S69's regime-dependent posterior-predictive coverage error can be reduced without regime labels or ground-truth leakage by calibrating standardized predictive residual bias and dispersion as a function only of the model's own predictive dispersion.

## Frozen design
- Preserve the S69 posterior, simulator, intervention targets, setpoints, and 32 predictive draws.
- Calibration inputs are truth-free at deployment: predictive mean and predictive standard deviation only.
- Training labels are realized intervention responses from a disjoint calibration panel.
- Fit five quantile bins of log predictive SD. In each bin estimate standardized-residual bias and centered dispersion, shrunk toward the global estimates with 100 pseudo-observations.
- Verify the calibration layer by four-fold world-level cross-fitting on the training panel, then freeze a full-training calibrator and evaluate on a fresh held-out panel.
- Never use regime labels in fitting or application. Regime is revealed only for post-hoc scoring.

## Worlds
- Mechanics: 2 linear + 2 heteroskedastic fresh worlds.
- Calibration training: 64 + 64 fresh worlds.
- Held-out evaluation: 64 + 64 fresh worlds, disjoint seeds.

## Controls and metrics
Compare raw versus calibrated standardized residual RMS and nominal normal 80%/95% interval coverage, overall and separately by hidden regime. Record absolute coverage error from nominal and cross-fitted training performance.

## Success criteria
SUPPORTED only if all of the following hold on held-out worlds:
1. finite mechanics and calibration;
2. mean absolute 80/95 coverage error across regimes decreases by at least 20% versus raw;
3. neither regime's combined 80/95 absolute coverage error worsens by more than 0.02;
4. calibrated 80% coverage is in [0.74,0.86] and calibrated 95% coverage in [0.91,0.98] in each regime;
5. calibrated RMS standardized residual is in [0.85,1.15] in each regime.

Failure is scientifically informative. If global truth-free dispersion conditioning cannot jointly calibrate both hidden regimes, the successor must model richer observable response-state structure rather than tune bins or shrinkage.
