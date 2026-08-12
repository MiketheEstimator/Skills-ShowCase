# EXP-002S28 Evaluation

**Disposition:** MULTIVARIATE_REPRESENTATION_NOT_SUPPORTED

Tail-only CV AUC: 0.3167
Multivariate CV AUC: 0.5200
AUC gain: 0.2033
Multivariate balanced accuracy: 0.4706

## Regime error counts
- **arctan_laplace**: n=24, beneficial=18, FN=3, FP=6
- **linear_gaussian**: n=24, beneficial=9, FN=0, FP=15
- **softsign_t5**: n=24, beneficial=18, FN=0, FP=6
- **tanh_t3**: n=24, beneficial=23, FN=1, FP=1

## Next
S28 did not show enough incremental selector information in posterior disagreement plus residual summaries; test a materially different observable model-adequacy representation rather than tuning classifiers or thresholds.