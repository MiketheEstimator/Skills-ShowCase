# EXP-002S37 — Missing Terminal Class Localization: S30 as Anchor Expert

## Status
PENDING until execution marks RUNNING.

## Rationale
S36 found per-world represented-class oracle coverage of 1.0 but no seven-class global convex stack could noninferiorly cover all mechanism×noise cells. The key localization is that the strong comparator S30 is itself a per-world dynamic LG/TT mixture and was not represented as an expert inside S35. In validation tanh+Gaussian, every raw class had nonnegative mean delta versus S30. S37 tests whether omission of the S30 science posterior as an anchor expert explains the global feasibility failure.

## Frozen diagnostic
Reuse only S35 training worlds 72201–72248 and validation worlds 72261–72296. Add an eighth expert `S30` whose posterior/edge error is exactly the frozen S30 science output on each world. The other experts remain `LG,TG,TT,SG,ST,AG,AT`.

Solve exact minimax LPs separately on training and validation over the eight-expert simplex, minimizing maximum factorial-cell mean edge delta versus S30. Since the S30 anchor has zero delta by definition, the LP must be weakly noninferior; the scientific question is whether specialized experts can create a strictly negative robust improvement while retaining the S30 safety floor.

## Dispositions
- `ANCHOR_RESOLVES_FEASIBILITY` if exact worst-cell mean delta <= -0.01 on both training and validation and overall mean delta < 0 on both.
- `ANCHOR_ONLY_SAFE` if both exact worst-cell deltas are within [-0.01,+0.001] and S30 receives >=0.90 weight on either split.
- `ANCHOR_TRANSFER_UNSTABLE` if one split achieves <=-0.01 worst-cell delta but the other does not.
- `MIXED_ANCHOR_RESULT` otherwise.

## Success
Diagnostic completion requires exact LP convergence and a frozen disposition. No treatment is promoted from retrospective data.

## Invariants
No new worlds, no tuning, no deployment selector, no changes to planning. Ground truth is retrospective diagnostic only. Google Drive remains read-only.
