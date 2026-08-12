# EXP-002S39 — Credal Science Posterior from Specialist Disagreement

## Status
PENDING -> RUNNING when executable workflow checkpoints the frozen protocol.

## Motivation
EXP-002S37 established S30 as the only globally safe point-posterior anchor, while EXP-002S38 found substantial oracle residual value distributed heterogeneously across specialist posteriors and no specialist that was independently safe. This experiment therefore does **not** move the S30 point posterior toward any specialist. It tests whether disagreement among specialists can be used as an uncertainty signal for selective abstention/fallback.

## Hypothesis
Observable structural disagreement between S30 and the six specialist posteriors identifies worlds in which publishing S30 is comparatively risky. A frozen disagreement gate can reduce S30 large harms and improve risk-adjusted terminal structural quality while retaining useful coverage, without changing intervention traces or the S30 posterior on promoted worlds.

## Frozen design
For every world, execute the committed S35 component stack and preserve the S30 point posterior. Compute edge marginals for S30 and specialists TG, TT, SG, ST, AG, AT. No ground truth enters any disagreement score.

Candidate observable disagreement scores:
1. `mean_credal_width`: mean across directed edges of `max(marginal)-min(marginal)` over {S30,TG,TT,SG,ST,AG,AT}.
2. `max_credal_width`: maximum edge credal width.
3. `mean_l1_from_s30`: mean absolute specialist-vs-S30 edge-marginal deviation, averaged across specialists and edges.

Training worlds: seeds 72301–72348 (48; balanced over the six committed S32 cells).
Validation worlds: seeds 72361–72396 (36; held out from gate fitting).
Confirmation worlds: seeds 72401–72448 (48; exposed only after validation passes).

For each score, candidate thresholds are the empirical training quantiles {0.50,0.60,0.70,0.80,0.90}. A world is promoted when `score <= threshold`; otherwise the system abstains from the S30 science posterior and falls back to the committed baseline posterior. Ground truth is used only after scores are frozen to evaluate terminal quality.

## Training selection
For each score/threshold pair compute:
- coverage,
- hybrid mean edge delta versus baseline, where promoted worlds use S30 and abstained worlds use baseline (delta 0),
- hybrid mean Brier delta versus baseline,
- S30 large harms among promoted worlds (`edge_delta_vs_baseline > 0.50`),
- fraction of always-S30 improvement retained, defined when always-S30 mean edge delta is negative as `abs(hybrid_mean_edge_delta)/abs(always_s30_mean_edge_delta)`.

Eligible gates must satisfy all of:
- coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial on average, improvement retained >= 0.70.

Among eligible gates select the one with the lowest promoted large-harm count, then lowest hybrid mean edge delta, then highest coverage. Remaining ties prefer `mean_credal_width`, then the lower threshold. If no gate is eligible, S39 is falsified at training and no validation worlds are run.

## Validation gate
Freeze the selected score and numerical threshold before validation. Validation passes only if:
- coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean Brier delta <= +0.005,
- improvement retained >= 0.70 when always-S30 is beneficial,
- hybrid mean edge delta is <= 0 (non-harmful versus baseline).

If validation fails, mark scientific falsification and do not expose confirmation worlds.

## Confirmation promotion
If validation passes, run the frozen gate on confirmation worlds. Promotion requires:
- coverage >= 0.60,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta < 0,
- paired bootstrap 95% upper bound for hybrid edge delta versus baseline < 0,
- hybrid mean Brier delta <= +0.005,
- improvement retained >= 0.70,
- mechanics invariants hold on every world.

## Mechanics invariants
- S30 remains the point posterior on promoted worlds.
- Abstention uses the committed baseline posterior; no specialist posterior is substituted.
- Intervention traces, budget, world generation, and RNG namespaces are unchanged from the committed lineage.
- All posterior masses are finite and normalized.
- Training, validation, and confirmation are strictly separated.
- Negative results are preserved.

## Success interpretation
Success supports a **credal uncertainty layer around S30**, not specialist model selection and not specialist posterior averaging. Falsification redirects toward uncertainty representations that model world-class uncertainty explicitly rather than another threshold on the same disagreement geometry.