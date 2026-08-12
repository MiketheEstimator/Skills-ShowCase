# EXP-002S27 Evaluation

**Disposition:** FROZEN_SELECTOR_FAILED_CONFIRMATION

**Selected threshold:** 6.0

Overall edge delta: -0.275561; CI [-0.4094254684489801, -0.15035647134837937]; Brier -0.007016; large harms 1.

## By regime
- **linear_gaussian**: edge 0.000000, CI [0.0, 0.0], Brier 0.000000, robust selected 0/24, harms 0
- **tanh_t3**: edge -0.557615, CI [-0.8748581248045908, -0.2763900858741995], Brier -0.015769, robust selected 12/24, harms 0
- **softsign_t5**: edge -0.148143, CI [-0.4027810798641452, 0.1138183290116294], Brier -0.002163, robust selected 9/24, harms 1
- **arctan_laplace**: edge -0.396486, CI [-0.7016051167950242, -0.12937890574537086], Brier -0.010131, robust selected 11/24, harms 0

## Next
S27 prospectively falsified the frozen one-dimensional PPC-tail selector; diagnose false robust/baseline selections using preregistered multivariate observable features before any new selector is trained.