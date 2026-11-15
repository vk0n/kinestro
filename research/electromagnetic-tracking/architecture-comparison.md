<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Electromagnetic architecture comparison

**Status: research comparison and laboratory recommendation only.** No tracking architecture, component, or operating frequency is approved by this document. Physical measurements on Kinestro hardware have not been performed. See the [reference register](references.md) for sources, dates, evidence classes, and published-system limitations.

## Measurements and necessary assumptions

For a calibrated point-dipole source at the origin, define

$$
A(\mathbf r)=\frac{\mu_0}{4\pi\|\mathbf r\|^3}(3\hat{\mathbf r}\hat{\mathbf r}^{T}-I).
$$

With known transmitter moments in matrix $M$, receiver-to-reference rotation $R$, and three calibrated receiver axes, the signed channel matrix is $H=R^{T}A(\mathbf r)M$. There are nine scalar observations from three independent excitations. A sinusoidal pickup measures induced voltage; conversion to this field-equivalent representation requires frequency, pickup area/turns, gain, polarity and phase calibration. A magnetometer must instead have suitable bandwidth/noise for the excitation. Three nominally orthogonal coils alone do not establish any of those conditions. This coupling approach follows [Raab et al.](https://ohiostate.pressbooks.pub/app/uploads/sites/45/2020/01/raabetal.pdf).

The following are **analytical deductions for the ideal calibrated model**:

- A six-parameter rigid pose needs at least six independent local scalar constraints; merely counting channels does not prove Jacobian rank or global uniqueness. Unknown gains, coil positions or moments add nuisance parameters.
- One single-axis pickup sees its axis direction but not rotation about that axis: at most five pose degrees of freedom. Three excitations provide only three scalars and cannot recover an unconstrained five-dimensional state. Additional spatially different fields or a justified orientation prior are needed. Anser's eight-source/single-pickup arrangement is a concrete five-DoF example. [Cavaliere et al.](https://www.mdpi.com/1424-8220/21/8/2822)
- Two nonparallel receiver axes and three independent source excitations yield six observations, a necessary count for six DoF, but singular geometry and discrete ambiguities still require analysis. Three receiver axes provide redundancy and simplify calibration/consistency checks.
- Co-located dipoles satisfy $A(-\mathbf r)=A(\mathbf r)$. The two positions are indistinguishable even if an optimizer converges and the local pose Jacobian has full rank. A hemisphere restriction is additional information, not a field measurement. For equal calibrated orthogonal moments, the squared field matrix determines the radial axis and range, but only the axis **up to sign**. This ambiguity is also identified in [Wahlström et al.](https://arxiv.org/html/1909.08356v1).
- Adding a second independent receiver does not resolve the first receiver's sign ambiguity without an additional valid geometric constraint. It creates two pose-estimation problems sharing the same reference and excitation.

## Candidate arrangements

| Candidate | What is observed; timing and axes | Observability and two-forearm consequences |
| --- | --- | --- |
| A — One co-located triaxial transmitter, triaxial magnetic receivers | Nine signed channels per receiver from three independently labelled excitations; TDM, coherent FDM, or other identifiable patterns. Both receivers listen to the same field. | Six-DoF locally in the calibrated ideal model, with global antipodal ambiguity. Single-axis channel nulls occur with orientation, while the complete ideal triad has no corresponding all-axis null. Both arms require independent calibration/quality handling; listening at two locations does not inherently require doubling TX slots. |
| B — Multiple body-mounted, spatially separated sources | Known source locations/moments and distinct excitation labels provide spatially different observations. Can use triad receivers or sufficiently many scalar pickup observations. | Separation can break co-located inversion symmetry and improve spatial diversity, but not every layout is well-conditioned. If source separation is tiny relative to receiver distance, differences become weak. Body/coil mount movement introduces extrinsic-calibration errors. All sources remain on the body, preserving the runtime infrastructure boundary. |
| C — Role reversal: wrist transmitters, central receiver array | Linear reciprocal inductive coupling permits source/receiver interchange with calibrated gains. Forearm sources need independent time/frequency labels; central array measures each active source. | Relative position remains possible; a single-axis wrist source cannot reveal its roll. Triad wrist transmitters or additional valid orientation observations are needed for full pose. Moves excitation, drive electronics and heat onto forearms; two active sources increase scheduling/cross-coupling concerns. Reciprocity does not make power budgets equal. |
| D — Permanent magnets on forearms, body-mounted magnetic array | Spatial DC field samples; no source excitation timing or pickup voltage from a stationary field. Array estimates dipole location/direction and background field. | Typically five DoF per dipole; roll is absent. Two magnets are superposed without intrinsic frequency labels, complicating identity and crossed-arm association. The [2021 prototype](https://arxiv.org/html/2101.11276v1) demonstrates the principle only in a small eye-scale workspace. |
| E — Pulsed-DC fields and settling-time sampling | Excite sources sequentially, allow relevant transients to settle, measure/integrate appropriate receiver response. Receiver technology and waveform are coupled choices. | May reduce some conductive transient effects; cannot be assumed to remove ferromagnetic distortion. Dead time competes with update rate, and static-field sensors face offset/background issues. The [pulsed-DC patent](https://patents.google.com/patent/US5453686A/en) supplies a disclosed implementation principle, not a numerical wearable guarantee. |

B is supported by the spatially distinct multicoil field generator in [Cavaliere et al.](https://www.mdpi.com/1424-8220/21/8/2822); adapting it to torso mounting is a new engineering hypothesis. C is a reciprocity-based engineering alternative, not a claim that a specific cited device already satisfies Kinestro. TDM can separate source labels but requires accounting for motion between slots; FDM requires amplitude/phase separation, appropriate bandwidth and interference testing. Motion during a transmission is a documented issue in [magneto-inductive navigation](https://arxiv.org/html/1909.08356v1).

## Decision matrix against Kinestro

This matrix is a qualitative engineering assessment. It deliberately has no weighted score; an unknown feasibility constraint cannot be averaged away.

| Criterion | A: central triad | B: separated body sources | C: wrist sources | D: permanent magnets | E: pulsed DC |
| --- | --- | --- | --- | --- | --- |
| Position/pose observability | Local six-DoF; antipodal pair | Potentially resolves ambiguity; layout-dependent | Layout/axis-dependent | Dipole position/direction; roll absent | Depends on source geometry and sampled channels |
| Useful two-arm coverage | Signal decays rapidly with range; measured envelope unknown | Spatial diversity potentially helpful; unknown envelope | Central receive aperture limits coverage; unknown | Arm-scale feasibility unknown | Unknown after settling/noise constraints |
| Accuracy limits | Noise, calibration, finite geometry, field distortion, wrong hemisphere | Same plus source extrinsics | Same plus active-source association/coupling | Ambient gradients, saturation, magnet association, calibration | Offsets, transients, settling, ferromagnetic effects |
| Size/mass | Source triad centrally; sensor triads on arms | More body coils/support/wiring | Drivers/coils on both forearms | Magnets on arms; sensor array centrally | Source/driver/receiver technology-dependent |
| Energy | Central drive and two receiver chains; total unknown | More excitation paths or reduced duty; total unknown | Increased forearm excitation burden; total unknown | No excitation power; receiver/host power unknown | Duty cycle/peak-current/settling tradeoff unknown |
| Receiver complexity | Three calibrated axes, coherent acquisition | More identifiable source channels | Central multichannel array | DC triad array and background estimation | Waveform-specific front end/integration |
| Calibration | Moments, geometry, polarity, gains, timing | A plus inter-source poses and mounting stability | Source identity plus central-array geometry | Array geometry, offsets, moments/background | Step response, offsets and timing plus geometry |
| Metal sensitivity | Requires measurement | Redundancy may detect disagreement; correction unproven | Requires measurement | Static magnetic distortion remains | Conductive improvement conditional; ferro remains |
| Cost/difficulty drivers | Coil manufacture, low-noise front end, timing | Added drivers, mechanics and calibration | Two drive/power chains plus array | Sensor array, calibration and data association | Driver transients and low-offset measurement |

**Recommendation:** use A as the minimum off-body baseline to validate signal levels, phase/polarity, gain calibration and inverse fitting. Include explicit opposite-position tests rather than hiding the symmetry through initialization. In the same fixture, add a known displaced source configuration B to test whether its extra information reliably distinguishes both signs and covers lateral/crossed-arm poses. This is a staged experiment, not approval of A for the final wearable. A tight, physically justified hemisphere restriction might suffice for a deliberately restricted laboratory region; unrestricted body-relative use needs stronger evidence.

Confidence is high that the ideal-model ambiguity must be handled; confidence in wearable energy, environmental robustness and the 5 cm target is low until the [bench plan](bench-validation-plan.md) is executed. Reconsider electromagnetic tracking if a useful two-arm envelope requires unacceptable current/heat/mass, if normal torso/forearm mounting changes defeat calibration, if nearby everyday metal produces undetectable errors above the target, or if ambiguity cannot be resolved without excluding priority use cases. Raising power is not a cure for systematic distortion or missing observability.

## Boundary and hemisphere validation

The original all-positive-y anatomical sample is not evidence that Kinestro can enforce that condition. A y>0 restriction could be acceptable for an explicitly bounded, independently verified laboratory workspace; unrestricted two-arm use needs evidence covering side/back motion, arms resting alongside the body, changes in source mounting, and reacquisition. These are possible challenges to the restriction, not newly measured anatomical postures. The separate [boundary study](simulation-results.md#boundary-and-hemisphere-validation-boundary-v1) labels its stress points as abstract off-body diagnostics rather than modifying the anatomical model.

Temporal continuation supplies history, not an absolute-sign observation. A mirrored trajectory with the same receiver attitude is equally smooth and has identical measurements. Maintaining both hypotheses preserves uncertainty honestly; residuals from a co-centered model cannot select between their exact antipodal pair, including with noise. A failed initial branch choice can remain continuously wrong.

Spatially separated sources should therefore be a priority **comparison in physical validation**, alongside controlled branch initialization and restart tests. The current diagnostic displaces one source by 0.12 m; its observed residual-selection behavior is not proof of uniqueness, sufficient separation, or a final layout. Test noncollinear spatial diversity, calibration stability and alternative-pose margins across the actual intended envelope before selecting hardware.

Other potential information includes an independently registered position/known initialization zone, externally justified kinematic constraints, or an additional body-worn spatial observation. An orientation-only IMU prior cannot distinguish $\mathbf r$ from $-\mathbf r$ when their attitudes are identical. Translational inertial information might help only with a separately justified motion/reference model and its own errors; this study implements no such fusion. Left/right module identity alone is not a proof of spatial side, especially for crossed arms. None of these possibilities is selected or validated here. E1 remains open.
