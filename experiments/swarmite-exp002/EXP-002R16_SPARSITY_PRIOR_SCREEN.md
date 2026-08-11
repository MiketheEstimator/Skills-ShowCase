# EXP-002R16 — Generator-Informed Sparsity Prior Screen

## Status
COMPLETE_EXPLORATORY_HETEROGENEOUS

After terminal-rescoring mechanisms failed to promote, this screen moved to inference correctness rather than search. The benchmark generator uses sparse forward-edge inclusion (p=0.35), while benchmark-v2 inference uses a uniform prior over all 29,281 DAGs. R16 compared the frozen width-1 controller under the uniform prior versus an approximate sparsity prior proportional to `0.35^k * 0.65^(10-k)` for a DAG with k edges.

Seeds 63001-63012 were fresh. Environment, proposal, and planner RNG namespaces were matched. No per-world truth entered the prior.

## Result
Sparse-minus-uniform terminal edge error mean: +0.0664; median: -0.1649; wins/losses: 8/12 vs 4/12; bootstrap 95% CI [-0.363,+0.678]. Mean Brier delta: +0.01063. One catastrophic world (63012) had edge delta +2.877; excluding it only as a diagnostic, not as an inferential result, the other 11 worlds averaged -0.189 edge error.

## Interpretation
A full-strength sparsity prior is not safe to promote: mean edge error and calibration worsened. However, the 8/12 directional wins plus a single dominating failure indicate prior strength, not the general idea of regularizing DAG density, is the unresolved variable. This screen is hypothesis-generating only because the exact prior-strength protocol was not committed before execution.

## Successor
EXP-002R17 preregisters prior-strength calibration with explicit train/validation/held-out separation. The catastrophic R16 world is never reused for tuning or evaluation.