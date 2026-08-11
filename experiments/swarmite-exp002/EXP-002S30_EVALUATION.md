# EXP-002S30 Evaluation

**Disposition:** CONTINUOUS_COMBINATION_SUPPORTED

**Selected T:** 5.0

Overall edge delta -0.715073; CI [-0.9292696471619044, -0.5206940834588978]; Brier -0.019857; harms 4; mean alpha 0.555.

## By regime
- **linear_gaussian**: edge 0.009582, CI [-0.004607466122255724, 0.027281794659707766], Brier 0.000221, alpha 0.023, harms 0
- **tanh_t3**: edge -1.695313, CI [-2.239803662156467, -1.1979063230839615], Brier -0.052911, alpha 0.926, harms 1
- **softsign_t5**: edge -0.321840, CI [-0.56697267719985, -0.10905536751796535], Brier -0.004267, alpha 0.562, harms 2
- **arctan_laplace**: edge -0.852721, CI [-1.203970491559929, -0.5150786059979449], Brier -0.022469, alpha 0.710, harms 1

## Next
S30 supported ADEQ-weighted posterior combination; test the frozen mixing rule on unseen mechanism/noise families before promotion to reference architecture.