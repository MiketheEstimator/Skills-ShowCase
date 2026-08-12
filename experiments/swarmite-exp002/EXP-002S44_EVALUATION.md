# EXP-002S44 Evaluation

**Disposition:** FALSIFIED_ON_CONFIRMATION

S44 froze the S43 topology-class decision without retuning and evaluated it under simultaneous graph-density and heteroskedastic nonlinear mechanism shift.

## Screen
Class-aware coverage 1.000; hybrid edge delta -0.712383; CI [-0.9894502145350491, -0.38166755568794597]; Brier 0.001834; harm rate 0.042; retention 1.000.
Frozen S39 control hybrid edge delta -0.712383; coverage 1.000.

### Joint cells
- **dense_asinh**: n=4, coverage=1.000, hybrid edge delta=-0.300482, harm rate=0.000
- **dense_sin**: n=4, coverage=1.000, hybrid edge delta=-0.230452, harm rate=0.250
- **dense_tanh**: n=4, coverage=1.000, hybrid edge delta=-0.581156, harm rate=0.000
- **sparse_asinh**: n=4, coverage=1.000, hybrid edge delta=-0.992295, harm rate=0.000
- **sparse_sin**: n=4, coverage=1.000, hybrid edge delta=-1.111769, harm rate=0.000
- **sparse_tanh**: n=4, coverage=1.000, hybrid edge delta=-1.058146, harm rate=0.000

## Confirmation
Class-aware coverage 1.000; hybrid edge delta -0.850876; CI [-1.048643196950944, -0.6492041030945005]; Brier -0.005979; harm rate 0.042; retention 1.000.
Frozen S39 control hybrid edge delta -0.850876; coverage 1.000.

### Joint cells
- **dense_asinh**: n=8, coverage=1.000, hybrid edge delta=-0.483559, harm rate=0.125
- **dense_sin**: n=8, coverage=1.000, hybrid edge delta=-0.689673, harm rate=0.125
- **dense_tanh**: n=8, coverage=1.000, hybrid edge delta=-1.016700, harm rate=0.000
- **sparse_asinh**: n=8, coverage=1.000, hybrid edge delta=-0.957081, harm rate=0.000
- **sparse_sin**: n=8, coverage=1.000, hybrid edge delta=-1.259868, harm rate=0.000
- **sparse_tanh**: n=8, coverage=1.000, hybrid edge delta=-0.698373, harm rate=0.000

## Next
S44 falsified topology-only utility propagation under compound shift; replace the topology-only class posterior with an explicit joint latent class over topology × nonlinear mechanism/noise rather than retuning scalar thresholds or S43 parameters.