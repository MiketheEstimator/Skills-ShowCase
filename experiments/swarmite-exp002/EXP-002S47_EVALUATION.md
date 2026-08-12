# EXP-002S47 Evaluation

**Disposition:** FALSIFIED_AT_SCREEN

The exact S46 risk model and rule were frozen; no S47 fitting or threshold selection occurred.

## Screen
Coverage 0.854; edge delta -0.383781; CI [-0.6209020448946947, -0.17945487776978916]; Brier -0.002708; harm rate 0.024; retention 0.966.

### By regime
- **linear**: coverage=0.750, edge=-0.000372, harm=0.000
- **weak_effect**: coverage=0.875, edge=0.004013, harm=0.000
- **compound_t**: coverage=1.000, edge=-0.973684, harm=0.000
- **heteroskedastic**: coverage=0.750, edge=-0.718230, harm=0.167
- **topology**: coverage=1.000, edge=-0.002401, harm=0.000
- **joint**: coverage=0.750, edge=-0.612013, harm=0.000

## Next
S47 identified breadth-transfer failure; isolate the unsupported regime(s) from prospective breadth results and introduce a materially targeted robustness mechanism rather than globally refitting the successful S46 risk model.