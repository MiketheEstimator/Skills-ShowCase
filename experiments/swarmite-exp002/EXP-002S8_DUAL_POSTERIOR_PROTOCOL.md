# EXP-002S8 — Dual-Posterior Separation of Planning and Structural Inference

## Status
RUNNING after protocol freeze.

## Hypothesis
S7 shows that S5's nonlocal posterior improves terminal structural inference when evaluated on the baseline controller's intervention sequence, while feeding that posterior back into proposal/EIG selection creates the harmful worlds. Separating the planning posterior from the reporting posterior should preserve the inference gain while preventing policy-feedback harm.

## Frozen design
Maintain two posteriors over the same observations.

1. Planning posterior: the committed benchmark-v2 fixed-noise TAU2=4 posterior. It alone drives proposal generation, EIG scoring, action selection, and all intervention decisions.
2. Structural posterior: the frozen S5 nonlocal included-effect evidence model with slab 0.5*N(-0.65,0.15^2)+0.5*N(+0.65,0.15^2) per included edge. It receives exactly the same observational and interventional rows but never influences planning. Terminal edge error, Brier, MAP, and true-mass metrics are reported from this structural posterior.

Control is benchmark-v2 width-1 portfolio inference and planning. Intervention budget, proposal count, action sequence RNG, environment RNG, and intervention costs are therefore exactly matched by construction. Additional inference compute is tracked separately.

## Mechanics gate
Fresh seeds 66801-66804. Verify exact 29,281-DAG support for both posteriors, identical action trace and intervention spend to control, finite normalized structural posterior, deterministic replay, and no structural-posterior values entering proposal/EIG calls.

## Prospective screen
Fresh seeds 66811-66822. Pass only if structural-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If passed, confirm on fresh seeds 66901-66924. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=3/24 large harms, and exact trace identity to control in every world.

## Scientific distinction
This is an architecture change in state use: one posterior for intervention planning and a different posterior for structural inference. It is not another prior-width tuning experiment and directly tests the policy-feedback mechanism supported by S7.