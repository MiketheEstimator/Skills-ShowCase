# EXP-002S9 Evaluation

## Disposition
COMPLETE_TRANSFER_SUPPORTED.

The S8 dual-posterior architecture generalized without retuning when nonzero causal-effect magnitudes were shifted from the original 0.4-0.9 range to Uniform(0.15,0.90). The 12-world transfer screen passed, and the independent 24-world confirmation produced mean edge delta -0.4857, paired bootstrap 95% CI [-0.7143,-0.2744], mean Brier delta +0.00058, 21/24 wins, one large-harm world, and exact action-trace identity in all worlds.

This weakens the concern that S8 succeeds only by memorizing the original effect-size gap. The next higher-order uncertainty is mechanism-form shift: whether the structural inference benefit survives when the true parent-child relationship is nonlinear while both planner and structural posterior remain the frozen linear models.