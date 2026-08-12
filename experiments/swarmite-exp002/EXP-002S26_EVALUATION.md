# EXP-002S26 Evaluation

**Disposition:** REGIME_SPECIFIC_SELECTOR_JUSTIFIED

## Regimes
- **linear_gaussian**: ROBUST_HARMFUL; edge 0.467248, CI [0.0030583125442800725, 1.0235608966020917], Brier 0.034211, harms 8, D 1.782, tail 1.844, nonlinear 0.037
- **tanh_t3**: ROBUST_SUPPORTED; edge -1.403086, CI [-1.6862811949438392, -1.126307499723751], Brier -0.042547, harms 0, D 2.127, tail 23.646, nonlinear 0.041
- **softsign_t5**: ROBUST_SUPPORTED; edge -0.653488, CI [-0.9055320235927904, -0.3974737714373573], Brier -0.010285, harms 0, D 1.817, tail 8.682, nonlinear 0.026
- **arctan_laplace**: ROBUST_SUPPORTED; edge -0.722003, CI [-0.9900661639325027, -0.4615177817741896], Brier -0.013853, harms 0, D 1.909, tail 6.903, nonlinear 0.049

## Next
S26 supports robust inference on shifted regimes but harms in-distribution linear-Gaussian worlds; learn an observable selector on separate worlds, with no truth inputs at deployment.