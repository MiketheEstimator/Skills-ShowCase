# EXP-002R23 Evaluation

## Disposition
COMPLETE_FALSIFIED_AT_SCREEN.

## Mechanics gate
Seeds 65101-65104 passed the frozen mechanics gate: finite family scores/posteriors, exact 29,281-DAG support, spend <=15, deterministic replay, and no ground-truth access in action selection.

## Prospective screen
Fresh seeds 65111-65122 were evaluated only after the mechanics gate was durably persisted.

Treatment-minus-control results: mean terminal edge-error delta = +0.7919865933; mean Brier delta = +0.0104616190; wins/losses = 1/11; 10/12 worlds worsened by >0.50 edge-error units; net MAP delta = +1. The preregistered pass criteria were therefore decisively missed.

## Scientific interpretation
The design-adaptive g-prior does not repair the R21 coefficient-prior pathology. Despite replacing isotropic shrinkage with design-scaled covariance, it substantially worsens terminal structural recovery. Confirmation is not justified.

The next experiment is a mechanism diagnostic, not an efficacy retry: measure whether the g-prior again shifts posterior graph density and whether that shift increases terminal edge-count bias. Reusing R23 screen worlds for this explanatory diagnostic is permitted because no new efficacy claim is made from them.