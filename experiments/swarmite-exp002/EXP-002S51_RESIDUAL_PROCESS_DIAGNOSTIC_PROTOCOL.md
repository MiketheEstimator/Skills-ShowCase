# EXP-002S51 — Residual-Process Representation Diagnostic

## Motivation
EXP-002S50 falsified bounded evidence-weighted averaging of the frozen S30 anchor and the S49 heteroskedastic specialist. The specialist had heteroskedastic upside but could not be safely allocated without damaging the linear anchor. Before introducing a new latent residual-process representation, S51 prospectively determines whether the remaining failure is primarily (a) terminal posterior point-estimate insufficiency, (b) adjudication/discrimination insufficiency, or (c) mixed.

## Hypothesis
The heteroskedastic breadth failure is expected to show measurable oracle specialist headroom while the existing observable variance evidence fails to discriminate when that specialist should be trusted. If so, the next mechanism should change the observable residual-process representation used for model adjudication rather than merely retune mixture weights or promotion thresholds.

## Material distinction
- Diagnostic only: no new posterior is promoted and no threshold is fitted.
- Not S48: no promotion repair.
- Not S49: no fixed specialist blend.
- Not S50: no evidence-weighted posterior mixture.
- Planning remains baseline-only and budget 15.
- Ground truth is used only after each world is complete for diagnostic attribution.

## Frozen components
- Baseline planner and baseline terminal posterior from benchmark v2.
- S30 terminal posterior as the robust science anchor.
- S49 heteroskedastic terminal posterior as the diagnostic specialist.
- S46 promotion model/rule, unchanged.
- S50 cross-fitted variance evidence `d_var` / `q_het`, unchanged.

## Prospective worlds
- Mechanics: 4 fresh worlds, 2 linear + 2 heteroskedastic, starting at external-seed search 78101.
- Diagnostic panel: 96 fresh worlds, 48 linear + 48 heteroskedastic, starting at external-seed search 78201.
- No training/validation/confirmation split is needed because S51 learns no deployable parameter and promotes no candidate.

## Per-world quantities
After the fixed trajectory, persist:
1. baseline, S30, and P_HET edge error and Brier score;
2. S30 and P_HET deltas versus baseline;
3. specialist gain over S30 = `edge_error(S30) - edge_error(P_HET)`;
4. oracle two-posterior gain = `edge_error(S30) - min(edge_error(S30), edge_error(P_HET))`;
5. observable S50 `d_var` and `q_het`;
6. frozen S46 predicted edge delta, predicted harm probability, and promote decision;
7. evaluation-only labels: specialist beats S30, S30 large harm (>0.50 versus baseline), and regime.

## Primary diagnostic metrics
Report overall and by regime:
- mean S30 delta and P_HET delta versus baseline;
- specialist win rate and mean specialist gain over S30;
- mean oracle two-posterior headroom;
- S30 large-harm rate and frozen-S46 promoted large-harm rate;
- AUC of `q_het` for the evaluation-only label `P_HET edge error < S30 edge error` when both classes occur;
- Spearman-like rank correlation (Pearson correlation of ranks) between `q_het` and realized specialist gain.

Bootstrap a 95% interval for mean heteroskedastic oracle headroom.

## Frozen interpretation
Classify the bottleneck without tuning:
- `ADJUDICATION_DOMINANT` if heteroskedastic mean oracle headroom >= 0.10, its bootstrap 95% lower bound > 0, and q_het specialist-win AUC < 0.65.
- `POINT_ESTIMATE_DOMINANT` if heteroskedastic mean oracle headroom < 0.05 or its bootstrap 95% upper bound <= 0.05.
- `MIXED` otherwise.

This classification is diagnostic, not a claim of deployable superiority.

## Success / completion
S51 completes when mechanics pass and the 96-world diagnostic panel is persisted with the frozen classification. Scientific falsification is valid: any of the three classifications is informative.

## Successor rule
- If `ADJUDICATION_DOMINANT`: enqueue S52 to replace scalar fitted-magnitude variance evidence with a materially richer latent residual-state representation (for example nodewise residual-state features / mixture variance process) while keeping S30 as anchor.
- If `POINT_ESTIMATE_DOMINANT`: enqueue S52 to build a latent residual-process terminal likelihood that changes the specialist posterior itself, not the gate.
- If `MIXED`: enqueue S52 as a joint residual-process model whose latent state supplies both specialist likelihood and adjudication evidence, with S30 retained as mandatory anchor/control.

Do not retry S48–S50 thresholds, caps, temperatures, or fixed blends.