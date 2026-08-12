# EXP-002S47 — Reference Breadth Confirmation of Continuous-Risk S30 Architecture

## Motivation
S46 prospectively supported a continuous observable risk layer around the S30 terminal science posterior on the joint topology × heteroskedastic nonlinear family. On 120 held-out worlds it promoted 87.5%, reduced promoted large harms to 0.95%, improved mean hybrid edge delta to -0.818, and outperformed the always-S30/topology-only structural mean by selectively rejecting harmful worlds. Before reference-architecture promotion, the exact frozen S46 model and rule must transfer outside its training family.

## Hypothesis
The frozen S46 continuous-risk model will preserve material S30 benefit and harm control across a balanced mixture of previously distinct world-shift families without refitting coefficients, standardization, or thresholds.

## Frozen artifacts
Load from `EXP-002S46_TRAINING_RESULT.json` without modification:
- feature ordering and standardization,
- ridge edge-delta coefficients,
- logistic large-harm coefficients,
- training harm prevalence,
- selected edge/harm promotion cutoffs.

Planning remains baseline-only and S30 remains terminal-only.

## Six prospective world families
Each evaluation block contains equal counts from:
1. `linear`: benchmark-v2 linear homoskedastic generator.
2. `weak_effect`: linear generator with nonzero effects Uniform(0.15,0.90), as in S9.
3. `compound_t`: tanh mechanisms with variance-normalized Student-t(df=3) noise, as in S17.
4. `heteroskedastic`: mixed tanh/sin/asinh mechanisms with S40 heteroskedastic noise.
5. `topology`: sparse/dense graph-density shift with otherwise benchmark-v2 linear observations, as in S41.
6. `joint`: sparse/dense topology plus heteroskedastic tanh/sin/asinh mechanisms, as in S44.

The exact S46 observable feature extractor is applied to all regimes, including its fixed mechanism predictive scores. Regime labels and ground truth are evaluation-only and never enter the S46 risk model.

## Prospective seeds
Regime is assigned deterministically by seed modulo six, with complete six-regime blocks:
- Mechanics: 74301–74306 (one per regime).
- Screen: 74311–74358 (48 worlds; 8 per regime).
- Held-out confirmation: 74401–74520 (120 worlds; 20 per regime), unavailable unless screen passes.

All seeds are fresh.

## Matched controls
Report on identical worlds:
1. baseline,
2. always-S30,
3. frozen S39 scalar credal gate.

The S43 topology-only utility rule is reported diagnostically but is not a universal matched control because several S47 regimes do not belong to its sparse/dense training ontology.

## Mechanics invariants
- budget <=15,
- planning trajectory generated only by baseline posterior,
- S30 normalized and finite,
- all 19 frozen S46 features finite and in the same order,
- S46 predictions finite,
- all six regimes represented in mechanics.

## Screen success
Overall frozen S46 hybrid must satisfy:
- coverage >= 0.50,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta < 0,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.55,
- risk-prediction Brier <= constant S46-training-prevalence predictor Brier.

Additionally each regime must have:
- coverage >= 0.25,
- hybrid mean edge delta <= +0.10,
- promoted large-harm rate <= 0.125 at screen (one harm permitted in an 8-world regime cell).

## Confirmation promotion
Require all overall screen criteria with improvement retention >= 0.60, plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0,
- each regime coverage >= 0.30,
- each regime hybrid mean edge delta <= 0,
- each regime promoted large-harm rate <= 0.10,
- overall promoted large-harm rate <= 0.05.

## Interpretation
Success promotes the architecture `baseline planning posterior -> S30 terminal science posterior -> continuous observable risk adjudicator -> baseline fallback` to the current Swarmite reference terminal architecture. Failure localizes the unsupported regime and redirects to regime-specific robustness or broader ensemble uncertainty; it does not justify refitting on held-out worlds.
