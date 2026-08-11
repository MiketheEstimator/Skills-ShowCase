# Swarmite Endless Improvement Worker

## Purpose
Maintain a persistent scientific improvement queue. Experiment completion is an internal event that immediately triggers evaluation and the next queued experiment. The hourly automation is only a watchdog/resumer.

## Worker state machine

PENDING -> RUNNING -> {COMPLETE | FAILED | BLOCKED}

On COMPLETE:
1. Persist raw results and traces.
2. Compare against preregistered controls under matched resources.
3. Update Established Findings only when supported.
4. Record anomalies and failure modes.
5. Generate materially justified successor experiments.
6. Append successors to QUEUE.json unless an existing item already tests the same uncertainty.
7. Mark current item COMPLETE.
8. Immediately pop the highest-priority runnable PENDING item and continue.

On FAILED:
1. Distinguish scientific falsification from execution failure.
2. Scientific falsification is a valid COMPLETE result.
3. Execution failure is FAILED/BLOCKED with exact cause.
4. Enqueue a materially different recovery experiment only when it tests the same scientific question without repeating the failed mechanism.
5. Pop next runnable item.

On runtime/tool limit:
1. Persist checkpoint, current experiment, completed substeps, artifacts, and exact next action.
2. Leave item RUNNING.
3. Watchdog resumes the RUNNING item before popping new work.

## Scientific invariants
- Ground truth never leaks to experiment designers.
- Resource budgets must be matched when comparing policies.
- Evaluation metrics must include terminal scientific quality, efficiency, and calibration; avoid single-metric reward gaming.
- Preserve negative results.
- Strong simple controls are mandatory.
- Separate training, validation, and held-out test worlds where learning occurs.
- Prefer paired-world comparisons and uncertainty intervals.
- Do not claim superiority when intervals are unresolved.
- Track compute cost separately from intervention cost for deeper search.
- Google Drive is read-only fodder. Never delete or modify Drive content.

## Improvement hierarchy
1. Correctness of experimental design.
2. Validity of controls and metrics.
3. Terminal scientific understanding.
4. Information/resource efficiency.
5. Generalization under world-model shift.
6. Compute efficiency.
7. Scale and open-world transfer.

## Queue discipline
The queue is not a fixed roadmap. Completed experiments can reorder, supersede, split, or append items based on evidence. It should never become empty while unresolved scientific uncertainties remain.
