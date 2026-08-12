# EXP-002S40 Evaluation

**Disposition:** HETEROSKEDASTIC_TRANSFER_SUPPORTED

Frozen S39 gate: `mean_credal_width <= 0.2692013432171404`

## Screen
Coverage: **0.958**
Hybrid edge delta: **-0.733**
Promoted large-harm rate: **0.043**
Brier delta: **-0.0052**

## Confirmation
Coverage: **1.000**
Hybrid edge delta: **-0.811**
95% bootstrap: **[-0.9600670631399039, -0.6557263518793027]**
Promoted large-harm rate: **0.021**
Brier delta: **0.0009**

## Next
S40 supported heteroskedastic transfer without retuning; test whether the frozen S39 uncertainty layer survives sparse/dense topology shift before architectural promotion.