# EXP-002S16 — Fixed S15 Gate Under Noise-Distribution Shift

Status: RUNNING after protocol freeze.

Hypothesis: the supported S15 disagreement-gated dual-posterior architecture transfers without retuning to a different model shift.

Worlds: use benchmark-v2 linear DAG mechanisms and coefficient generator. Replace Gaussian structural noise with standardized Student-t(df=3) noise scaled to unit variance. Keep interventions, observation count, costs, budget, DAG generator, and coefficients unchanged.

Architecture: planning remains the original benchmark-v2 Gaussian planner. Terminal science inference remains the frozen S10/S5 nonlocal posterior. Use the frozen S15 gate D <= 1.50 for structural promotion; otherwise abstain as model-shift-sensitive. No retuning.

Mechanics: seeds 68701-68704. Require deterministic replay, 29,281 DAGs, normalized finite posteriors, spend <=15, and identical traces.

Screen: seeds 68711-68722. Pass if coverage >=0.50, promoted mean edge delta <= -0.10, promoted mean Brier delta <= +0.005, <=2 promoted large harms, and trace identity.

Confirmation if screen passes: seeds 68801-68824. Require coverage >=0.50, promoted mean edge delta <= -0.10, bootstrap 95% upper bound <0, promoted mean Brier delta <= +0.005, <=3 promoted large harms, and trace identity.

If falsified, redirect toward a generalized model-shift detector using multiple posterior-disagreement signals rather than retuning the 1.50 threshold on exposed worlds.