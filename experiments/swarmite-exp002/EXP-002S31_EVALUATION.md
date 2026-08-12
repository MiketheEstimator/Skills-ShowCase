# EXP-002S31 Evaluation

**Disposition:** TRANSFER_FALSIFIED

Overall edge delta -0.208011; CI [-0.32388028667061497, -0.10387745514922234]; Brier -0.006046; harms 2; mean alpha 0.283.

## By regime
- **linear_gaussian_anchor**: edge 0.009556, CI [0.0002001982129168821, 0.027214390263671638], Brier 0.001317, alpha 0.036, ADEQ -34.176, harms 0
- **sin_gaussian**: edge 0.033219, CI [-0.011836550772212854, 0.08623652037288895], Brier 0.001686, alpha 0.119, ADEQ -20.283, harms 0
- **asinh_t7**: edge -0.223512, CI [-0.5002638239315709, 0.024730389508662128], Brier -0.005983, alpha 0.358, ADEQ -4.810, harms 1
- **leakyrelu_contaminated**: edge -0.651305, CI [-0.9303825959819241, -0.3874261307995629], Brier -0.021204, alpha 0.619, ADEQ 7.617, harms 1

## Next
S31 exposed a transfer boundary for the baseline+S23 model set; isolate the failing unseen mechanism/noise family before expanding terminal model classes.