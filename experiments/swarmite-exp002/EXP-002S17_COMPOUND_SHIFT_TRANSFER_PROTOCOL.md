# EXP-002S17 — Fixed Gate Under Compound Nonlinear + Heavy-Tail Shift

Status: RUNNING after protocol freeze.

## Rationale
S15 supports disagreement-gated dual-posterior inference under nonlinear mechanism shift. Fresh reproducible S16R supports the same frozen D<=1.50 gate under standardized Student-t(df=3) noise shift. The next uncertainty is compositional robustness: whether the same architecture remains reliable when both shifts occur simultaneously rather than one at a time.

## Frozen design
Use benchmark-v2 DAG/coefficient generation, costs, intervention budget, proposal controller, and Gaussian planning model. Generate environment outcomes with `tanh(parent)` structural response and standardized Student-t(df=3) innovations. Terminal science inference remains the frozen S5 nonlocal linear posterior. Planning and science posteriors remain strictly separated. Promotion remains frozen at D = sum(abs(edge_marginals(science)-edge_marginals(planning))) <= 1.50. No retuning.

The executable must be committed before efficacy-world exposure and must freeze exact RNG consumption semantics.

## Fresh worlds
Mechanics: 69101-69104.
Screen: 69111-69122.
Confirmation if screen passes: 69201-69224.

## Mechanics gate
Deterministic replay; exactly 29,281 DAGs; normalized finite posteriors; spend <=15; identical planning traces between control and terminal-science treatment.

## Screen pass
Coverage >=0.50; promoted mean edge delta <= -0.10; promoted mean Brier delta <= +0.005; <=2 promoted harms >0.50; exact trace identity.

## Confirmation promotion
Coverage >=0.50; promoted mean edge delta <= -0.10; paired bootstrap 95% upper bound <0; promoted mean Brier delta <= +0.005; <=3 promoted harms >0.50; exact trace identity.

If compound shift fails while both component shifts pass independently, enqueue a multi-signal model-shift gate rather than retuning D on exposed worlds.