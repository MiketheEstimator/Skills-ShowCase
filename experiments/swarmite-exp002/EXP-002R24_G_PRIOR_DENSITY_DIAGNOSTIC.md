# EXP-002R24 — g-Prior Density Diagnostic

## Status
COMPLETE_DIAGNOSTIC_SUPPORTED.

## Purpose
Explain the R23 efficacy failure without generating a second efficacy claim. The same R23 screen worlds 65111-65122 were reused only to compare posterior expected graph size against the committed control and true graph size after terminal inference.

## Result
The g-prior increased posterior expected graph size relative to control in 12/12 worlds. Mean expected-edge-count shift was +0.76324 edges. Mean absolute terminal edge-count bias increased from 1.21368 edges under control to 1.97691 under the g-prior.

Per-world g-prior minus control expected-edge-count deltas were all positive: +0.910, +0.661, +0.546, +0.509, +0.774, +0.742, +0.570, +0.851, +1.104, +0.424, +1.404, +0.662.

## Interpretation
R23 reproduces the same qualitative density pathology diagnosed in R22 even though the coefficient prior geometry is materially different. This weakens the hypothesis that isotropic shrinkage alone caused the problem. The more general vulnerability appears to be the fixed-noise Gaussian family marginal-likelihood formulation and its sensitivity to coefficient-prior volume/Occam factors.

## Successor justification
Do not retry another coefficient covariance or graph sparsity penalty. The next experiment should change the likelihood mechanism itself by integrating residual scale uncertainty rather than holding noise variance fixed at 1. A conjugate scale-integrated family evidence model is materially different from R17-R23 and directly tests the revised mechanism.