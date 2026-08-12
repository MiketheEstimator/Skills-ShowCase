# State-Dependent Controller V5

## Hypothesis
A tabular state-dependent controller using uncertainty, budget phase, and intervention coverage can learn when to switch among information-gain, falsification, cheapest-test, and novelty roles.

## Method
The controller was trained across a mixture of original and transfer causal worlds. Three explicit scientific utility profiles were tested: discovery, efficiency, and balanced. The policy received Monte Carlo episode-level credit for state/action choices and was frozen before held-out evaluation.

## Result
The hypothesis was not supported. The learned controller did not beat the best fixed policy for any profile.

### Discovery profile
- Original: learned 96.98% recovery vs novelty 97.24%.
- Transfer: learned 92.62% vs novelty 93.37%.

### Efficiency profile
- Original: learned utility 0.8546 vs novelty 0.8571.
- Transfer: learned utility 0.8193 vs information-gain 0.8202.

### Balanced profile
- Original: learned utility 0.8341 vs novelty 0.8406.
- Transfer: learned utility 0.7548 vs novelty 0.7799.

## Interpretation
The state representation is aliased. Uncertainty, elapsed budget, and coverage do not sufficiently identify whether the current causal world is sparse/clean or dense/noisy, nor whether recent observations indicate model mismatch. Episode-level credit assignment is also too weak to learn reliable switching behavior from a small training population.

## Established finding
State dependence is not automatically beneficial. A learned controller must have state variables that expose the environmental properties that actually determine which experiment-design policy is valuable.
