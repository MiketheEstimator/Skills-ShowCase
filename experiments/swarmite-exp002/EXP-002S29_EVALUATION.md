# EXP-002S29 Evaluation

**Disposition:** DIRECT_ADEQUACY_NOT_SUPPORTED

AUC: 0.6970
Balanced accuracy at ADEQ>0: 0.6796
Spearman ADEQ vs edge delta: -0.4543

## By regime
- **linear_gaussian**: median ADEQ -26.754, beneficial 9/24, FP 0, FN 9
- **tanh_t3**: median ADEQ 22.290, beneficial 23/24, FP 1, FN 1
- **softsign_t5**: median ADEQ -5.831, beneficial 18/24, FP 1, FN 13
- **arctan_laplace**: median ADEQ 8.763, beneficial 18/24, FP 4, FN 6

## Next
S29 found per-world hard model selection insufficient even with direct predictive adequacy; replace hard selection with decision-theoretic continuous combination of baseline and robust terminal posteriors.