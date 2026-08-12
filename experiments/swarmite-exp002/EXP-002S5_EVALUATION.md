# EXP-002S5 Evaluation

## Disposition
COMPLETE_PROMISING_FAILED_HARM_GUARDRAIL.

The nonlocal included-effect prior materially improved mean terminal edge recovery on fresh screen worlds: treatment-minus-control mean edge delta -0.3705 with 8/12 wins. Mean Brier delta +0.00450 satisfied the preregistered calibration ceiling. However, 3/12 worlds worsened by more than 0.50 edge-error units, exceeding the <=2/12 safety guardrail. S5 therefore does not advance to confirmation.

## Interpretation
Unlike predictive-score variants S2 and S4, S5 did not show universal density inflation and produced large gains in several worlds. This supports the structural hypothesis that distinguishing true nonzero effects from near-zero pseudo-edges can improve DAG discrimination. The remaining failure mode is brittleness: a narrow slab centered at magnitude 0.65 is more concentrated than the generator's actual 0.4-0.9 effect range.

The next experiment should preserve the nonlocal zero gap while widening support across the generator's effect-size range, rather than tune a single Gaussian width after seeing efficacy outcomes.