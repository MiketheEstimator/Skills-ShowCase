# EXP-002S19 Evaluation

**Disposition:** FALSIFIED_ON_CONFIRMATION
**Selected gate:** `{'a': 2.0, 't': 8.0, 'n': 0.1, 'n_promoted': 12, 'coverage': 0.5, 'mean_edge_delta': -0.5687949676521885, 'mean_brier_delta': -0.0005563706706118542, 'large_harms': 0, 'wins': 10, 'qualifies': True}`

## Validation
- Coverage: 0.542
- Mean edge delta: -0.572404
- Mean Brier delta: -0.001009
- Large harms: 0

## Held-out confirmation
- Coverage: 0.479
- Mean edge delta: -0.510503
- Bootstrap 95% edge-delta CI: [-0.6123756297557961, -0.40652305468339517]
- Mean Brier delta: -0.003683
- Large harms: 0

## Next direction
Explicit model-class uncertainty / mixture-of-world-model terminal inference. Do not continue threshold proliferation.