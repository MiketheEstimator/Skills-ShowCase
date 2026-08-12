# EXP-002S33 Evaluation

**Disposition:** EXPANDED_MODEL_SET_FALSIFIED

Expanded minus frozen S30 edge delta: **0.062056**; bootstrap 95% CI [-0.06236321273465108, 0.17679359181349777]
Brier delta vs S30: **-0.007961**
Large harms vs S30: **4/36**
Expanded edge delta vs baseline: **0.123706**
Wins vs S30: **14/36**

## Mean model weights
- **LG**: 0.2250
- **TG**: 0.2514
- **TT**: 0.0373
- **SG**: 0.1904
- **ST**: 0.0307
- **AG**: 0.2287
- **AT**: 0.0366

## By factorial cell
- **tanh_gaussian**: Δedge vs S30 -0.106069; Δedge vs baseline -0.109831; ΔBrier vs S30 -0.009586
- **tanh_t7**: Δedge vs S30 0.108549; Δedge vs baseline 0.009585; ΔBrier vs S30 -0.009675
- **sin_gaussian**: Δedge vs S30 -0.011867; Δedge vs baseline 0.266742; ΔBrier vs S30 -0.010161
- **sin_t7**: Δedge vs S30 -0.028218; Δedge vs baseline -0.073864; ΔBrier vs S30 -0.016343
- **asinh_gaussian**: Δedge vs S30 0.103171; Δedge vs baseline 0.079742; ΔBrier vs S30 -0.003981
- **asinh_t7**: Δedge vs S30 0.306770; Δedge vs baseline 0.569858; ΔBrier vs S30 0.001979

## Next
S33 expanded the represented mechanism×noise classes but failed promotion; diagnose whether predictive weighting, class dilution, or residual model-set insufficiency caused failure before changing temperature or adding classes.