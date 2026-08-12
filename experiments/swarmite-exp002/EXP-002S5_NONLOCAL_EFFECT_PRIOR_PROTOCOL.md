# EXP-002S5 — Nonlocal Included-Effect Prior Evidence

## Status
RUNNING after protocol freeze.

## Hypothesis
The benchmark Gaussian slab assigns substantial prior density to included-edge coefficients near zero, allowing dense DAGs to explain data with effectively absent edges at low structural cost. The world generator instead has a real effect-size gap: absent edges are exactly zero and present edges have magnitude 0.4-0.9. A nonlocal included-edge prior that places mass away from zero may improve causal edge discrimination without another graph-level sparsity penalty.

## Frozen design
Keep benchmark-v2 world generator, uniform DAG prior, width-1 proposal portfolio, intervention budget 15, proposal RNG, real-environment RNG, candidate count, known residual variance 1, and intercept prior variance 4 unchanged. Control remains committed benchmark-v2 inference.

Treatment changes only family model-selection evidence. For every included parent coefficient, use an equal two-component Gaussian slab: 0.5*N(-0.65,0.15^2)+0.5*N(+0.65,0.15^2). The intercept retains N(0,4). For a family with k parents, integrate exactly over all 2^k sign configurations and combine configuration marginal likelihoods by log-sum-exp with equal mixture weights. Empty-parent families are unchanged except for the intercept prior. This uses no ground truth from the realized world; hyperparameters are frozen from the benchmark generator class already committed in v2.

For posterior-predictive EIG simulation, retain the benchmark full-data Gaussian family posterior. Only DAG family evidence changes, isolating the structural-discrimination effect.

## Mechanics gate
Fresh seeds 66401-66404. Verify exact 29,281-DAG support, finite normalized posteriors, deterministic replay, spend <=15, exact enumeration of 2^k sign configurations for each family, and no ground-truth access in scoring. Persist runner and gate before efficacy exposure.

## Prospective screen
Fresh seeds 66411-66422. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If passed, confirm on fresh seeds 66501-66524. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

## Scientific distinction
This is not another graph sparsity prior, global coefficient shrinkage prior, residual-scale model, or predictive-score retry. It tests a nonlocal spike-versus-slab structural mechanism implied by the generator's zero-versus-nonzero effect gap.