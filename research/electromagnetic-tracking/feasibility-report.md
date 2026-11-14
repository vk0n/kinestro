<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Electromagnetic tracking feasibility: M1/E1 research phase

## Finding and evidence status

**Proceed to a limited off-body proof of concept, without committing Kinestro to electromagnetic tracking.** Calibrated, phase-signed multiaxis fields are theoretically sufficient for useful local pose estimation. The numerical study also preserves substantial negative results: global position ambiguity, noise-dependent branch errors, calibration-induced bias, finite-coil mismatch, and false confidence from converged optimizers. Wearable engineering feasibility remains unproven.

Use a co-centered triaxial AC source and two triaxial receivers as the simplest **laboratory baseline**, then compare a calibrated displaced-source variant to test ambiguity handling. This recommendation is not an accepted ADR, production topology, operating frequency, component selection, or proof that the preliminary 5 cm target is met. A robust hemisphere strategy or asymmetric geometry is required before unrestricted body-relative operation is credible.

| Evidence class | What exists in this task |
| --- | --- |
| Confirmed project intent | Linux host, two forearm modules and central wearable, body-relative tracking, replaceable sensing; existing ADRs unchanged |
| Assumed/model input | Simplified body dimensions, coil moments/geometries, noiseless free space, Gaussian field noise and imposed calibration defects |
| Theoretical | Dipole equations, signed-channel observability, exact co-centered antipodal symmetry, field/range scaling |
| Simulated | 4,320 noisy/mismatched pose fits, 72 assumed workspace targets, Jacobian diagnostics, and independent limiting-case tests |
| Literature-reported | Manufacturer specifications and academic physical experiments, identified separately in [references](references.md) |
| Experimentally measured by Kinestro | **None.** The [bench plan](bench-validation-plan.md) is proposed and has not been executed. |

The [existing E1 baseline](../../docs/research-backlog.md#e1--off-body-electromagnetic-workspace-and-distortion-characterization) remains the physical gate. This task completes its initial theoretical/numerical investigation, not E1 as a whole.

## Physical model and approximations

Let the reference-frame displacement from a source center to a receiver center be $\mathbf r$, with $r=\|\mathbf r\|$ and $\mathbf n=\mathbf r/r$. A source magnetic moment is $\mathbf m=NI A\hat{\mathbf u}$ in A·m². In free space, the quasistatic point-dipole field is

$$
\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi r^3}
\left[3\mathbf n(\mathbf n^T\mathbf m)-\mathbf m\right].
$$

This is the leading multipole term of a localized current loop, not an accurate arbitrary near-wire model. Field scales linearly with moment and as $r^{-3}$ at fixed direction. On a dipole's axis its amplitude is twice its equatorial amplitude. These relationships underlie the established tracking models in [Raab et al.](references.md#physical-models-and-observability) and [Wahlström et al.](https://arxiv.org/html/1909.08356v1).

For a finite thin circular transmitter winding, the independent evaluation model integrates Biot–Savart:

$$
\mathbf B(\mathbf r)=\frac{\mu_0NI}{4\pi}
\oint\frac{d\boldsymbol\ell\times(\mathbf r-\mathbf r')}{\|\mathbf r-\mathbf r'\|^3}.
$$

The implementation uses periodic midpoint quadrature with 256 elements, a point receiver and fixed moment ($NI=m/(\pi a^2)$). The independent axial limit is $B_z=\mu_0NIa^2/[2(a^2+z^2)^{3/2}]$. The axial finite/dipole ratio is $(1+(a/z)^2)^{-3/2}$: this gives a direct validity check rather than assuming a universal distance cutoff. Tests check this formula, convergence of quadrature, far-field agreement, and exclusion of singular thin-wire positions. Finite transmitter/RX geometry and flux integration matter in real systems; [Cavaliere et al.](https://www.mdpi.com/1424-8220/21/8/2822) explicitly study extended coils. The simulator does not integrate receiver area or a winding pack.

The source's sinusoidal RMS moment is modeled as a phase-referenced signed amplitude. The illustrative 10 kHz frequency enters the separate induced-voltage/power calculation; free-space quasistatic field amplitudes here have no frequency dependence. At 10 kHz the free-space wavelength $c/f$ is approximately 30 km; an approximately 1 m workspace is deeply subwavelength. This is magnetic near-field amplitude/coupling estimation, **not time-of-flight electromagnetic ranging**, and $r^{-3}$ is a small-source approximation within that quasistatic regime. A coil can be too close for the dipole approximation while still deeply quasistatic.

The use of $\mu_0\approx4\pi10^{-7}$ H/m is an engineering approximation. No core, material permeability distribution, skin effect, transmitter back-reaction, receiver loading, RF propagation, saturation, or physiological tissue model is included. Assumed air-core moments do not imply the human body or a room has no effect.

### What a receiver measures

With transmitter moments as columns of $M$, receiver-to-reference rotation $R$, and RX sensitivity-axis rows $P$, the dipole observation is

$$
Y=P R^T\frac{\mu_0}{4\pi r^3}(3\mathbf n\mathbf n^T-I)M.
$$

Three identified source states and a triaxial receiver provide nine signed scalars. For induction coils the direct observable is flux-derived voltage: $v=-d\Phi/dt$, with $\Phi\approx N_r A_r\hat{\mathbf u}_r^T\mathbf B$ only when the field is approximately uniform over the pickup. Thus $|V|_{\rm rms}\approx\omega N_rA_r|B_\perp|_{\rm rms}$; a calibrated phase/gain transformation is needed before treating voltage as the simulator's field-equivalent $Y$. Mutual inductance is $\Phi/I_t$, and reciprocity in the assumed linear reciprocal quasistatic model motivates role reversal; it does not remove power, synchronization, or geometry differences between those implementations.

A field sensor must instead resolve the chosen excitation bandwidth, range, drift and phase. An arbitrary low-cost compass output is not automatically a synchronized field measurement. DC/slow excitation needs ambient-field/offset rejection; AC can separate source channels from ambient DC but introduces frequency-dependent gain, phase, eddy-current and settling issues. Sequential excitation needs a frozen-pose approximation or motion compensation; frequency multiplexing needs separate transfer calibration and enough acquisition bandwidth.

Receiver uncertainty includes winding/resistor and amplifier voltage/current noise, ADC quantization/reference noise, bandwidth/filter delay, timing error, source-current noise, cross-axis calibration, environmental interference and thermal drift. The simulation sweeps **post-demodulation field-equivalent noise** instead of assigning an unselected sensor a fictitious specification. Noise density, integration time and per-frame variance are not interchangeable; obtain the actual spectrum/covariance and effective noise bandwidth on the bench.

## Observability and inverse positioning

For equal, calibrated orthogonal source moments $M=mI$ and a full calibrated RX triad,

$$
Y=R^T A,\quad A=a(3\mathbf n\mathbf n^T-I),\quad
a=\frac{\mu_0m}{4\pi r^3},\quad
Y^TY=a^2(I+3\mathbf n\mathbf n^T).
$$

The Gram eigenvalues are $(4a^2,a^2,a^2)$. Its principal eigenvector gives direction **up to sign**, and $\|Y\|_F=\sqrt6a$ gives range when the moment/gains are known. On a chosen branch, $Y A^{-1}$ gives $R^T$, projected to SO(3) for a noisy initialization. This is our analytic derivation and initialization, checked against invariants and an independent local covariance formula.

Since $A(-\mathbf r)=A(\mathbf r)$, the co-centered model has the same observations at $\mathbf r$ and $-\mathbf r$ with the **same receiver orientation**. Centered finite circular loops preserve that symmetry too. Nine measurements and a full local Jacobian do not establish a unique global pose. Magnitude-only measurements lose still more sign information. A branch prior must be stated and validated, particularly near a hemisphere boundary.

Six independent scalar constraints are necessary for an unconstrained six-state local pose, but six numbers are not sufficient to guarantee rank, conditioning or uniqueness. One RX axis with three source states cannot instantaneously recover an unconstrained 5DoF pickup pose. Two RX axes give six scalars and can have full local rank at generic poses, yet the supplied radial-normal configuration has rank four. A full triad is the more informative laboratory baseline. A single known dipole plus unknown receiver attitude has only three scalars for six states; even known attitude leaves a continuous azimuthal ambiguity in its equatorial plane. See the [architecture comparison](architecture-comparison.md) for alternatives and two-receiver consequences.

The local Jacobian differentiates translations scaled by **1 m** and local SO(3) perturbations scaled by **1 rad**. SVD reports rank and a condition number under those declared units; this is not a scale-free hardware quality score. A local marginalized covariance $(J^TJ)^{-1}\sigma_B^2$ is computed through SVD only for full-rank cases. For a radial coordinate system and unknown RX attitude, its positional diagonal is

$$
\operatorname{diag}\Sigma_p=
\left(\frac{\sigma_B r}{a}\right)^2
\left(\frac59,\frac59,\frac1{54}\right).
$$

This ideal local high-SNR bound predicts transverse sensitivity growing approximately as $r^4\sigma_B/m$. It excludes global branch mistakes, bias, material distortion, unknown gains and unreliable optimizer initialization. A converged fit can therefore disagree with the physical state by approximately twice the range while retaining a tiny residual.

Common unknown source gain and range are inseparable in this model: multiplying the true field by $g$ gives the fitted range $r/g^{1/3}$. The augmented gain-plus-pose Jacobian has rank six for seven unknowns. A rigid RX-frame rotation can be absorbed into fitted attitude, whereas nonorthogonality or unequal gains corrupt the measurement geometry. These effects are tested separately rather than all called “misalignment.”

## Assumed Kinestro geometry and numerical findings

The workspace uses waist origin, right-handed $+x$ to the user's right, $+y$ forward, and $+z$ upward. Chest source position is $(0,0.04,0.32)s$ m; shoulders are $(\pm0.19,0.04,0.50)s$ m; upper arm length is $0.30s$ m, forearm length $0.26s$ m. The RX center lies 65% from elbow to wrist. Uniform body scales $s=0.85,1,1.15$ are **assumptions, not population percentiles or measured anthropometry**.

Six paired limb configurations cover rest, raised interaction, forward extension, lateral extension, near torso and crossed arms. They give 72 receiver targets across both hands and waist/chest configurations, with random receiver roll in noise trials. This is a sparse assumed sampling, not proof of continuous workspace coverage, anatomical comfort, collision-free reachability, or wrist sensing. The [workspace figure](figures/workspace.svg) and [CSV](results/workspace.csv) expose every target and frame.

Calculated distances are **0.189–0.954 m for waist** and **0.115–0.785 m for chest**. At illustrative $m=0.0502655$ A·m² per axis, minimum dipole scale $a$ is 5.78 nT and 10.40 nT respectively; individual channel projections can be zero. The chest arrangement improves worst-case distance in this model, but its closest targets are only 2.87 source radii from a 40 mm source, increasing finite-geometry sensitivity. That tradeoff is not a mounting decision.

Under ideal matched models and the explicit positive-$y$ branch prior, the pooled 3D error P95 is **1.18 cm at 0.1 nT** and **10.21 cm at 1 nT** assumed per-entry noise. At 1 nT the waist and chest P95 are **11.48 cm and 5.32 cm**. Even the latter slightly misses the proposed 5 cm screen; larger noise and wrong-lobe estimates fail more seriously. These are **simulations, not achieved sensing performance**. The complete distributions, finite-model/gain experiments, failure counts and limitations are in [simulation results](simulation-results.md).

Two passive receivers can observe the same source states without allocating another set of transmitter slots in the ideal model. Their independent-pose observation Jacobian is block diagonal with rank 12 for the illustrated 18-scalar system; adding unknown common source gain does not resolve that nuisance state. The numerical targets include both arms, but no receiver loading, mutual coupling, wireless contention, clock drift, or shared calibration covariance is simulated. Hardware must establish these conditions.

## Power, distortion, and remaining engineering limits

The [power analysis](power-feasibility.md) calculates illustrative coil copper dissipation near 0.088 W per active axis and approximately 11 g copper per axis, but winding voltage can be approximately 8.5–11.9 V RMS at 10 kHz under its simplified inductance assumptions. These exclude drivers, losses, enclosure, synchronization, batteries and receiver electronics. Source copper is not total system mass or power, and no 4–6-hour runtime is demonstrated. A 1 nT pickup signal can be sub-microvolt in the illustrative receiver, making gain/phase/noise calibration central to the practical gate.

Ferromagnetic permeability redirects and may hysteretically bias fields; conductors support eddy currents with phase- and geometry-dependent secondary fields. The skin-depth relation $\delta=\sqrt{2/(\omega\mu\sigma)}$ illustrates dependence on frequency, conductivity and permeability, but does not predict position bias for arbitrary objects. Nearby electronics and cables can generate coherent or broadband interference; shared source/receiver circuitry can cross-couple. Source-axis and time-skew simulations are generic sensitivity cases, **not numerical metal-distortion results**. No quantitative metal-clearance or on-body accuracy claim is made. Realistic material effects need measured complex transfer maps or a separately justified electromagnetic material model.

Measured noise versus bandwidth, winding impedance and driver loss, coil/receiver calibration stability, close-range finite geometry, dual-receiver loading/timing, distortion, and operator exposure must be resolved before a wearable build. The [bench plan](bench-validation-plan.md#safety-review-before-energizing) identifies exposure/equipment standards for specialist applicability review. Neither the model nor a successful off-body fit establishes safety, implant compatibility or compliance.

## Minimum evidence before architecture commitment

1. Independently calibrated signed complex measurements across the declared body-relative target grid for **both receivers**, with metrology uncertainty, calibration/evaluation separation, repeated mounting, and retained failure counts.
2. Measured source moment, noise/covariance versus observation bandwidth, field/current linearity, finite-geometry mismatch and phase/timing, explaining whether the simulated low-noise regime is attainable at a useful pose rate.
3. Explicit resolution/detection of hemisphere ambiguity over lateral, near-torso, rest and crossed configurations, comparing a displaced source where needed; small residuals alone cannot pass.
4. Held-out position P95 near the proposed 5 cm screen with agreed coverage/failure limits, plus power, thermal and dimensional budgets credible for each module. Bench screening does not establish wearable ergonomics or battery runtime.
5. Controlled ferromagnetic/conductive/electronic perturbation trials with bounded operating limits and an appropriate safety review before any on-body stage.

Reconsider the tested geometry if the required noise/integration time, ambiguity restrictions, or calibration cannot support this envelope. Reconsider electromagnetic tracking more broadly if physically credible variants require unacceptable source size/energy, restrict ordinary intended arm poses, or remain unpredictably distorted in the priority environments. No alternative sensing technology is selected here. E1 remains open and no existing architecture decision is changed.
