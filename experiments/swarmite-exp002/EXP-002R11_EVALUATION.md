# EXP-002R11 Evaluation

EXP-002R11 completed all 12 preregistered worlds (58001-58012) under the frozen benchmark-v2 engine.

## Result
Posterior-predictive discrepancies were measurable: mean energy discrepancy 0.1294, mean absolute outcome-mean error 0.3442, mean absolute log variance-ratio error 0.2795, and empirical 90% predictive coverage 0.8675.

The decision-mechanism criterion was not supported. Mean within-world Spearman correlation between calibration error and EIG rank error was +0.1242 with bootstrap 95% CI [-0.0556,+0.3010]. Mean correlation between calibration error and terminal badness was -0.0051 with bootstrap 95% CI [-0.1869,+0.2000]. Pooled correlations were likewise weak (+0.0456 for rank error and +0.0716 for terminal badness).

High-precision one-step EIG remained only weakly aligned with terminal recovery (mean rho +0.1879), and its selected action carried mean hindsight terminal edge-error regret 0.6402.

## Disposition
`COMPLETE_FALSIFIED_DOMINANT_MISCALIBRATION`

The posterior predictive is imperfect, but the preregistered evidence does not support its calibration error as the dominant cause of intervention-ranking or terminal-recovery failure. The queue therefore redirects to horizon mismatch rather than another calibration correction.

## Successor
EXP-002R12 tests a materially different mechanism: budget-aware terminal value of information. It evaluates actions by posterior-predictive terminal edge uncertainty after spending the remaining intervention budget, rather than by immediate entropy reduction alone. Seeds 59001-59006 and the success thresholds were frozen before execution.