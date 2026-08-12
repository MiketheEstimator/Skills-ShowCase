# EXP-002S69 Evaluation

**Disposition:** PREDICTIVE_MISCALIBRATION_SUPPORTED

S69 disposition PREDICTIVE_MISCALIBRATION_SUPPORTED. Predictive intervention-response calibration by regime: {'linear': {'n_response_cells': 2560, 'mean_standardized_residual': -0.006772905635903747, 'rms_standardized_residual': 1.0599041811871397, 'coverage80': 0.7546875, 'coverage95': 0.900390625}, 'heteroskedastic': {'n_response_cells': 2560, 'mean_standardized_residual': 0.022766061408813272, 'rms_standardized_residual': 0.6997770505823854, 'coverage80': 0.905859375, 'coverage95': 0.977734375}}.

## Next
S69 directly identified posterior-predictive intervention-response miscalibration. Build a cross-fitted regime-agnostic bias/dispersion calibration layer and retest predictive coverage before any planner promotion.
