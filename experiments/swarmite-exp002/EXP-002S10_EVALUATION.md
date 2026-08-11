# EXP-002S10 Evaluation

## Disposition
`COMPLETE_FAILED_CALIBRATION_GUARDRAIL`

The frozen dual-posterior architecture retained a large structural-recovery advantage under the nonlinear `tanh(parent)` environment, but it failed the preregistered calibration guardrail.

- Screen n=12: mean edge delta -0.6486; 12/12 wins; mean Brier delta +0.00272; zero large harms; exact trace identity.
- Confirmation n=24: mean edge delta -0.3941; paired bootstrap 95% interval [-0.5404,-0.2296]; 21/24 wins; one large harm; exact trace identity.
- Confirmation mean Brier delta +0.01068, exceeding the frozen +0.005 limit.

## Interpretation
Planning/inference separation remains useful under mechanism-form shift: planning actions were unchanged and structural edge recovery improved strongly. However, the linear nonlocal science posterior becomes too poorly calibrated under nonlinear misspecification to promote as broadly robust.

## Required redirect
Do not retune the linear nonlocal prior on these exposed worlds. Test a materially different terminal inference family that models nonlinear parent effects while preserving the baseline planning posterior and identical intervention trace.