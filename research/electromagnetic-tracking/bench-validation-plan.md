<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# E1 off-body bench validation plan

**Status: proposed; not performed.** This plan tests the numerical assumptions against laboratory evidence. It requires no human participants, wearable trial, purchases, or production component selection. It extends the existing [E1 baseline](../../docs/research-backlog.md#e1--off-body-electromagnetic-workspace-and-distortion-characterization); E1 remains open until physical measurements and model comparison are reviewed.

The [physical POC research outline](physical-poc/README.md) adds the owner's visual references, a concept-art audit, corrected antipodal geometry and staged research questions. The illustrations do not establish apparatus availability or capability.

## Question and provisional configuration

Can a characterized, practically sized transmitter and two independently oriented receivers yield useful position estimates over the declared waist/chest interaction envelopes, with approximately 5 cm accuracy, acceptable failures, and credible power/timing?

Start with three identified, approximately co-centered orthogonal **air-core transmitter windings**, a coherent AC current reference, and two triaxial receivers on separate fixtures. A generic 40 mm mean radius, 100 turns, 0.1 A RMS active-axis current and 10 kHz carrier are calculation references from [power feasibility](power-feasibility.md), not a construction specification or authority to energize a coil at those settings. Determine actual safe apparatus limits first; record every departure from the numerical reference.

Sequential axis excitation is the first simple channel-separation experiment. Start with wired timing and acquisition so radio uncertainty does not obscure field physics. Test receiver loading with both receivers present. Add a spatially separated, mechanically referenced transmitter only as a comparison experiment if the co-centered configuration's global ambiguity cannot be resolved over the intended workspace. No recommendation here approves a Kinestro tracking architecture.

## Required capabilities

| Capability | Purpose and qualification |
| --- | --- |
| Current-limited source/driver, waveform generator, calibrated current shunt, oscilloscope | Measure actual RMS/peak current, frequency, polarity, harmonic content, settling, and fault behavior; do not infer moment from a requested DAC value |
| Three receiver axes with accessible calibrated raw output | Record field-proportional signals or induced voltage, clipping, noise, and cross-axis transfer; characterize bandwidth and gain/phase |
| Synchronous multichannel acquisition plus reference channel | Preserve six receiver channels and transmitter reference timing; simultaneous acquisition or measured interchannel skew |
| LCR/impedance measurement and DMM | Measure winding resistance, inductance, mutual coupling, parasitics, and temperature drift |
| Nonconductive translation/orientation fixtures and independent metrology | Position and orient both receivers without nearby metal stages; locate actual sensor centers and transmitter centers |
| Power meter and temperature measurement | Record driver input energy, coil current, driver/coil hot spots, ambient temperature, and warm-up behavior |
| Characterized ferromagnetic and conductive samples; controllable electronics | Separate baseline, distortion, and interference conditions; record material and geometry rather than label all objects simply “metal” |

Use independently characterized laboratory reference metrology; it is not a runtime infrastructure dependency. Independently establish metrology uncertainty and fixture repeatability. Proposed screening goals are expanded position uncertainty no more than 5 mm and angular uncertainty no more than 1°; these are **test-apparatus proposals**, not achieved specifications. A 5 mm position budget reserves 10% of the preliminary 5 cm target for reference uncertainty. If unavailable, report the actual uncertainty and whether the tracker error can be meaningfully separated from it.

## Calibration and evaluation sequence

1. **Freeze the manifest:** record coil geometry/centers, receiver-axis locations, coordinate transforms, apparatus identifiers, firmware/acquisition versions where relevant, waveform and current conventions, filter response/noise bandwidth, timing, ambient conditions, and the exact simulator configuration/commit. Use the numerical research coordinate conventions unchanged and mark all transforms explicitly.
2. **Baseline characterization:** with excitation off, record each receiver's spectrum, noise versus observation time, offsets, channel covariance, electronics interference, and sensitivity to cable routing. With excitation on, measure reference current, all channels' complex gain, clipping margin, harmonic leakage, loading and cross-axis coupling. Measure field-current proportionality at several currents within reviewed limits.
3. **Calibrate on a separate set:** determine actual coil moments, axis nonorthogonality, receiver gains/polarities/phases, offsets and rigid mounting transforms. Use positions and rotations that are not later scored. Record fit residuals and metrology uncertainty. Do not calibrate away a test object's distortion using evaluation data.
4. **Static evaluation:** replay the simulator's labelled body-size, waist/chest, arm-rest, raised, forward/lateral, near-torso and crossed-arm targets using off-body fixtures. Preserve target IDs. Add deliberate mirrored $+\mathbf r/-\mathbf r$ targets to expose the co-centered model's hemisphere ambiguity; assess wrong-branch estimates separately from local precision.
5. **Systematic geometry grid:** supplement anatomical points with assumed radii 0.15, 0.25, 0.40, 0.60, 0.80 and 1.00 m where physically accessible. At each radius sample at least the six cardinal directions plus non-axis-aligned directions, with receiver orientations spanning all axes rather than only pointing at the source. Near-field samples challenge the dipole approximation; far samples challenge SNR. These are characterization samples, not a claim that every direction is anatomically reachable.
6. **Repeatability and time:** randomize evaluation order; perform at least three independently re-mounted calibration/evaluation runs as an initial proposal. Record stationary time series and repeatable translation/rotation trajectories with known timing. Measure the separate effects of averaging, sequential-axis motion skew, pose update rate, sample age and estimator time. A laboratory cursor is unnecessary for this physics gate.
7. **Two-receiver trials:** hold one receiver fixed while moving/rotating the other, then move both independently including close/crossed positions. Compare one-receiver and two-receiver observations with identical excitation. Test clock offset/drift, dropped acquisition blocks, reconnect/reset epochs and staggered samples without silently filling gaps as fresh data.

Pre-register repetitions, hold-out targets, and condition grouping before collection. Three remounts are an initial reproducibility screen, not enough to guarantee a statistically precise 95th percentile. Choose the final sample count and uncertainty interval from pilot variability and the intended decision.

The [boundary-v1 validation](simulation-results.md#boundary-and-hemisphere-validation-boundary-v1) adds an explicit prerequisite: include its separately labelled off-body [negative/near-zero/positive-y fixtures](results/boundary-v1/workspace.csv), crossings in both directions, motion on the plane, changing attitude, and unknown-state restart. Compare uninterrupted continuation with reacquisition from the same recorded observations. Preserve both co-centered hypotheses rather than choosing the one nearest metrology truth. Prioritize a calibrated spatially separated source comparison and alternative-pose residual margins; do not infer absolute sign reliability from local precision, low residuals or smooth paths. These remain proposed bench procedures, not completed physical work or selected hardware.

## Distortion, interference, and power experiments

Run clean-baseline versus perturbation comparisons at matched poses. Use separate ferromagnetic steel, a predominantly nonmagnetic conductor such as copper/aluminum, and nearby powered electronics. Record dimensions, thickness, orientation, distance, placement relative to source/receiver, power state, excitation frequency, and repeat sequence. Sweep object distances without promising any metal-clearance value in advance. Record complex in-phase/quadrature observations: eddy-current phase change can help diagnose distortion but does not automatically correct it.

Test ordinary ambient interference, deliberate controlled near-carrier interference, cable motion, current-reference error, gain drift, and sensor-axis mounting changes. Identify which conditions introduce bias, correlated errors, phase drift, amplitude loss, saturation or dropped data. Include repeated no-object baselines to detect drift. Do not infer ferromagnetic or conductive-object errors from the simulator's independent Gaussian-noise sweep.

At each candidate current/frequency/duty sequence, measure actual DC input power, coil current/voltage, driver losses, warm-up, settling, coil/driver surface temperatures and fault shutdown. Report averages and peaks. Test spatially separated transmitter mutual coupling and receiver loading if that variant is built. A successful finite-coil model comparison still leaves enclosure thermals, battery runtime, body loading, and radio energy unvalidated.

## Data and reporting

Use a private or project-approved data location for raw recordings; commit only small derived tables/figures and reproducible analysis. No participant information is needed. For each acquisition block preserve:

- Run/condition/target/receiver IDs; monotonic timestamps, clock domains and sequence numbers; excitation axis/frequency and reference phase.
- Raw receiver channels, reference current/waveform or calibrated reference samples, units, gain range, saturation flags, filter/integration settings, actual sample rate and channel skew.
- Independent ground-truth position/orientation and uncertainty; complete frame transforms; calibration identity; apparatus/environment/object metadata; supply power and temperatures where recorded.
- Estimated pose and quality, residual, branch/initialization, convergence status, rejected/dropout reason, and processing duration. Preserve failures and negative results.

Report Euclidean receiver-center position error median/95th percentile/worst, orientation error where estimated, workspace coverage, wrong-branch and optimizer-failure rates, static jitter, dynamic lag, current/energy, uncertainty and calibration repeatability. Count invalid/excluded poses against attempted coverage rather than improving error statistics by dropping them. Report per-receiver, per-placement, per-body-size, range and interference-condition results; disclose finite sample counts and uncertainty on percentiles. Anatomical hand/wrist offset is a separate future uncertainty, not included in a receiver-center accuracy claim.

## Continue/revise criteria

Before the bench run, agree on the intended operational workspace, ambiguity strategy and failure-rate ceiling. The existing E1 proposal uses approximately **5 cm at the 95th percentile** of position error over that declared workspace, with coverage and failures reported separately. It is a research screening criterion, not frozen product acceptance.

**Continue** toward a more integrated proof of concept only if independently held-out clean-baseline data meets the agreed accuracy/coverage criteria for both receivers, the estimate's branch is known or reliably detected, measured field/noise/timing agree sufficiently with the model, and measured power/thermal behavior supports a credible wearable budget. Define that budget and acceptable mismatch from metrology/calibration uncertainties before judging success.

**Revise** geometry, sensing, calibration or excitation if local accuracy is promising but range, ambiguity, drift, finite-coil mismatch or energy dominates. **Reject the tested configuration** if the useful workspace cannot be observed robustly within feasible size/power, or only succeeds through undocumented hemisphere assumptions or evaluation-data calibration. Reconsider electromagnetic tracking if repeated physically credible variants cannot provide the required envelope without unacceptable restrictions. A commercial tracker or ideal-noise simulation alone cannot pass this gate.

## Safety review before energizing

Keep the first stage entirely off-body. Review current limiting, isolation, wiring strain relief, fusing/fault shutdown, accessible conductor/driver voltage, stored resonant energy, coil temperature, nearby conductive heating, and interference with laboratory electronics. Set hardware-specific stop conditions before running; no safe numerical voltage, temperature or exposure limit is asserted by this plan. Establish a controlled fixture zone and suitable field measurements; do not infer operator exposure solely from a far-field receiver value.

The exposure assessment must review the applicable jurisdiction and waveform, including harmonics and nonuniform close-to-source fields. Relevant primary starting points are [ICNIRP low-frequency guidelines (2010, 1 Hz–100 kHz)](https://www.icnirp.org/en/publications/article/lf-gdl-2010.html), [ICNIRP RF guidelines (2020, 100 kHz–300 GHz)](https://www.icnirp.org/en/publications/article/rf-guidelines-2020.html), [IEEE C95.1-2019](https://standards.ieee.org/ieee/80/4940/), and [IEC 62311:2019](https://webstore.iec.ch/en/publication/33985). The 2020 ICNIRP publication supersedes the 100 kHz–10 MHz part of the 2010 guidance; do not combine obsolete limits. IEC 62311 supplies assessment methods when no dedicated product standard applies, rather than a universal exposure limit. Device/implant interference needs separate review: general exposure guidance does not establish implant compatibility. These references are a review list, not a declaration of applicability, legal compliance, certification, or permission for on-body experiments.
