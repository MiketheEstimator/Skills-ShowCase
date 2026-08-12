# EXP-002S65 — Decision-Theoretic Local Structural Action Diagnostic

## Status
Prospective protocol frozen before mechanics/training inspection.

## Scientific basis
EXP-002S64 retained strong prospective S62 localization/proposal evidence (AUC 0.7108; proposal usefulness 0.5686) but falsified constrained posterior-projection geometry at training (paired edge difference +0.02564, no excess large harms). S63 and S64 therefore jointly argue against another posterior reweighting/projection repair. S65 changes the action layer while leaving the posterior itself untouched.

## Hypothesis
S62's evidence may be useful for structural decisions even when it is not suitable for modifying the full DAG posterior. A Bayes action that combines the frozen S30 local parent-family belief with S62's intervention-state refit belief according to prospectively learned anchor-error probability, then chooses the globally valid DAG minimizing expected local edge loss, can reduce structural decision error without degrading posterior calibration because no posterior probabilities are changed.

## Frozen components
- benchmark/data generator, DAG universe, baseline planner, budget 15, S30 anchor, and S46 outer promotion remain unchanged;
- S62 leave-one-state-out local posterior construction and eight evidence features remain unchanged;
- S64's ridge-regularized anchor-error model form remains unchanged;
- no S56-S58 residual likelihood, no S49 specialist, no S63 exponential tilt, and no S64 IPF projection is used;
- validation/confirmation are never used for fitting or parameter choice.

## New action mechanism
For each target node v:
1. Compute S30's induced local parent-family marginal `m30_v(pm)`.
2. Compute S62's mean leave-one-state-out local parent-family distribution `q62_v(pm)`.
3. Predict `p_error_v` with the frozen-form S62 feature model trained only on the fresh training panel.
4. Form a decision belief, not a posterior: `d_v = (1-p_error_v) * m30_v + p_error_v * q62_v`.
5. For every legal parent mask `a`, compute expected incoming-edge Hamming loss `R_v(a)=sum_pm d_v(pm)*Hamming(a,pm)`.
6. Enumerate the frozen legal DAG universe and choose the single DAG minimizing `sum_v R_v(parent_mask(DAG,v))`.
7. The matched control is the same Bayes-action construction using only `m30_v` at every node. This isolates the value of S62 evidence at the action layer.
8. S46 promotion is applied identically. On non-promoted worlds both candidate and control use the baseline posterior's analogous Hamming-loss Bayes action.

The candidate does not alter S30, edge marginals, Brier score, or calibration. S65 tests only whether supported evidence improves the final structural action.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 98001;
- training: 64 + 64 worlds beginning 98101;
- validation: 32 + 32 worlds beginning 98501;
- held-out confirmation: 64 + 64 worlds beginning 98801.

## Matched metrics
- graph-action edge Hamming error candidate minus matched control;
- linear and heteroskedastic paired action differences;
- fraction of worlds where the candidate action differs from control;
- candidate/control large action harms (candidate exceeds control by >= 2 directed edges);
- held-out S62 error-localization AUC/Brier and proposal usefulness as mechanism checks;
- posterior calibration metrics are reported as invariant-by-construction rather than optimized.

## Training qualification
All must hold:
1. mechanics pass, identical trace, spend <= 15, valid selected DAG;
2. localization AUC >= 0.60 and Brier <= constant-prevalence Brier;
3. S62 proposal usefulness on anchor-error nodes > 0.50;
4. candidate differs from control on 2%-70% of worlds;
5. overall paired mean action-edge difference <= +0.03 edges;
6. heteroskedastic paired mean action-edge difference <= -0.08 edges;
7. linear paired mean action-edge difference <= +0.08 edges;
8. candidate large action harms <= control large action harms + 1.

## Validation qualification
Training gates plus overall paired mean action-edge difference <= 0 and heteroskedastic difference <= -0.04 edges, with no excess large harms.

## Confirmation qualification
Validation gates plus bootstrap 95% upper endpoint for overall paired action-edge difference < 0, heteroskedastic difference < -0.08 edges, and no excess large harms.

## Disposition and successor logic
- `SUPPORTED`: freeze S65 and test breadth/mechanism-shift transfer.
- `FALSIFIED_ACTION_GEOMETRY`: S62 evidence remains supported but decision action fails; next branch must test whether evidence should guide experiment allocation/information acquisition rather than terminal inference.
- `FALSIFIED_EVIDENCE_TRANSFER`: prospective S62 evidence fails; return to a new set-valued/intervention-invariance representation diagnostic.
- `BLOCKED_EXECUTION_*`: repair execution only without opening later panels.

Scientific falsification is a completed result and immediately redirects the queue.