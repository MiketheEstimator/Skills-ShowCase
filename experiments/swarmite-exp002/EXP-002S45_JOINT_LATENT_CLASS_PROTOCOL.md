# EXP-002S45 — Joint Topology–Mechanism/Noise Latent-Class Decision

## Motivation
S44 strongly improved aggregate structural recovery under combined topology plus heteroskedastic nonlinear shift, but prospectively failed its cell-level harm guardrail: dense-asinh and dense-sin each showed a 12.5% large-harm rate. The frozen S43 decision used topology class alone and promoted every S44 world, so the failure localizes the remaining uncertainty to mechanism/noise subtype rather than topology-only uncertainty.

## Hypothesis
An explicit observable posterior over the six joint world classes `{sparse,dense} × {tanh,sin,asinh}` can propagate class-specific S30 utility and large-harm risk well enough to preserve most of S30's structural benefit while suppressing the risky dense mechanism/noise cells.

## Frozen S30 anchor and planner
Planning remains the benchmark-v2 baseline posterior with intervention budget 15. S30 remains terminal-only and is constructed exactly as in the committed S30/S43/S44 lineage. No S45 mechanism may alter planning actions.

## Observable joint-class posterior
### Topology component
Use the exact S42 observable posterior `q_density = P(dense | data)` from sparse-vs-dense graph-family evidence. This component is unchanged.

### Mechanism/noise component
For each candidate mechanism `m ∈ {tanh, sin, asinh}`, compute a deterministic 3-fold out-of-sample predictive log score from the accumulated observational/interventional data:
1. For each node, exclude rows where that node was intervened upon.
2. Use all other nodes transformed by candidate `m` as predictors plus an intercept.
3. Fit ridge regression (`lambda = 0.25`) on two folds.
4. On the held-out fold compute Gaussian predictive log likelihood with the known S40 heteroskedastic family `sigma = clip(0.55 + 0.35*abs(mu), 0.55, 1.80)`.
5. Sum scores across nodes/folds and normalize by the number of held-out node-observations.

Convert the three scores to a mechanism posterior by softmax with temperature `T_mech` selected **only on S45 training worlds** from `{0.05, 0.10, 0.20, 0.50, 1.00}` to minimize multiclass negative log likelihood of the known training mechanism labels. Ties select the larger temperature (more conservative posterior).

The deployment joint posterior is the normalized outer product of `q_density` and `q_mechanism`; no joint-cell truth is used at deployment.

## Utility model
Training worlds estimate, separately for all six true joint cells:
- mean S30 edge delta vs baseline,
- S30 large-harm rate (`edge delta > +0.50`).

For a deployment world:
`expected_delta = Σ_c q(c|data) * mu_c`
`expected_harm = Σ_c q(c|data) * harm_c`

Promote S30 iff `expected_delta < 0` and `expected_harm <= 0.05`; otherwise fall back to baseline. There is no deployment threshold search.

## Matched controls
Evaluate on identical worlds:
1. baseline posterior,
2. always-S30,
3. frozen S43 topology-only decision using the S43 class utilities,
4. frozen S39 scalar credal gate.

## Prospective splits
All seeds are fresh and excluded from S44.
- Training: 73501–73572 (72 worlds; 12 per joint cell).
- Validation: 73601–73636 (36 worlds; 6 per joint cell).
- Held-out confirmation: 73701–73772 (72 worlds; 12 per joint cell), exposed only if validation passes.

Persist the full training mechanism-score table, selected `T_mech`, six cell utilities, and harm estimates before any validation world is evaluated. Persist validation disposition before confirmation exposure.

## Validation success criteria
Joint-class hybrid must satisfy all:
- mechanics invariants hold,
- all six training and validation cells represented at planned counts,
- mechanism posterior finite and normalized,
- coverage >= 0.50,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta vs baseline < 0,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.65,
- joint-class hybrid mean edge delta no worse than topology-only S43 control by > +0.02,
- mechanism classifier multiclass NLL on validation is better than or equal to the uniform posterior NLL `log(3)`.

## Confirmation promotion
Require all validation criteria plus:
- paired bootstrap 95% upper bound for joint-class hybrid edge delta < 0,
- no joint cell with promoted large-harm rate > 0.10,
- at least 0.60 improvement retention,
- confirmation mechanism NLL <= `log(3)`.

## Interpretation
Success supports a role-separated terminal architecture with explicit world-class uncertainty over both topology and mechanism/noise. Failure means this hand-specified six-class ontology is insufficient and redirects to learned continuous risk prediction or broader model-class ensembles, not scalar abstention or retuning S43/S44 thresholds.
