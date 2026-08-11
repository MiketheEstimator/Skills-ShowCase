# EXP-002S44 — Joint Class-Aware Decision Transfer under Topology + Heteroskedastic Shift

## Motivation
S43 prospectively supported explicit topology-class uncertainty around the S30 science-posterior anchor and outperformed the older scalar credal gate. S40 separately supported transfer under heteroskedastic nonlinear mechanisms. The unresolved question is whether the frozen S43 decision remains safe when both sources of shift occur simultaneously rather than one at a time.

## Hypothesis
The frozen S43 class-aware publish-vs-fallback rule will preserve a material fraction of S30 structural benefit under a joint graph-density and heteroskedastic nonlinear mechanism shift, without violating calibration or large-harm guardrails.

## Frozen decision rule
No parameter is fit or retuned in S44.

Use the exact S42 observable topology posterior `q = P(dense | data)` and the exact S43 training estimates:
- `mu_sparse = -0.17642413429903825`
- `mu_dense = -0.04040343473196801`
- `harm_sparse = 0.0`
- `harm_dense = 0.0`

For each world:
`expected_delta = (1-q)*mu_sparse + q*mu_dense`
`expected_harm = (1-q)*harm_sparse + q*harm_dense`

Promote S30 iff `expected_delta < 0` and `expected_harm <= 0.05`; otherwise publish the baseline posterior. S30 itself is unchanged.

## Joint shift family
World topology alternates across six balanced cells:
- sparse DAG generator probability 0.15,
- dense DAG generator probability 0.55.

Within each topology class, mechanism cycles across `tanh`, `sin`, and `asinh` parent transforms. Observation noise is heteroskedastic with `sigma = clip(0.55 + 0.35*abs(mu), 0.55, 1.80)`, exactly matching the previously supported S40 shift mechanism.

Thus each six-world block contains all 2 × 3 topology/mechanism cells. No S44 seed has appeared in prior experiments.

## Matched controls
1. Baseline posterior under the same intervention trajectory and joint-shift observations.
2. Always-S30 on the same worlds, to measure available structural benefit.
3. Frozen S39 scalar credal gate (`mean_credal_width <= 0.2692013432171404`) on the same worlds.

Intervention budget remains 15. Planning uses the baseline posterior only; S30 and all uncertainty layers are terminal-only. Planning traces therefore must remain identical by construction.

## Prospective stages
- Mechanics: seeds 73301–73306, one complete balanced 2 × 3 block.
- Screen: seeds 73311–73334, 24 worlds, four complete blocks.
- Held-out confirmation: seeds 73401–73448, 48 worlds, eight complete blocks; unavailable until screen passes.

## Mechanics invariants
All worlds must have:
- spend <= 15,
- finite normalized S30 posterior,
- `0 <= q <= 1`,
- identical planning/control trajectory construction,
- valid topology and mechanism labels,
- all six joint cells represented in the mechanics gate.

## Screen success criteria
The frozen class-aware hybrid must satisfy all:
- mechanics invariants hold,
- coverage >= 0.60,
- promoted large-harm rate (`edge delta > +0.50`) <= 0.05,
- hybrid mean edge delta vs baseline < 0,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.70,
- hybrid mean edge delta no worse than frozen S39 by more than +0.02.

## Confirmation promotion
Require every screen criterion on confirmation plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0,
- no joint topology/mechanism cell with mean hybrid edge delta > +0.10,
- no joint topology/mechanism cell with large-harm rate > 0.10.

## Interpretation
Success supports S43's explicit class-aware uncertainty decision as a transferable terminal architecture under compound topology/noise/mechanism shift and makes it eligible for reference-architecture promotion. Failure falsifies topology-only utility propagation under compound shift and redirects to a joint latent class over topology × mechanism/noise, not another scalar threshold or retuning of S43.
