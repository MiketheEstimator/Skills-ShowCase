# EXP-002S38 — Specialist Residual Value Over the S30 Anchor

## Status
PENDING until execution marks RUNNING.

## Rationale
S37 showed that the exact robust convex solution over S30 plus seven specialists is 100% S30 on both exposed splits. This rules out a static global mixture but does not tell us whether one specialist is independently safe, whether specialist gains are highly heterogeneous, or whether the specialists are more useful as uncertainty witnesses than as point-posterior corrections.

## Frozen retrospective diagnostic
Reuse only S35 training worlds 72201–72248 and validation worlds 72261–72296. For each raw specialist `TG,TT,SG,ST,AG,AT` (LG is omitted because S30 already contains the LG anchor), compute versus S30 separately on both splits:
- mean edge-error delta;
- win rate;
- mean improvement conditional on winning;
- mean harm conditional on losing;
- large-harm rate (>0.50 edge-error worsening);
- 90th percentile harm among losses;
- factorial-cell mean deltas.

Also compute the per-world oracle specialist gain over S30 and oracle-class concentration.

## Frozen diagnostic rule
A `SAFE_SPECIALIST` exists only if the same specialist on **both** splits satisfies: mean edge delta <= -0.10, win rate >= 0.70, and large-harm rate <= 0.05.

Disposition:
1. `SAFE_SPECIALIST_IDENTIFIED` if such a specialist exists.
2. `HETEROGENEOUS_RESIDUAL_VALUE` if no safe specialist exists, but oracle specialist coverage >= 0.80 and mean oracle improvement >= 0.20 on both splits.
3. `LOW_RESIDUAL_VALUE` if oracle specialist coverage < 0.80 or mean oracle improvement < 0.20 on either split.
4. `MIXED_RESIDUAL_VALUE` otherwise.

## Scientific meaning
If residual value is heterogeneous, do not repeat failed hard selectors or predictive weighting. The next mechanism should use specialist disagreement to improve calibration/traceability while preserving S30 as the point-estimate anchor.

## Invariants
No new worlds, no tuning, no deployment selector, no point-posterior modification. Ground truth is retrospective diagnostic only. Google Drive remains read-only.
