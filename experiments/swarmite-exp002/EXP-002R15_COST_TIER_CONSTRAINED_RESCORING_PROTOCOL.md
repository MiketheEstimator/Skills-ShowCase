# EXP-002R15 — Cost-Tier-Constrained Selective Terminal Rescoring

## Status
RUNNING after protocol freeze; no prospective R15 world has been observed.

## Motivation
R13 produced a favorable mean edge-error delta (-0.133), better average Brier and true-DAG mass, and bounded compute, but failed its strict 8/12 win criterion because four worlds tied and three lost. The post-hoc R14 heterogeneity audit found no useful terminal-margin or one-step-gap gate. The only concrete mechanistic warning was the sole override to a higher intervention-cost tier, which was harmful. This is exploratory and must be prospectively tested.

## Hypothesis
The useful R13 terminal-planning signal is concentrated among cost-neutral or cost-reducing overrides. Disallowing terminal rescoring from increasing first-intervention cost will preserve large beneficial overrides while suppressing a source of harmful treatment heterogeneity.

## Frozen design
Use 12 fresh benchmark-v2 worlds, seeds 61001 through 61012. Score the same ten fixed interventions with 30-simulation one-step EIG. Form the same top-3 shortlist. Remove from override eligibility any shortlist candidate whose intervention cost exceeds the one-step argmax cost. Apply four remaining-budget terminal rollouts only to eligible shortlist candidates. If no alternative eligible candidate beats the control terminal score, retain the one-step action. Continue both chosen real arms with the frozen width-1 controller and budget 15. RNG namespaces remain isolated by world, arm, action, rollout and continuation step.

## Primary endpoint
Paired terminal edge error, treatment minus one-step control.

## Secondary endpoints
Brier, true-DAG mass, MAP recovery, override frequency, harmful-override frequency, intervention cost, and planner simulations.

## Promotion criteria
Promote only if all hold: mean paired edge-error delta <= -0.10; no more than 2/12 worlds worsen by >0.10 edge-error units; mean Brier delta <= +0.005; mean planner-simulation ratio <=10x one-step audit. Otherwise falsify the cost-tier gate and redirect away from this terminal-rescoring family.

## Checkpoint discipline
Persist each world atomically. R13/R14 observations are training/exploratory only and are not pooled into the R15 prospective statistics.