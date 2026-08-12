# EXP-002S10 — Dual-Posterior Transfer Under Nonlinear Mechanism Shift

## Status
RUNNING after protocol freeze.

## Hypothesis
S8-S9 show robust gains across effect-size shift, but both true worlds remain linear. The dual-posterior structural inference should be treated as broadly robust only if its advantage survives moderate mechanism-form misspecification without changing planning actions relative to the matched control.

## Frozen transfer worlds
Use the benchmark-v2 DAG topology and coefficient generator with original nonzero magnitudes 0.4-0.9. Replace each structural equation's parent contribution `x_u * W[u,v]` with `tanh(x_u) * W[u,v]`; additive N(0,1) noise, intervention semantics, observation count, costs, and budget remain unchanged. This creates smooth nonlinear mechanisms while preserving graph topology and effect signs.

Control uses the committed linear benchmark posterior for both planning and terminal inference, but receives data from the nonlinear environment. Treatment uses the exact S8 architecture without retuning: the same linear benchmark posterior drives every planning decision, while the frozen S5 nonlocal linear structural posterior is terminal output only. Both arms must therefore have identical intervention traces by construction.

## Mechanics gate
Fresh seeds 67201-67204. Verify deterministic nonlinear-world replay, exact 29,281-DAG support, finite normalized posteriors, spend <=15, and treatment/control action-trace identity.

## Prospective screen
Fresh seeds 67211-67222. Pass only if mean edge delta <= -0.10, mean Brier delta <= +0.005, <=2/12 worlds worsen by >0.50, and every action trace is identical.

If passed, confirm on 67301-67324 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=3/24 large harms, and exact trace identity.

If falsified, preserve the negative result and redirect toward a structural posterior that explicitly models nonlinear parent effects rather than retuning the linear nonlocal prior on these worlds.