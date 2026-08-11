# EXP-002R12 Evaluation

## Disposition
COMPLETE_FALSIFIED_PREREGISTERED_CRITERIA.

## Primary result
Across six preregistered worlds, the mean Spearman alignment between score and negative realized terminal edge error was 0.135 for 30-simulation one-step EIG and 0.091 for full remaining-budget terminal VOI. The paired mean change was -0.044 with bootstrap 95% CI [-0.426, +0.372], failing the preregistered +0.15 alignment threshold.

## Regret anomaly
Despite worse average rank alignment, the terminal-VOI argmax reduced terminal edge-error regret in 4/6 worlds. Mean regret fell from 0.312 to 0.122, a mean improvement of 0.191 edge-error units. This is a real anomaly worth following, but it is not sufficient to promote R12 because the primary alignment criterion failed.

## Compute
The terminal rollout used 29.65x to 44.73x the one-step audit compute across the six worlds, averaging 37.72x. This exceeds the preregistered 25x pathological-compute ceiling in every world.

## Scientific interpretation
Full-horizon rollout is not validated as a general ranking objective. However, its occasional strong argmax regret reduction suggests terminal planning may contain useful information concentrated near the decision boundary rather than across the entire 10-action ranking. The next experiment should therefore test selective terminal rescoring of a small one-step shortlist, rather than repeating full-action full-horizon ranking.

## Negative-result preservation
No R12 observation is promoted as evidence that deeper planning is generally superior. The supported conclusion is narrower: exhaustive terminal VOI ranking is too expensive and does not improve mean rank alignment under benchmark v2, while a decision-focused regret signal remains unresolved.