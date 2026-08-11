# EXP-002S32 Evaluation

**Disposition:** MECHANISM_NOISE_INTERACTION_OR_MIXED_GAP

## Factorial cells
- **tanh_gaussian**: UNRESOLVED; edge -0.029343, CI [-0.10276019026023797, 0.014344253445597232], Brier -0.000364, alpha 0.061, ADEQ -23.284, robust-edge 0.056992
- **tanh_t7**: UNRESOLVED; edge -0.049935, CI [-0.2800435047586651, 0.17654652983598412], Brier 0.005166, alpha 0.402, ADEQ -1.733, robust-edge -0.221687
- **sin_gaussian**: UNRESOLVED; edge 0.046606, CI [-0.02700672432067713, 0.14766341962277327], Brier 0.002261, alpha 0.095, ADEQ -19.121, robust-edge 0.239042
- **sin_t7**: SUPPORTED; edge -0.086727, CI [-0.1799253600930977, -0.0012863291927297377], Brier 0.001092, alpha 0.328, ADEQ -8.596, robust-edge -0.136712
- **asinh_gaussian**: UNRESOLVED; edge 0.006308, CI [-0.005373190516321699, 0.022738581074675638], Brier 0.000408, alpha 0.029, ADEQ -30.035, robust-edge 0.337883
- **asinh_t7**: UNRESOLVED; edge -0.183629, CI [-0.5539645460853179, 0.07936290044282948], Brier -0.002095, alpha 0.260, ADEQ -8.948, robust-edge -0.430676

## Mechanism marginals
- **tanh**: UNRESOLVED; edge -0.039639, CI [-0.15470795105730556, 0.0785843083526106], Brier 0.002401
- **sin**: UNRESOLVED; edge -0.020060, CI [-0.08525416792504513, 0.0475628334731583], Brier 0.001677
- **asinh**: UNRESOLVED; edge -0.088660, CI [-0.27125911169439365, 0.04245268768252583], Brier -0.000844

## Noise marginals
- **gaussian**: UNRESOLVED; edge 0.007857, CI [-0.028768588377878254, 0.047315182711479574], Brier 0.000768
- **t7**: UNRESOLVED; edge -0.106763, CI [-0.24912397734802794, 0.01702865607881224], Brier 0.001388

## Next
S32 found a mixed interaction boundary rather than a single mechanism/noise defect; test a small preregistered expanded terminal model set before changing weighting rules.