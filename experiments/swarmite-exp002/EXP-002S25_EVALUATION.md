# EXP-002S25 Evaluation

**Disposition:** FALSIFIED_AT_SCREEN

## Screen
- Overall edge delta: -0.382705
- Overall Brier delta: 0.004363
- Large harms: 3
- By regime: `{'linear_gaussian': {'n': 4, 'mean_edge_delta': 0.5979370031976948, 'mean_brier_delta': 0.04562491480274012, 'wins': 2, 'large_harms': 2}, 'tanh_t3': {'n': 4, 'mean_edge_delta': 0.19130195286110396, 'mean_brier_delta': 0.03788891951837746, 'wins': 2, 'large_harms': 1}, 'softsign_t5': {'n': 4, 'mean_edge_delta': -1.3665704821500193, 'mean_brier_delta': -0.03826035207380773, 'wins': 4, 'large_harms': 0}, 'arctan_laplace': {'n': 4, 'mean_edge_delta': -0.9534880072722726, 'mean_brier_delta': -0.027802755882914015, 'wins': 3, 'large_harms': 0}}`

## Next
S25 failed heterogeneous transfer; isolate the failing regime and mechanism before changing the supported S23/S24 inference.