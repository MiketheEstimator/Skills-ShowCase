# EXP-002R8 — EIG Alignment Regime Validation

## Motivation
EXP-002R7 rejected a simple universal horizon-mismatch story: high-precision one-step EIG had positive mean terminal-edge rank alignment, but alignment ranged from strongly positive to negative across worlds. A post-hoc diagnostic on the six R7 worlds found initial mean edge uncertainty was the strongest observed moderator (Pearson r about +0.60), while initial posterior entropy, max posterior mass, true-DAG mass, and graph edge count were weaker. This observation is hypothesis-generating only.

## Hypothesis
The terminal usefulness of one-step entropy EIG is state-dependent: it aligns better with terminal edge recovery when posterior edge marginals are broadly uncertain, and becomes unreliable when edge uncertainty is already relatively concentrated.

## Prospective design
Run 12 fresh validation worlds not used in R7. At the initial observational posterior, record mean edge uncertainty `mean(4p_e(1-p_e))` without ground-truth access. Repeat the frozen R7 intervention-forcing audit: generate width-2 decision-0 candidates, estimate each with independent 30-simulation EIG, force each candidate as the first intervention, then complete the remaining budget with frozen width-1 control. Ground truth is used only for terminal evaluation.

## Primary test
Across validation worlds, correlate initial mean edge uncertainty with the within-world Spearman correlation between candidate EIG and negative terminal edge error. Report Pearson and Spearman moderator correlations plus bootstrap 95% confidence intervals by resampling worlds.

## Secondary tests
Compare moderator strength against initial posterior entropy and max posterior mass. Record EIG-argmax terminal rank and regret. No threshold or gating policy is fit in this experiment.

## Success criterion
Treat the regime hypothesis as supported only if the uncertainty moderator correlation is positive and its world-bootstrap 95% interval excludes zero, and it is at least as strong as the entropy/max-mass alternatives. Otherwise falsify this moderator and redirect toward proposal semantics or posterior-model calibration.

## Checkpoint discipline
The 12 worlds are fixed as seeds 55001 through 55012. Partial batches may be persisted atomically and pooled only because the executable benchmark-v2 engine and seed mapping are frozen.