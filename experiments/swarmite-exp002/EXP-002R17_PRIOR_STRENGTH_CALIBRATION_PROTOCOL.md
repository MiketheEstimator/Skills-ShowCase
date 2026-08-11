# EXP-002R17 — Sparsity-Prior Strength Calibration

## Status
RUNNING after protocol freeze.

## Hypothesis
The R16 failure pattern is caused by an overstrong sparsity prior rather than by sparsity regularization itself. A weaker fixed prior penalty can improve terminal scientific quality without the catastrophic over-shrinkage observed at full strength.

## Frozen design
Use the benchmark-v2 engine and width-1 portfolio controller. Replace the uniform DAG prior with a tempered generator-informed log prior: `lambda * [k log(0.35) + (10-k) log(0.65)]`, where k is DAG edge count and lambda is selected only from {0.00, 0.25, 0.50, 0.75, 1.00}.

Training worlds: seeds 64001-64024. For each lambda, run matched paired worlds and select the lambda minimizing mean terminal edge error, subject to mean Brier delta versus lambda=0 not exceeding +0.005. Ties within 0.01 edge-error units select the smaller lambda.

Validation worlds: seeds 64101-64112. Freeze the selected lambda before validation. Advance to held-out testing only if validation mean edge-error delta <= -0.10, validation mean Brier delta <= +0.005, and no more than 2/12 validation worlds worsen by >0.50 edge-error units.

Held-out worlds, if validation passes: seeds 64201-64224. Promotion requires held-out mean edge-error delta <= -0.10, paired bootstrap 95% upper bound < 0, mean Brier delta <= +0.005, and no more than 3/24 worlds worsening by >0.50.

## Scientific controls
Lambda=0 is the committed uniform-prior baseline. All policies use identical intervention budgets, candidate generation, EIG simulation counts, and RNG namespaces. Ground-truth DAGs are used only for terminal evaluation, never for lambda selection inside a world. R16 seeds 63001-63012 are excluded from all R17 stages.

## Checkpoint discipline
Persist the full training grid and selected lambda before any validation seed is executed. Persist validation disposition before any held-out seed is executed.