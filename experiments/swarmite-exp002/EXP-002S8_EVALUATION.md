# EXP-002S8 Evaluation

## Disposition
COMPLETE_SUPPORTED.

The dual-posterior architecture passed both preregistered stages. On the 12-world screen it improved edge error in 12/12 worlds with mean delta -0.6558, mean Brier delta -0.00257, zero large harms, and exact control action traces. On the independent 24-world confirmation it improved 22/24 worlds with mean edge delta -0.4705, paired bootstrap 95% CI [-0.6370,-0.3159], mean Brier delta -0.00081, zero large harms, and exact action-trace identity in every world.

## Established mechanism
S7 showed that the S5 nonlocal posterior itself improved inference on all baseline action sequences, while harms emerged only when that posterior influenced intervention planning. S8 prospectively confirmed that separating posterior roles resolves that failure: keep the benchmark posterior for experiment design, while using the nonlocal zero-versus-nonzero effect model for terminal structural inference.

The next uncertainty is generalization. The supported structural posterior is informed by the benchmark generator's nonzero-effect gap, so it must be tested under effect-size distribution shift before being treated as broadly robust.