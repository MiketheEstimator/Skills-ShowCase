# EXP-002S71 Evaluation

**Disposition:** RESPONSE_STATE_CALIBRATION_FALSIFIED

S71 disposition RESPONSE_STATE_CALIBRATION_FALSIFIED. Held-out calibration: {'linear': {'raw': {'mean': -0.007553812154990252, 'rms': 1.0482071901786238, 'coverage80': 0.783984375, 'coverage95': 0.943359375}, 'calibrated': {'mean': -0.03549845802401659, 'rms': 1.9813873616903053, 'coverage80': 0.48125, 'coverage95': 0.67421875}}, 'heteroskedastic': {'raw': {'mean': 0.0001336232761186898, 'rms': 0.6977648233463519, 'coverage80': 0.93359375, 'coverage95': 0.988671875}, 'calibrated': {'mean': 0.027533787367992408, 'rms': 1.3804204653369783, 'coverage80': 0.6765625, 'coverage95': 0.857421875}}}; coverage-error summary: {'raw_mean': 0.09746093750000001, 'calibrated_mean': 0.4052734375, 'relative_improvement': -3.1583166332665327}.

## Next
S71 falsified conditional Gaussian moment calibration. Test distribution-free empirical/conformal response sets using truth-free grouping; do not retune S70/S71 moment models.
