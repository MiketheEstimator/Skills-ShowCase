# EXP-002R20 — Distributionally Robust EIG Across Prior Classes

## Hypothesis
R17-R19 show that replacing the inference prior is unstable. Prior-class uncertainty may still be useful for experiment selection if it is treated as decision uncertainty rather than as a forced terminal posterior. A maximin EIG controller can prefer interventions informative under both uniform and hierarchical sparsity beliefs while retaining the uniform posterior for final inference.

## Frozen treatment
Benchmark-v2, width-1 proposal portfolio, budget 15. Control uses the committed uniform posterior and ordinary EIG. Treatment maintains two posteriors over the same likelihood: uniform-prior and R18 hierarchical Beta-Binomial prior. Candidate proposals are generated from the uniform posterior in both arms. For each candidate, treatment computes EIG-per-cost independently under both posteriors and selects the candidate maximizing the minimum of the two scores. The real observation updates both posteriors, but terminal metrics are computed from the uniform posterior only. Intervention budgets and candidate sets are matched; additional planner compute is tracked separately.

## Screen
Fresh paired seeds 64701-64712. Pass if mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on 64801-64824 requiring mean edge delta <= -0.10, bootstrap 95% upper bound <0, Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.