# EXP-002R5 — Monte-Carlo EIG Winner's-Curse Audit

## Hypothesis
Benchmark-v2 width-2 fails to convert local estimated-EIG gains into terminal recovery because selecting the maximum over twice as many low-simulation EIG estimates amplifies Monte-Carlo optimism. The extra swarm therefore wins the judge partly by noise rather than by genuinely higher expected information.

## Material difference from prior breadth experiments
This is not another width threshold or breadth retry. It holds the frozen proposal generator and environment fixed and audits the reliability of the planner's EIG estimator itself.

## Design
On fresh diagnostic worlds, preserve the deployed 3-simulation EIG score used for action selection. At each decision, independently rescore all affordable width-2 candidates using a high-precision posterior-predictive estimate with 30 simulations and a separate `v2|audit-planner` RNG namespace. Record: low-vs-high EIG rank correlation; low-score optimism of the selected candidate; fraction of deployed selections that are not high-precision argmax; whether extra-swarm selections are more optimistic than base-swarm selections; and high-precision incremental EIG of width-2 over the width-1 candidate subset.

## Primary diagnostic
Mean selection optimism = deployed 3-sim EIG minus independent 30-sim EIG for the action selected by the deployed planner, stratified by base-swarm vs extra-swarm provenance.

## Falsification
Winner's curse is supported only if extra-swarm selected actions show materially larger positive selection optimism and/or misranking than base-swarm selections. If high-precision rescoring confirms the extra swarm's local EIG advantage without excess optimism, redirect toward horizon/credit mismatch instead.

## Initial stage
Run 6 fresh worlds as a diagnostic screen. No policy parameters are tuned from these outcomes.
