# EXP-002S20 Evaluation

**Disposition:** FALSIFIED_AT_SCREEN

## Mechanics
- `{'n': 4, 'dag_count_ok': True, 'spend_ok': True, 'trace_identical_all': True, 'planning_reconstruction_ok': True, 'posteriors_normalized': True, 'weights_valid': True}`

## Prospective screen
- Mean edge delta vs planning control: 0.955714
- Mean Brier delta vs planning control: 0.017400
- Mean Brier delta vs fixed S5: 0.005673
- Large harms: 10
- Mean model weights: [0.008009599252305724, 0.07035143299608315, 0.9216389677516111]

## Next direction
S20 did not promote; diagnose model-class evidence domination and shared likelihood misspecification before adding any new model class.