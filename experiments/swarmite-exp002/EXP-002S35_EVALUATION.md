# EXP-002S35 Evaluation

**Disposition:** STRUCTURAL_STACKING_FALSIFIED_VALIDATION

Selected weights: `{'LG': 0.6031615676768385, 'TG': 0.012514340621518289, 'TT': 0.059462254638280025, 'SG': 0.014319773478203093, 'ST': 0.23050576871928283, 'AG': 0.02753635294358805, 'AT': 0.0524999419222891}`
Training minimax objective: `{'worst_cell_delta': 0.1276709676332539, 'mean_delta': 0.037527103820187736, 'l2': 0.42434870513085254}`

Evaluation edge delta vs S30: **0.002411**
95% CI: [-0.08652042734333419, 0.09892142080733121]
Brier delta vs S30: **-0.001139**
Large harms: **2**

## Next
Training-optimized global structural weights failed fresh validation; diagnose training-distribution instability versus irreducible per-world heterogeneity before any adaptive stacking.