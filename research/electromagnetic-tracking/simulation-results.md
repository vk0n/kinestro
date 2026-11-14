<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Synthetic simulation results

**Evidence class: SIMULATED throughout. No physical measurements were performed.** These are conditional results for the source, geometry, calibration, noise and branch assumptions below, not a sensor specification or validated Kinestro performance. See [reproduction instructions](README.md#reproduce), the [model/derivation](feasibility-report.md), and the machine-readable [summary](results/summary.json).

## Method, parameters, and denominators

The committed run uses seed **20261115**, CPython 3.14.7, NumPy 2.5.4, SciPy 1.18.1, and Matplotlib 3.11.2. Source-module SHA-256 hashes are recorded in the JSON. It evaluates **4,320 primary pose fits**, plus 24 random-initialization fits and specific ambiguity diagnostics. No observed failures are removed before computing error distributions.

| Input | Value and convention |
| --- | --- |
| Baseline source | Three co-centered orthogonal identified states; each moment $m=100\pi(0.04)^2(0.1)=0.0502655$ A·m² RMS |
| Field and receiver | Free-space dipole; 3 signed calibrated RX axes; local-to-reference rotation $R$; observation $R^TB$ |
| Workspace | 72 points: 3 assumed size scales × 6 paired arm configurations × 2 hands × 2 source placements; see [geometry](e1/geometry.py) and [full target CSV](results/workspace.csv) |
| Coordinate frame | Waist origin, +x right, +y forward, +z up; source-relative positions in metres; orientation perturbations in radians |
| Noise | Independent zero-mean Gaussian per signed matrix entry, post-demodulation field-equivalent RMS: 0, 0.1, 1, 10, 100 nT; no measured bandwidth/spectrum implied |
| Monte Carlo | 6 independent noise/random-roll trials per point per noise level: 432 fits/level; 216 per mount; each body-scale/mount stratum has 72 |
| Roll | Uniform local RX roll in $[-\pi,\pi]$; full-triad rotational norm invariance is checked separately |
| Initialization | Analytic seed from the observation only, choosing positive reference y; this is an explicit hemisphere prior. No truth-seeded Monte Carlo fits |
| Inverse | SciPy bounded trust-region-reflective least squares (`trf`); ±2 m numerical position box, unrestricted rotation-vector parameters, 180 maximum evaluations, 1 nT residual scaling; tolerances $10^{-10}$ |
| Model mismatch | Finite TX loops, gains, nonorthogonality, source offset and sequential motion described below; the inverse remains an ideal point dipole |
| Statistics | Euclidean receiver-center position error; geodesic SO(3) attitude error; median/P95/worst, optimizer status, ≤5 cm fraction, and wrong-lobe fraction |

The positive-y restriction is only used to choose the seed, not imposed as a solver bound. `antipodal_lobe_fraction` counts $\hat{\mathbf p}\cdot\mathbf p_{true}<0$, a **truth-dependent offline diagnostic**, not a runtime confidence test. A separate negative-y fraction tests the stated hemisphere. Noise can select a mirror-like lobe near the y=0 boundary even while the estimated y remains positive. Local fit residual and solver status cannot reliably detect this.

The [official SciPy least-squares documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) describes the bounded local solver and its termination criteria. We explicitly select `trf`; a returned success flag establishes numerical termination, not global uniqueness.

The equal-moment analytic initializer is evaluated against independent random noise, independent receiver roll, and finite/corrupted forward observations. There is no fitted calibration dataset or parameter tuning on the evaluation targets. This is stronger than noiseless self-inversion, but still a simulation with known calibration conventions. It is not population-level validation.

Reported evaluation counts are SciPy's `nfev`, which excludes calls used for numerical Jacobian estimation. They are not wall-clock latency, sensor acquisition counts, or an achieved update rate.

## Workspace and signals

![Assumed two-arm waist/chest workspace with field scale](figures/workspace.svg)

| Mount | Distance range | Minimum dipole scale $a$ | Important limitation |
| --- | --- | --- | --- |
| Waist | 0.1893–0.9544 m | 5.78 nT RMS | Lateral/extended arms create weak, branch-sensitive observations |
| Chest | 0.1149–0.7847 m | 10.40 nT RMS | Shorter worst-case distance, but closest positions challenge finite-coil approximation and dynamic range |

Here $a=\mu_0m/(4\pi r^3)$; the full matrix norm is $\sqrt6a$. Individual projected channels can approach zero. With all calibrated axes and isotropic noise, a rigid RX rotation changes those entries but not the norm or ideal local information. The receiver remains a point sample, not a finite-area pickup.

Both hands include rest, raised, forward, lateral, near-torso and crossed poses. These are assumed static configurations, not measured walking/seated kinematics. All 72 nominal targets are evaluated; the ≤5 cm fraction describes sampled **attempts**, not continuous workspace volume or a guarantee between points. Anatomical wrist/hand offsets, skin/mount slip and fine wrist movement are not measured by this model.

## Noise sweep

Each row pools 432 attempts. Noiseless inversion recovers the declared branch to numerical precision; it is a consistency test, not a performance result.

| Noise [nT RMS/entry] | Pooled median [cm] | Pooled P95 [cm] | Waist P95 [cm] | Chest P95 [cm] | Attempts ≤5 cm | Antipodal lobe |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.044 | 1.18 | 1.59 | 0.54 | 100% | 0% |
| 1 | 0.457 | 10.21 | 11.48 | 5.32 | 82.64% | 1.16% |
| 10 | 5.01 | 127.24 | 137.65 | 111.05 | 50.00% | 12.04% |
| 100 | 35.32 | 102.80 | 108.81 | 86.27 | 24.07% | 20.60% |

**All these optimizers reported success.** Numerical termination therefore fails as a proxy for the proposed accuracy screen. The 10/100 nT results are severely nonlinear, with spurious solutions and branch errors; the nonmonotone P95 at extreme noise does not mean that adding noise improves tracking. P95 attitude error rises from approximately 1.67° at 0.1 nT to 14.64°, 146.37° and 172.16° at the higher levels. Worst errors, residuals, and counts are retained in the JSON.

At 1 nT, P95 for assumed body scales 0.85/1/1.15 is **7.04/10.42/18.77 cm at waist** and **2.80/4.39/13.04 cm at chest**. Different ranges and rare wrong-lobe fits affect these pooled body-size results. They are not evidence of a demographic effect. [Body-size](results/body_size_summary.csv), [pose](results/pose_summary.csv), and [distance](results/distance_summary.csv) tables retain their individual denominators. The farthest chest bin has only 12 trials and a 25% wrong-lobe fraction: its P95 is particularly unstable.

![Synthetic field, noise sensitivity, and finite-model mismatch](figures/sensitivity.svg)

The three finite-model curves overlap when plotted against distance/radius: at fixed moment the dimensionless thin-loop approximation error depends on that ratio, not the absolute radius. This is a model-scaling result, not three independent physical measurements.

## Forward-model and calibration mismatch

The following scenarios each use 72 targets, one random RX roll per target, and **zero added random measurement noise** to isolate their effects. These are synthetic sensitivity scenarios, not estimates of manufacturing tolerance or real metal distortion.

| Perturbation applied only in forward model | Pooled position P95 [cm] | P95 attitude error [degrees] |
| --- | --- | --- |
| Common TX gain +1% / +5% / +10% | 0.28 / 1.35 / 2.62 | approximately zero |
| First TX moment rotated 2° about reference z | 2.22 | 3.35 |
| RX gains [1.03, 0.97, 1] | 1.83 | 4.72 |
| First RX axis tilted 2° toward local second axis | 1.12 | 3.42 |
| Rigid RX-frame rotation 2° | numerical position precision | 2.00 |
| First source center shifted +5 mm in reference x | 0.94 | 4.75 |
| Sequential states span 10 ms, +y translation at 1 m/s | 1.72 | 11.71 |
| Finite transmitter radius 2 / 4 / 8 cm, same moment | 0.42 / 1.66 / 6.74 | 2.72 / 10.61 / 40.62 |

Common gain is an undetectable range-scale bias in the ideal model, with near-zero fitting residual. A rigid RX rotation is absorbed into estimated attitude and does not imitate nonorthogonality. Finite transmitter geometry is significant for the closest chest targets; increasing radius at fixed moment changes geometry and winding requirements together, not free signal gain. The exact axes, signs and perturbations are in [run.py](e1/run.py); finite-field quadrature accuracy is tested independently from dipole mismatch.

Two moment sweeps with the **correct moment supplied to the inverse** use 432 noisy trials each at 1 nT. Halving the moment yields pooled P95 **57.11 cm** with **4.63%** wrong-lobe fits; doubling it yields **5.98 cm** with **0.46%** wrong-lobe fits. These use different random draws and do not establish a precise current threshold or monotone probabilistic guarantee. Stronger excitation cannot resolve the exact co-centered symmetry or systematic field distortion.

A combined held-out sensitivity case uses finite 4 cm transmitter loops, common gain +5%, RX gains [1.03, 0.97, 1], and 1 nT random noise. Across 432 attempts its pooled median/P95 is **1.73/12.59 cm**, and **2.08%** of estimates are on the opposite lobe. Separate favorable single-error scenarios are therefore insufficient to claim the target.

## Observability, ambiguity, and initialization failures

Numerical rank uses relative singular-value threshold $10^{-7}$; derivatives use centered $10^{-5}$ perturbations of 1 m translation and 1 rad **local** rotation coordinates. Finite-difference roundoff is not interpreted as a new observable state. Among the 72 nominal geometries, one RX axis has rank 3, two axes happen to have rank 6, and full triads have rank 6. Two-axis condition numbers span approximately 22–769 under the declared scaling, versus 12–91 for full triads. These dimensioned/scaled comparisons are not direct error estimates.

The deliberate aligned radial-z diagnostic has **rank 4 with two RX axes** and **rank 6 with three**. Thus the absence of singular points in a sparse anatomical sample would not justify saying six channels always recover six DoF. Ideal local covariance for the full triad matches the independent analytical diagonal $(5/9,5/9,1/54)(\sigma_B r/a)^2$, but that calculation omits all global branch errors and bias.

At test position (0.22, 0.43, 0.17) m, the ideal antipodal observation difference is zero. Fitting from the mirrored initialization yields **1.024 m position error** with approximately $1.7\times10^{-14}$ nT RMS residual. Centered finite loops preserve the symmetry to quadrature precision. Across 24 arbitrary noiseless initializations, 24 optimizers terminate successfully; 12 recover the intended position within 5 cm and 24 reach one of the two antipodal positions within 5 cm. These are explicit alternative solutions, not noise or unexplained implementation failures.

Moving one source center +0.12 m in x produces a nonzero approximately **43.39 nT** same-attitude mirror difference at this one pose. With the displaced observations themselves supplying the approximate analytic seed, the positive start recovers the pose. The negative start still reaches a wrong local minimum approximately **0.920 m** away, with only **1.21 nT** RMS residual after adjusting attitude. This is an **initialization/local-minimum failure** retained as evidence. Breaking one exact symmetry does not prove robust branch discrimination at 1 nT, global uniqueness, or coverage for that layout.

The ideal two-receiver joint Jacobian has rank **12 for 12 pose states** from 18 observations. Adding a common unknown source gain gives 13 states but still rank **12**, consistent with the scale ambiguity. Passive receivers do not interfere in this model by construction; no measured coupling, scheduling, radio or clock behavior is implied.

## Interpretation and limits

The preliminary 5 cm screen is plausible **in favorable synthetic conditions**, including the assumed 0.1 nT regime. It is not robustly met over this assumed workspace at 1 nT, and the actual attainable field noise versus update rate is unknown. Chest placement improves range in the selected body model but also emphasizes close-field model error; no mounting decision follows.

Six noise trials per point and one roll per mismatch point provide screening-level empirical percentiles, not confidence intervals or a reliable extreme-error probability. Results depend on the assumed pose distribution and branch prior. No saturation, colored/coherent interference, source-current fluctuations, thermal drift, receive-coil flux integration, receiver loading, mutual coupling, metal fields, human motion, BLE timing, fusion or display latency is modeled. A scalar field-noise number cannot establish the acquisition time needed to achieve it.

Model equations, limiting cases, calibration variants, branch tests and independent forward-model cases explain the recorded failures; no unexplained solver-status failures occurred in this run. The reference-frame attitude is receiver attitude, not hand articulation. Figures and summaries are small reproducible synthetic report artifacts; raw Monte Carlo draws are regenerated from the seed rather than committed. Use the [off-body bench plan](bench-validation-plan.md) to determine whether the assumptions are physically attainable. E1 remains open.
