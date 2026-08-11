# EXP-002S52 — Latent Residual-State Adjudication Model

## Motivation
EXP-002S51 prospectively classified the remaining heteroskedastic breadth failure as `ADJUDICATION_DOMINANT`: on 48 fresh heteroskedastic worlds the frozen S49 specialist had mean oracle two-posterior headroom 0.133 with bootstrap 95% interval [0.044, 0.248], while the scalar S50 `q_het` evidence had specialist-win AUC 0.378. The specialist can occasionally improve S30, but the existing scalar fitted-magnitude variance score cannot tell when.

## Hypothesis
A richer **cross-fitted latent residual-state representation** can discriminate worlds in which the frozen heteroskedastic specialist beats the frozen S30 anchor without changing planning, intervention trajectories, the S30 posterior, the specialist posterior, or the S46 outer promotion rule.

## Material distinction
S52 does **not** retune S48 promotion thresholds, S49 fixed blends, S50 mixture caps/temperatures, or S50 scalar variance evidence. It changes the observable state representation used for terminal adjudication.

The candidate is hierarchical:
1. frozen baseline-only planner, budget 15;
2. frozen S46 outer promote/defer decision;
3. if S46 defers, output baseline posterior exactly;
4. if S46 promotes, choose between frozen S30 and frozen P_HET using an S52 adjudicator trained only on fresh training worlds.

Thus specialist use cannot alter experiment selection and cannot bypass S46.

## Observable residual-state representation
Using five-fold cross-fitting and no ground-truth graph labels, fit the same nodewise linear mean models used by S50. On held-out residuals derive per-node residual-process summaries, then aggregate across nodes:
- log residual variance;
- rank/linear association of `|residual|` with `log1p(|prediction|)`;
- slope of `log(residual^2 + eps)` on `log1p(|prediction|)`;
- high-vs-low fitted-magnitude residual variance ratio;
- standardized tail fraction;
- standardized absolute-residual mean;
- residual variance dispersion across fitted-magnitude bins.

Persist mean, standard deviation, and maximum/robust-maximum summaries where defined, plus S50 `d_var`, `q_het` and the frozen S46 19-dimensional observable feature vector. No true regime, DAG, edge error, or specialist-win label enters the feature vector.

## Learned adjudicator
On fresh training worlds only:
- ridge regression predicts realized `specialist_gain = edge_error(S30) - edge_error(P_HET)`;
- ridge logistic regression predicts `P(P_HET beats S30)`;
- standardization parameters and coefficients are frozen after training.

Training searches only the preregistered decision grid:
- win-probability cut in {0.55, 0.65, 0.75, 0.85};
- predicted-gain cut in {0.00, 0.05, 0.10}.

Inside S46-promoted worlds, use P_HET iff both cuts pass; otherwise use S30.

## Prospective worlds
All worlds are fresh and disjoint from S48–S51.
- Mechanics: 4 worlds, 2 linear + 2 heteroskedastic, selected from external-seed search starting 79001.
- Training: 128 worlds, 64 + 64, starting 79101.
- Validation: 64 worlds, 32 + 32, starting 79601.
- Held-out confirmation: 128 worlds, 64 + 64, starting 79901.

Ground truth is exposed only after each trajectory is complete to compute training labels or evaluation metrics.

## Controls
Primary control is frozen S46 + S30 on the exact same worlds and trajectories. Also persist always-S30 and diagnostic P_HET outcomes. Resource budget and planning are identical.

## Metrics
Overall and by regime report:
- S46 coverage;
- specialist-use rate among promoted worlds;
- candidate and control hybrid mean edge delta vs baseline;
- paired candidate-minus-control edge difference;
- bootstrap 95% interval for paired edge difference;
- candidate and control Brier delta;
- promoted large-harm count/rate;
- specialist-selection precision (`P_HET actually beats S30` among selected);
- specialist-win AUC and Brier score for the learned probability model.

## Frozen training qualification
A rule qualifies only if:
- mechanics pass;
- S46 coverage is unchanged;
- specialist-use rate among promoted is between 0.03 and 0.35;
- candidate overall hybrid mean edge delta <= control + 0.01;
- heteroskedastic candidate hybrid mean edge delta <= control - 0.02;
- linear candidate hybrid mean edge delta <= control + 0.02;
- candidate promoted large harms <= control promoted large harms;
- candidate hybrid mean Brier delta <= 0.005;
- specialist-selection precision >= 0.55.

Among qualifying rules choose the most negative heteroskedastic paired edge difference; ties within 0.01 choose the stricter win-probability cut, then stricter gain cut.

## Validation gate
With the frozen model/rule, require all training qualification conditions except specialist-use lower bound may fall to 0.02, plus:
- overall paired mean candidate-minus-control edge difference <= 0;
- learned specialist-win AUC >= 0.60.

Failure ends S52 at validation; held-out confirmation remains unopened.

## Confirmation support
Require validation gate plus:
- bootstrap 95% upper bound for overall paired candidate-minus-control edge difference < 0;
- heteroskedastic paired mean candidate-minus-control edge difference < -0.02;
- linear paired mean difference <= 0.02;
- no increase in promoted large-harm count vs S46/S30;
- learned specialist-win AUC >= 0.60 and probability Brier <= constant-prevalence Brier.

## Successor rule
- If supported: enqueue S53 as breadth/generalization transfer of the frozen S52 adjudicator across weak-effect, compound nonlinear/heavy-tail, topology, joint, and heteroskedastic regimes without retuning.
- If training or validation shows AUC < 0.60 despite S51 oracle headroom: enqueue S53 to change the residual-state representation itself to a nodewise latent mixture/variance-process embedding; do not retry S52 cutoffs.
- If discrimination is adequate but selected P_HET still harms calibration or edge quality: enqueue S53 to replace hard posterior selection with a calibrated terminal model-average whose weight is learned from the same residual state under a new preregistered objective.
- Execution failures are blocked and repaired without exposing later splits.
