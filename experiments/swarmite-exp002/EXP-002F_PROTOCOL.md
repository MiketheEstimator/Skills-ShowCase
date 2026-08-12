# EXP-002F — Isolated-RNG Matched-Depth Ablation

## Objective
Determine whether the apparent differences between one-step and two-step Bayesian proposal lookahead are caused by lookahead depth itself rather than stochastic proposal generation or RNG consumption inside planning simulations.

## Hypothesis
With proposal-generation randomness and environment randomness held identical across paired arms, two-step lookahead will improve terminal edge recovery relative to one-step lookahead under equal total experiment cost.

## Primary metric
Paired difference in terminal edge error: `two_step - one_step`.

## Secondary metrics
- True-DAG posterior mass
- Exact MAP graph recovery
- Posterior entropy
- Wall-clock compute and planner simulation count

## Controls
- Same held-out worlds
- Same initial posterior
- Same candidate proposal set at every decision point
- Same proposal-generator RNG stream
- Same observation/environment RNG stream
- Separate planner-only RNG stream for simulated lookahead outcomes
- Same total intervention-cost budget
- Same stopping rules

## Treatment isolation
At each real decision step, generate the candidate intervention set once from a deterministic proposal RNG keyed by `(world_seed, step_index)`. Feed that identical candidate set to both arms.

One-step arm scores each candidate using one-step expected value.

Two-step arm may use a separate planner RNG keyed by `(world_seed, step_index, candidate_id)` to simulate downstream outcomes, but this RNG must not alter candidate generation or the real environment sequence.

Real observations for each arm must use paired environment seeds derived only from `(world_seed, arm, real_step_index)` and never from the number of planning simulations consumed.

## Preregistered sample / decision rule
Run at least 24 matched worlds, extending to 48 if the primary 95% paired bootstrap CI still crosses zero. Declare support only if the CI excludes zero in the favorable direction. Declare practical equivalence only if the full CI lies inside ±0.05 edge error. Otherwise mark unresolved at n=48.

## Failure diagnostics
If MAP accuracy and posterior entropy diverge again while edge error remains unresolved, enqueue a posterior-calibration experiment rather than increasing search depth.

If isolated RNG materially changes the effect estimate relative to EXP-002E2, classify stochastic coupling as a confirmed confounder.

## Resource accounting
Report real intervention cost separately from planner compute. Do not allow additional planner compute to count as experimental budget, but record simulations and wall-clock time for efficiency comparisons.
