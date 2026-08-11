# EXP-002S43 Policy-Collapse Diagnostic

## Observation
The preregistered S43 decision rule was:

`promote S30 iff expected_delta < 0 and expected_harm <= 0.05`.

Training estimated:
- sparse mean S30 edge delta = **-0.1764241343**; sparse large-harm rate = **0.0**;
- dense mean S30 edge delta = **-0.0404034347**; dense large-harm rate = **0.0**.

For any topology posterior `q=P(dense|data)` in [0,1]:

`expected_delta = (1-q)*(-0.1764241343) + q*(-0.0404034347) < 0`

and

`expected_harm = 0`.

Therefore the frozen S43 class-aware policy promotes S30 for **every possible q**. It is exactly equivalent to an unconditional always-S30 policy under the fitted training parameters.

## Consequence
S43's prospective success is real as a policy outcome, but it does **not** establish that topology-class uncertainty caused the gain. The gain relative to S39 came from removing scalar-gate abstention. S42 remains independently supported as a topology-identification diagnostic, but S43 does not yet demonstrate decision value from that representation.

## Scientific disposition
Preserve the preregistered S43 result, but qualify it as `SUPPORTED_POLICY_OUTCOME / VACUOUS_CLASS_DEPENDENCE`.

The next experiment should compare the simpler always-S30 policy against the existing uncertainty-gated architecture under a compound topology + heteroskedastic observation shift. If unconditional S30 remains safe, prefer the simpler policy. If it fails, the next uncertainty representation must introduce finer world classes (mechanism/noise/topology) that can actually change the decision.
