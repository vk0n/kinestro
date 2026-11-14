<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# M1/E1 electromagnetic tracking research

**Numerical and literature research only. E1 remains open pending physical validation.** No hardware was built, measured, ordered, or selected; no human data was collected. This is an isolated research package, not Kinestro application software, firmware, a driver, or an approved tracking architecture.

Start with the [feasibility report](feasibility-report.md), [architecture comparison](architecture-comparison.md), [simulation results](simulation-results.md), [power analysis](power-feasibility.md), [proposed bench plan](bench-validation-plan.md), and [primary reference register](references.md).

## Reproduce

The recorded run used CPython **3.14.7**; exact tested package versions are in [requirements.txt](requirements.txt) and output metadata. Use a separate environment. From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
MPLCONFIGDIR=/tmp/kinestro-e1-matplotlib .venv/bin/python -m e1.run
```

The default run uses seed `20261115` and six Monte Carlo trials per anatomical point per noise level. It writes compact CSV/JSON summaries to `results/` and two original SVG figures to `figures/`. It performs 4,320 primary pose fits plus initialization diagnostics. For a separate output without overwriting committed results:

```sh
MPLCONFIGDIR=/tmp/kinestro-e1-matplotlib .venv/bin/python -m e1.run \
  --seed 20261115 --trials 6 --output /tmp/kinestro-e1-results \
  --figures /tmp/kinestro-e1-figures
```

Small numerical differences across Python/BLAS/platform versions are possible. Same-environment reproducibility and mathematical tests are checked; this is not a claim of bitwise portability. A different seed/trial count is a new simulation and must not be compared as if it were the committed run. The program never opens a device, network connection, or input-injection interface.

## Files and boundaries

| File | Purpose |
| --- | --- |
| [e1/model.py](e1/model.py) | Free-space dipole field and finite thin circular transmitter-loop quadrature; configurable moments, origins, RX orientation/axes |
| [e1/geometry.py](e1/geometry.py) | Explicit assumed body sizes, six paired arm poses, waist/chest frames, receiver location and orientation |
| [e1/estimation.py](e1/estimation.py) | Measurement-only analytic initialization, nonlinear pose fit, SO(3) attitude metric, locally scaled Jacobian/SVD |
| [e1/run.py](e1/run.py) | Seeded independent-noise and model-mismatch scenarios, ambiguity/initialization/two-receiver diagnostics, aggregates and figures |
| [tests/test_physics.py](tests/test_physics.py) | Independent closed-form limits, scale/rotation/ambiguity invariants, inverse and observability checks |
| [results/summary.json](results/summary.json) | Configuration, library versions, all scenario distributions/failures and ambiguity diagnostics |
| [results/workspace.csv](results/workspace.csv) | All 72 targets, frames, body sizes, receiver/limb coordinates, distances and field scales |
| [results/pose_summary.csv](results/pose_summary.csv), [body_size_summary.csv](results/body_size_summary.csv), [distance_summary.csv](results/distance_summary.csv) | Conditional error/failure distributions instead of only pooled successes |
| [results/observability.csv](results/observability.csv), [finite_field.csv](results/finite_field.csv) | Reduced-axis ranks, scaled conditioning and local precision bounds; finite-model mismatch |

Code, tests, dependency pins, and research ignore rules use `MPL-2.0`. Original documentation and derived synthetic report artifacts use `CC-BY-4.0`; [REUSE.toml](REUSE.toml) narrowly labels generated CSV/JSON/SVG outputs. No external datasets or third-party code are copied. See the repository [licensing policy](../../LICENSE.md).
