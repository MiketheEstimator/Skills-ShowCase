# EXP-002S4 Evaluation

## Disposition
COMPLETE_FALSIFIED_AT_SCREEN.

Blocked five-fold predictive evidence failed on every fresh screen world. Treatment-minus-control mean terminal edge-error delta was +2.3045 and mean Brier delta was +0.07289. All 12 worlds worsened by more than 0.50 edge-error units, so confirmation is prohibited by the frozen protocol.

## Scientific interpretation
S3 correctly identified the S2 warm-start density bias, but removing the unscored warm-start did not solve the larger problem. S4 remained denser than truth in all 12 worlds, with mean expected edge count 6.67 versus mean truth 3.75. This indicates that optimizing out-of-sample predictive density alone does not supply enough structural complexity discrimination for causal edge recovery in this benchmark.

The next justified mechanism should therefore alter the included-edge model itself rather than retry predictive scoring or another fixed graph sparsity penalty. The benchmark generator has a true gap between absent coefficients (exactly zero) and included effects (magnitude 0.4-0.9). A nonlocal included-edge prior that assigns low density near zero directly tests whether dense posterior graphs survive because the current Gaussian slab makes near-zero included coefficients too cheap.