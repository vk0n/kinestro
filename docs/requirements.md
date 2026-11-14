<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Requirements

## Concept and product scope

**Cyberdirigokinesis — Natural Spatial Human–Computer Interaction** is the broader concept of controlling digital systems through natural human movements and gestures, encompassing physical movements, spatial positioning, and gestures. **Kinestro — Wearable Spatial Input System** is the specific modular wearable hardware and software project implementing it under the approved [licensing policy](../LICENSE.md).

Voice interaction is a separate, independent concept. Voice recognition and voice command processing are outside Cyberdirigokinesis and are not Kinestro requirements or core subsystems. Any future interoperability with voice-controlled systems is an optional external integration.

## Classification

This is a research baseline, not a validated product specification. Each item uses one of four classifications:

- **D — Confirmed project decision:** established by the owner's foundation brief. Required direction or scope, not demonstrated capability.
- **P — Preliminary design preference:** favored approach or tentative target; subject to evidence and revision.
- **H — Engineering hypothesis:** a falsifiable claim requiring experiment.
- **Q — Open research question:** unresolved choice or missing knowledge.

Accepted [ADRs](adr/README.md) record established project decisions. Proposed engineering details in this document and the architecture remain proposals unless explicitly accepted. No experimental performance results exist yet.

## Functional requirements

| ID | Class | Requirement | Verification intention |
| --- | --- | --- | --- |
| F-01 | D | Include two forearm acquisition/feedback modules, a central wearable reference module, and a required Linux host. | Architecture review; later integrated demonstration |
| F-02 | D | Estimate hand/wrist movement relative to the central wearable, without requiring absolute world coordinates or SLAM. | Reference-frame review; known relative-pose trials |
| F-03 | D | Operate without stationary cameras, external tracking stations, or room-specific infrastructure. | Dependency review; later operation in different rooms |
| F-04 | D | Initially assign fusion, coordinate estimation, recognition, interaction state, cursor/input events, application integration, and feedback orchestration to the Linux host. | Responsibility review; later pipeline traces |
| F-05 | D | Support bidirectional communication: sensor/status data toward the host and feedback/configuration commands toward wearables. | Contract review; later round-trip and link-loss trials |
| F-06 | P | Use BLE for forearm-to-host communication. Protocol, topology, central-module link, rates, and synchronization remain open. | Two-module throughput, timing, and energy measurements |
| F-07 | P | Investigate electromagnetic positioning complemented by IMU measurements as the primary tracking direction. | E1 workspace characterization and later fusion comparison |
| F-08 | D | Explore sEMG for discrete commands, including click and hold intent; continuous force estimation is outside the initial scope. | E3 signal feasibility; later continuous-session command trials |
| F-09 | D | Activate through a raised open hand and provide a distinct deactivation gesture; sustained raised arms must not be required. | Sensing feasibility and later false-activation/fatigue trials |
| F-10 | D | Support position-based arm control and wrist-orientation rate control using a virtual touch plane concept. The algorithm is not fixed. | E2 observability; later mapping comparison |
| F-11 | D | Default to right-hand pointing and left-hand contextual commands/modifiers while allowing role reassignment. | Configuration review; later swapped-role trials |
| F-12 | D | Use haptic feedback as primary confirmation. Support subtle visual state indication without requiring constant device attention. | Later feedback recognition and attention trials |
| F-13 | D | Target a conventional Linux desktop with one or multiple flat displays first. | Later input-adapter and display-transition trials |
| F-14 | P | Investigate optional cameras near the wrists for hand-relative motion. No chest-mounted camera is required. | E2 comparison; power/privacy/occlusion assessment |
| F-15 | D | Keep VR, gaming, and smart-home adapters as future extensions; smart-home connectivity goes through the host. | Boundary review; no initial standalone IoT path |
| F-16 | D | Forearm modules must support battery-powered wearable operation. No battery chemistry, cell, or capacity is selected. | Later untethered operation and power/fault review |

## Non-functional requirements and tentative targets

| ID | Class | Requirement or target | Verification intention |
| --- | --- | --- | --- |
| N-01 | D | Separate acquisition, state estimation, gesture interpretation, interaction policy, and application integration; sensing technologies must be replaceable. | Contract/dependency review |
| N-02 | D | Use a hardware-independent input event model and allow later testing with synthetic or replayed data without wearables. | M3 hardware-free pipeline verification |
| N-03 | P | Aim for approximately 5 cm spatial position accuracy for broad movements and gestures. Workspace, reference point, statistic, and dynamic conditions need agreement. | E1 positional error distribution and coverage report |
| N-04 | D | Seek low perceived latency, smooth tracking, minimal jitter, and reliable relative movement. Numerical budgets are open. | End-to-end timing distributions, static jitter, dynamic lag, and user-task results |
| N-05 | D | Target operation while standing, walking, and sitting. Record posture-specific limitations. | Later posture/transition and incidental-movement trials |
| N-06 | P | Target at most 300 g per forearm module, preferably significantly lighter, with length up to approximately half the forearm. | Weighed complete module, including battery/straps; fit and fatigue assessment |
| N-07 | P | Seek several hours of battery operation; 4–6 hours is aspirational. Duty cycle and whether the target applies equally to every module need owner review. | Per-module average/peak power and measured runtime under a declared workload |
| N-08 | P | Prefer modular, potentially 3D-printed enclosures. | Attachment, fit, serviceability, thermal and mass review |
| N-09 | D | Consider wearable electrical, battery, thermal, electromagnetic, and skin-contact risks before on-body experiments. | Documented hazard review and experiment-specific controls |
| N-10 | D | Measure metallic/conductive-object sensitivity, tracking range, and power. Metal desk/chair compatibility is not fundamental. | E1 controlled environment perturbations |
| N-11 | D | Keep development incremental, research-driven, and measurable; explicitly record uncertainty. | Hypothesis/evidence review at each milestone |
| N-12 | D | Keep technical documentation and code comments in English. Follow the owner-approved MPL-2.0 software/firmware, CERN-OHL-W-2.0 original hardware source, and CC-BY-4.0 documentation policy, with explicit file-level assignments. | Documentation, SPDX, and licensing review; ADR-0006 |

## Hypotheses and unresolved choices

| ID | Class | Statement or question | Research link |
| --- | --- | --- | --- |
| U-01 | H | A wearable electromagnetic generator/receiver arrangement can provide useful body-relative position across the intended two-arm workspace within tolerable power, mass, and distortion limits. | R-01 / E1 |
| U-02 | H | Sufficient hand-relative orientation information can be obtained for smooth fine rate control without large arm movements. | R-02 / E2 |
| U-03 | H | A small discrete sEMG command set can remain distinguishable from rest and incidental movement across postures and repeated donning. | R-03 / E3 |
| U-04 | Q | How are excitation, receiver geometry, orientation ambiguity, sampling synchronization, and interference handled? | R-01, R-04 |
| U-05 | Q | What are the mount position, effective workspace, central-module power/mass budgets, and acceptable body-reference motion? | R-01, R-07 |
| U-06 | Q | What deactivation gesture, clutch/recenter policy, mapping, and display-selection behavior avoid fatigue and unintended actions? | R-05 |
| U-07 | Q | What latency, jitter, false-action, accuracy, and runtime criteria determine progression to integration? | R-04, R-05, owner review |

## Proposed operating safeguards

The following are engineering proposals for later validation, not additions to the owner's established decision set:

- Start inactive. Only deliberate activation enables application output. Keep a host-side manual disable path independent of gesture recognition.
- On stale data, invalid calibration, relevant sensor loss, or disconnection, suppress motion and new commands and release held buttons/modifiers. Recovery requires explicit reactivation. Define timeouts from measured timing, not arbitrary defaults.
- Define partial-module operation explicitly. Losing the contextual hand must not leave a modifier held; the pointing hand must not reuse an old estimate as fresh.
- Validate message versions, device identity, sequence, length, and age. Reject duplicates, malformed commands, and expired feedback. Bound vibration duration locally even if the host disappears.
- Minimize privileges for future input injection and reject unauthenticated control sources. Agree on pairing and configuration ownership before shared-environment trials.

Before on-body work, assess battery charging/protection, fault shutdown, surface temperature, strain relief, pressure/skin irritation, electrode electrical isolation, and electromagnetic exposure/interference, including the need for specialist review around implanted devices. Select applicable limits only after the excitation frequency, field strength, geometry, power system, use conditions, and jurisdiction are known. This baseline claims no certification or compliance.

For human recordings, agree on informed participation, physiological/video data handling, retention, and publication before collection. Keep identifiable recordings outside Git. Initial tests should use fixtures and off-body arrangements wherever the question allows.

## Measurement conventions to settle before claiming success

For N-03, report the Euclidean error of a declared tracked point in the central-reference frame. Receiver position and anatomical wrist/hand position are different: report mounting-offset uncertainty separately. Record ground-truth uncertainty, calibration conditions, workspace coverage, and failure regions. A proposed screening criterion is described in E1; it does not freeze product acceptance.

For N-04, distinguish sample age, transport delay, processing delay, input emission, and visible response. Smoothing may trade jitter for lag. For N-07, include each module's sensing, radio, feedback, processing, excitation where applicable, and conversion losses in the declared workload. Do not infer fine cursor precision from the broad 5 cm position target or extrapolate a brief bench power reading into validated wearable runtime.
