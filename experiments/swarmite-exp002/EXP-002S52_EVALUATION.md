# EXP-002S52 Evaluation

**Disposition:** FALSIFIED_AT_TRAINING

S52 was falsified at training: the 42-feature latent residual-state model showed useful specialist-win discrimination (training AUC 0.8360836083608361, Brier 0.12439288888984713 versus constant 0.1664478922540713) but every preregistered hard-selection rule used the specialist zero times, so no rule qualified. Hard selection, not the latent representation itself, is the immediate failure mode.

## Execution note
The original workflow correctly stopped scientific progression at the training gate, but its subsequent validation step failed while attempting to `git add` a deliberately absent validation artifact. That workflow-control failure is repaired here without exposing validation or confirmation worlds.

## Next
Test continuous residual-state-driven terminal model averaging. Do not retune S52 hard cutoffs.
