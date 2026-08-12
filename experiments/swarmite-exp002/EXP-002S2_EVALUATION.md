# EXP-002S2 Evaluation

## Disposition
COMPLETE_FALSIFIED_AT_SCREEN.

The preregistered prequential predictive-evidence treatment failed decisively on fresh screen seeds 66011-66022. Treatment-minus-control mean terminal edge-error delta was +1.6118, mean Brier delta was +0.03291, only 1/12 worlds improved, 11/12 worsened, and 11/12 exceeded the +0.50 large-harm threshold. The protocol therefore forbids confirmation exposure.

## Failure signature
The treatment posterior was denser than ground truth in all 12 screen worlds. Mean treatment expected edge count was 5.812 versus mean true edge count 3.583, a +2.229 edge bias. This is consistent with a family-size scoring defect rather than a planner-only failure.

## Scientific interpretation
The frozen S2 construction gave the first 10 eligible rows to every candidate family as an unscored warm-start. Larger families therefore received extra fitting capacity on those rows without paying evidence cost for that capacity. Because efficacy failure was accompanied by a universal dense-graph shift, the next justified step is a diagnostic of parent-count score advantage followed by an out-of-sample scoring mechanism that does not grant an unpenalized warm-start.

No confirmation worlds were inspected.