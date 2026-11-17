<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# M1/E1 electromagnetic tracking research

**Numerical/literature research and a proposed physical POC. E1 remains open pending physical validation.** No hardware was built, measured or ordered; no product components or architecture were approved and no human data was collected. This is an isolated research package, not Kinestro application software, firmware or a driver.

Start with the [feasibility report](feasibility-report.md), [architecture comparison](architecture-comparison.md), [simulation results](simulation-results.md), [power analysis](power-feasibility.md), [proposed bench plan](bench-validation-plan.md), and [primary reference register](references.md).

The [physical POC research outline](physical-poc/README.md) includes the owner's visual references, an independent engineering audit, corrected geometry and POC-1 through POC-4 research questions. Detailed validation requirements remain in the bench plan; E1 is open and no physical results are claimed.

The [boundary/hemisphere extension](simulation-results.md#boundary-and-hemisphere-validation-boundary-v1) evaluates negative y, exact y=0, near-boundary positions and continuous crossings separately from the original positive-y baseline. A locally accurate or continuous estimate does not establish the absolute branch. E1 and the hardware architecture remain open.

## Reproduce

The recorded run used CPython **3.14.7**; exact tested package versions are in [requirements.txt](requirements.txt) and output metadata. Use a separate environment. From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
MPLCONFIGDIR=/tmp/kinestro-e1-matplotlib .venv/bin/python -m e1.boundary_run
```

The boundary runner uses seed `20261116`, two noise trials, 41 frames per trajectory, and explicit independent random streams for static, initialization and trajectory studies. It writes only `results/boundary-v1/` and `figures/boundary-v1/`. Its 144 abstract off-body poses and six trajectories per mount are not additional anatomical measurements. Use a separate output to check reproducibility:

```sh
MPLCONFIGDIR=/tmp/kinestro-e1-matplotlib .venv/bin/python -m e1.boundary_run \
  --seed 20261116 --trials 2 --frames 41 \
  --output /tmp/kinestro-boundary-results --figures /tmp/kinestro-boundary-figures
```

The original 72-point baseline and all nine committed artifacts are preserved from commit `6ac8d9e`. That study used seed `20261115`, six trials and 4,320 primary pose fits. Its original `e1.run` remains available; run it into separate output directories:

```sh
MPLCONFIGDIR=/tmp/kinestro-e1-matplotlib .venv/bin/python -m e1.run \
  --seed 20261115 --trials 6 --output /tmp/kinestro-e1-results \
  --figures /tmp/kinestro-e1-figures
```

Small numerical differences across Python/BLAS/platform versions are possible. Same-environment reproducibility and mathematical tests are checked; this is not a claim of bitwise portability. A different seed/trial count is a new simulation and must not be compared as if it were the committed run. The program never opens a device, network connection, or input-injection interface.

At exact y=0, eigenvector sign and tiny roundoff changes can select a different antipodal branch, producing large differences in the returned position. Exact noiseless boundary flip counts are implementation/platform diagnostics, not universal physical rates. The symmetry, local-rank and observation-only tests do not assume a particular arbitrary sign there.

The original baseline JSON is a historical source-hash snapshot. Re-executing its runner from a package with new companion modules updates that source inventory; use commit `6ac8d9e` for byte-identical historical provenance. The boundary manifest records hashes of all nine preserved baseline artifacts and does not overwrite them.

The boundary study contains 1,152 static observations per source model, 3,936 trajectory observations per source model and 23,409 nonlinear fits including initialization, restart and local-precision diagnostics. Mirrored hypotheses are algebraically equivalent alternatives and are not counted as extra independent solver runs. All 32 current tests cover the original physics and the extension. No physical experiment or E1 completion is claimed.

## Files and boundaries

| File | Purpose |
| --- | --- |
| [e1/model.py](e1/model.py) | Free-space dipole field and finite thin circular transmitter-loop quadrature; configurable moments, origins, RX orientation/axes |
| [e1/geometry.py](e1/geometry.py) | Explicit assumed body sizes, six paired arm poses, waist/chest frames, receiver location and orientation |
| [e1/estimation.py](e1/estimation.py) | Measurement-only analytic initialization, nonlinear pose fit, SO(3) attitude metric, locally scaled Jacobian/SVD |
| [e1/run.py](e1/run.py) | Seeded independent-noise and model-mismatch scenarios, ambiguity/initialization/two-receiver diagnostics, aggregates and figures |
| [tests/test_physics.py](tests/test_physics.py) | Independent closed-form limits, scale/rotation/ambiguity invariants, inverse and observability checks |
| [e1/boundary.py](e1/boundary.py), [boundary_run.py](e1/boundary_run.py) | Separate off-body stress fixtures, observation-only strategies, static/temporal comparison and versioned artifacts |
| [tests/test_boundary.py](tests/test_boundary.py) | Mirrored/negative/boundary observations, temporal branch retention and no-truth-input regressions |
| [Boundary manifest](results/boundary-v1/summary.json) | Seeds, fixture definitions, metrics, limitations, current code hashes and preserved baseline artifact hashes |
| [results/summary.json](results/summary.json) | Configuration, library versions, all scenario distributions/failures and ambiguity diagnostics |
| [results/workspace.csv](results/workspace.csv) | All 72 targets, frames, body sizes, receiver/limb coordinates, distances and field scales |
| [results/pose_summary.csv](results/pose_summary.csv), [body_size_summary.csv](results/body_size_summary.csv), [distance_summary.csv](results/distance_summary.csv) | Conditional error/failure distributions instead of only pooled successes |
| [results/observability.csv](results/observability.csv), [finite_field.csv](results/finite_field.csv) | Reduced-axis ranks, scaled conditioning and local precision bounds; finite-model mismatch |

Code, tests, dependency pins, and research ignore rules use `MPL-2.0`. Original documentation and derived synthetic report artifacts use `CC-BY-4.0`; [REUSE.toml](REUSE.toml) narrowly labels generated CSV/JSON/SVG outputs. No external datasets or third-party code are copied. See the repository [licensing policy](../../LICENSE.md).
