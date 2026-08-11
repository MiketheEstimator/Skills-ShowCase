# EXP-002E Smoke Checkpoint — Two-Step Bayesian Proposal Lookahead

Status: RUNNING / mechanics validated / evidence insufficient.

## Hypothesis
Scoring concrete designer proposals by expected downstream terminal value over two experiment steps will outperform one-step proposal scoring under matched total cost.

## Execution note
The exact 29,281-DAG two-step implementation is materially more expensive than the one-step controllers. A 5-world pilot exceeded the current execution ceiling, so a 2-world smoke test at total cost budget 7 was run only to validate mechanics. It is not an inferential test of the hypothesis.

## Smoke result
| Mode | Edge error ↓ | True-DAG mass ↑ | MAP correct | Posterior entropy ↓ | Cost | Steps |
|---|---:|---:|---:|---:|---:|---:|
| One-step proposal scoring | 1.1502 | 0.2766 | 100% | 3.5110 | 7.0 | 7 |
| Two-step lookahead | 1.3273 | 0.2129 | 100% | 3.7965 | 7.0 | 7 |

Paired two-step minus one-step: edge error +0.1771; true-DAG mass -0.0637; entropy +0.2856.

## Interpretation
The smoke result leans against the hypothesis but n=2 is intentionally too small to support a scientific conclusion. The implementation is now validated. The next queue event should resume EXP-002E using batched matched worlds and/or reduce computation through cached simulated posterior transitions so a meaningful paired sample can complete within runtime limits.

## Required next action
1. Cache first-step simulated posterior states by (state fingerprint, proposal, sampled hypothesis).
2. Run matched batches independently and accumulate at least 12 held-out worlds.
3. Compare one-step vs two-step under identical total cost and seeds.
4. Bootstrap paired differences before marking EXP-002E COMPLETE or FAILED.
