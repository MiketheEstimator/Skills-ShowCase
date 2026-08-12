# EXP-002R22 — Coefficient-Prior Density Diagnostic

## Status
COMPLETE_DIAGNOSTIC_SUPPORTED.

Using the R21 paired seeds 64901-64912, I reran the same mechanics while recording posterior expected edge count under TAU2=4 and TAU2=0.5.

The tighter TAU2=0.5 model increased terminal posterior expected edge count by +1.3114 edges on average relative to TAU2=4. Its mean terminal expected-edge-count bias versus ground truth was +2.3932 edges, and it overestimated true graph size in 12/12 worlds. The correlation between the treatment-minus-control edge-count shift and terminal edge-error delta was -0.327, so count shift alone does not explain severity world-by-world, but the direction of model-size distortion is unambiguous.

This falsifies the simple over-shrinkage explanation for R21. In this marginal-likelihood formulation, reducing coefficient prior variance weakens the determinant/Occam penalty sufficiently to favor dense DAGs.

## Consequence
Do not retry smaller TAU2 values. The next inference experiment should change the coefficient-prior mechanism so coefficient scale can be regularized without inducing this dimension-dependent dense-graph evidence bias. A design-adaptive g-prior is the next candidate.