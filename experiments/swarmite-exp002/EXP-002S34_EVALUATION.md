# EXP-002S34 Evaluation

**Disposition:** PREDICTIVE_WEIGHT_MISALIGNMENT

Represented class beats S30 rate: **1.000**
Mean within-world Spearman predictive score vs structural utility: **-0.217**
Top-weight class equals oracle represented class: **0.083**
Mean expanded-mixture regret vs oracle represented class: **0.731**
Mean S30 regret vs oracle represented class: **0.669**

## Oracle class counts
- **LG**: 5
- **TG**: 0
- **TT**: 4
- **SG**: 3
- **ST**: 16
- **AG**: 1
- **AT**: 7

## Top-weight class counts
- **LG**: 10
- **TG**: 11
- **TT**: 0
- **SG**: 8
- **ST**: 1
- **AG**: 5
- **AT**: 1

## Next
S34 shows represented useful classes exist but predictive CV scores misrank structural utility; test a materially different training-only stacking objective based on terminal structural surrogate, with held-out validation and no truth at deployment.