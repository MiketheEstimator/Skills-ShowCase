# EXP-002S17 Evaluation — Compound Nonlinear + Heavy-Tail Shift

## Disposition
`COMPLETE_FALSIFIED_CALIBRATION_GUARDRAIL`

The frozen S15 disagreement gate (`D <= 1.50`) transferred structurally but not calibration-wise when nonlinear `tanh(parent)` mechanisms and standardized Student-t(df=3) noise were combined.

## Held-out confirmation
- Total worlds: 24
- Promoted: 21 (87.5% coverage)
- Mean promoted edge delta: -0.3581
- Paired bootstrap 95% interval: [-0.5027, -0.2073]
- Promoted wins: 17
- Promoted large harms >0.50: 0
- Mean promoted Brier delta: +0.00885
- Planning traces: identical in all worlds

The structural criteria passed comfortably, but the frozen Brier guardrail of <= +0.005 failed. This is a valid scientific falsification rather than an execution failure.

## Interpretation
The nonlocal science posterior remains useful under the compound shift, because structural recovery is still materially better and no promoted large harms occurred. The failure is specifically that the one-dimensional total edge-marginal disagreement statistic is insufficient to detect overconfident/miscalibrated science-posteriors when multiple forms of model mismatch occur together.

## Next uncertainty
Do not retune the exposed D threshold. Test a preregistered multi-signal abstention detector using independently observable planning-vs-science disagreement features, with fresh training, validation, and held-out confirmation worlds.