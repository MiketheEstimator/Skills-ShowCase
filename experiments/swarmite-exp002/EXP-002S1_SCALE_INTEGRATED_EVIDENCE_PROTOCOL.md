# EXP-002S1 — Scale-Integrated Family Evidence

## Status
RUNNING after namespace recovery and protocol freeze.

## Recovery rationale
The scientific question originated in R25 after R24, but repository audit found pre-existing unrelated R25/R26 executable/result namespaces. Those artifacts are not pooled or overwritten. S1 restarts the scale-integrated likelihood experiment under a clean namespace with fresh seeds.

## Hypothesis
The dense-graph distortions seen in R21-R24 may arise from fixed residual variance in the family evidence model. Integrating residual-scale uncertainty with exact conjugate Normal-Inverse-Gamma evidence and Student-t posterior predictive scoring may improve terminal structural recovery.

## Frozen treatment
Keep benchmark-v2, uniform DAG prior, width-1 proposal portfolio, intervention budget 15, proposal RNG, real-environment RNG, and three predictive planner simulations per candidate unchanged. Control is the committed TAU2=4 fixed-noise benchmark.

Treatment uses beta | sigma^2 ~ Normal(0, sigma^2 * 4 I), including intercept, and sigma^2 ~ Inverse-Gamma(a0=3,b0=2), prior mean 1. Use exact NIG marginal likelihood and exact Student-t posterior predictive simulation/scoring.

Executable lineage is `experiments/swarmite-exp002/swarmite_exp002_scale_integrated_nig_v1.py` at commit `183b066d08a79683ecfe216cff8ec577a30cdcc2`.

## Mechanics gate
Fresh mechanics-only seeds 65801-65804. Verify finite family evidence and predictive scales, normalized posterior over exactly 29,281 DAGs, deterministic replay, spend <=15, and no ground-truth access during action selection. Persist mechanics gate before efficacy exposure.

## Prospective screen
Fresh seeds 65811-65822. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If screen passes, confirm on 65901-65924 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

No R17-R26 efficacy worlds are reusable for S1 efficacy.