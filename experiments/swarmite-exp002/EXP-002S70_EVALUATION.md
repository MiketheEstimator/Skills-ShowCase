# EXP-002S70 Evaluation

**Disposition:** RESPONSE_CALIBRATION_FALSIFIED

S70 disposition RESPONSE_CALIBRATION_FALSIFIED. Held-out calibration: {'linear': {'raw': {'mean': -0.00340779803276193, 'rms': 1.0483747101584382, 'coverage80': 0.786328125, 'coverage95': 0.934375}, 'calibrated': {'mean': 0.0011569964963933476, 'rms': 1.214731894372649, 'coverage80': 0.71484375, 'coverage95': 0.8953125}}, 'heteroskedastic': {'raw': {'mean': -0.002256112586164241, 'rms': 0.7014113811742843, 'coverage80': 0.925390625, 'coverage95': 0.98984375}, 'calibrated': {'mean': 0.0012396982104340634, 'rms': 0.8060548082584313, 'coverage80': 0.8875, 'coverage95': 0.97890625}}}; coverage-error summary: {'raw_mean': 0.09726562500000002, 'calibrated_mean': 0.128125, 'relative_improvement': -0.31726907630522044}.

## Next
S70 falsified global predictive-dispersion conditioning. Test richer truth-free response-state features for calibration heterogeneity before any further planner modification; do not retune S70 bins or shrinkage.
