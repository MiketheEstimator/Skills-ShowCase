# EXP-002S1 Evaluation

## Disposition
COMPLETE_FALSIFIED_AT_SCREEN.

The collision-free Normal-Inverse-Gamma / Student-t likelihood treatment passed mechanics but failed prospective efficacy on fresh seeds 65811-65822. Mean treatment-minus-control edge-error delta was +0.70734, mean Brier delta +0.02067, wins/losses 4/8, six worlds worsened by >0.50, and net MAP delta was -2. Confirmation is not justified.

This result falsifies the hypothesis that simply integrating residual-scale uncertainty repairs the benchmark's family-evidence pathology. Together with R21-R24 it indicates that prior-volume/fixed-noise sensitivity is not solved by either coefficient covariance redesign or conjugate scale integration.

Next direction: replace closed-form marginal likelihood as the structural scoring primitive with a prequential predictive-evidence score computed from held-out/sequential observations. This changes the model-selection evidence mechanism rather than another prior or search-policy tweak.