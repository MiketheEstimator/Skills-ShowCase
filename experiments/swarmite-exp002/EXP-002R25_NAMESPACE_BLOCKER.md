# EXP-002R25 Namespace Blocker

R25 was frozen as the scale-integrated Normal-Inverse-Gamma / Student-t family-evidence experiment. Before prospective efficacy exposure, the intended runner path `experiments/swarmite-exp002/swarmite_exp002_r25.py` was found to already contain an unrelated scaled-intervention experiment.

Overwriting that executable would destroy lineage and violate the queue's reproducibility invariant. No R25 efficacy worlds were exposed or counted. The four local mechanics checks for the intended likelihood mechanism are not pooled because they were executed before a durable unique executable path existed.

Disposition: `BLOCKED_EXECUTABLE_NAMESPACE_COLLISION`. Recover the same scientific question under a fresh experiment ID and runner path, freeze that lineage, rerun mechanics atomically, then expose fresh efficacy worlds.