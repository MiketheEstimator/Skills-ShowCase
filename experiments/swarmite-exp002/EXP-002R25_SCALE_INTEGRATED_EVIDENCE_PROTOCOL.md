# EXP-002R25 — Scale-Integrated Family Evidence

## Status
RUNNING after protocol freeze.

## Hypothesis
R22 and R24 show that materially different coefficient-prior covariance choices both induce dense-graph marginal-likelihood distortions. The common mechanism may be the benchmark family evidence model's fixed residual variance. Integrating residual-scale uncertainty with a conjugate Normal-Inverse-Gamma family model may make the Occam factor less sensitive to coefficient-prior volume and improve terminal structural recovery.

## Frozen treatment
Keep benchmark-v2 world generator, uniform DAG prior, width-1 proposal portfolio, intervention-cost budget 15, proposal RNG, real-environment RNG, and three planner predictive simulations per candidate unchanged.

Control is the committed benchmark family model with TAU2=4 and fixed residual variance 1.

Treatment uses, independently for every candidate parent family, the conjugate model:
- beta | sigma^2 ~ Normal(0, sigma^2 * 4 I), including intercept;
- sigma^2 ~ Inverse-Gamma(a0=3, b0=2), whose prior mean is 1;
- posterior family evidence is the exact Normal-Inverse-Gamma marginal likelihood;
- posterior predictive simulation and incremental scoring use the corresponding Student-t predictive, not a Gaussian approximation.

This treatment changes the likelihood/world-model uncertainty mechanism rather than adding another graph-size penalty or coefficient covariance retry.

## Mechanics gate
Seeds 65301-65304 only. Verify finite family scores and normalized posterior over exactly 29,281 DAGs, Student-t predictive variance/scale finite and positive, deterministic replay, intervention spend <=15, and no ground-truth access during action selection. Mechanics worlds are excluded from efficacy analysis.

## Prospective screen
After the mechanics gate is persisted, use fresh seeds 65311-65322. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and no more than 2/12 worlds worsen by >0.50 edge-error units.

If screen passes, confirm on fresh seeds 65401-65424. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and no more than 3/24 large-harm worlds.

## Diagnostic outputs
Persist posterior expected edge count for both arms and true edge count only after each world's terminal policy execution. These are secondary mechanism diagnostics and may not influence action selection.

No R17-R24 efficacy worlds may be reused for prospective efficacy.