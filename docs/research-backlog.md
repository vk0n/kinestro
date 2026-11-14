<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Research backlog and milestones

All items below are **open**, and all experiments are **proposals, not executed work**. Priority reflects uncertainty and dependency rather than a procurement order. No components, implementation, model training, or human data collection are authorized by this documentation foundation.

## Prioritized research questions

| ID | Priority | Question and decision unlocked | Proposed evidence | Requirements |
| --- | --- | --- | --- | --- |
| R-01 | P0 | Can wearable electromagnetic tracking observe both arms across a useful workspace within power, distortion, and mounting constraints? | E1; characterize receiver geometry, pose ambiguity, reference movement, and environmental sensitivity | F-02, F-07, N-03, N-10, U-01 |
| R-02 | P0 | What actually observes wrist/hand motion relative to the forearm, including activation posture? | E2; compare forearm-only observation with independent hand sensing and optional camera/sEMG evidence | F-09, F-10, U-02 |
| R-03 | P0 | Is a small discrete sEMG vocabulary distinguishable across rest, posture changes, and repeated donning? | E3 signal study; later continuous-session recognition validation | F-08, U-03 |
| R-04 | P1 | Can two forearm streams, reference timing, and feedback coexist with acceptable latency and energy cost? | Declare channels/rates, compute a preliminary traffic budget, then measure concurrent streams, clock drift, packet gaps, and feedback contention | F-05, F-06, N-04, N-07 |
| R-05 | P1 | Which activation/deactivation and position/rate/virtual-plane policies avoid fatigue and unintended input? | Later user-task comparison of mapping variants, neutral/recenter/clutch rules, sofa posture, monitor transitions, and walking | F-09–F-13, N-04, N-05 |
| R-06 | P1 | Which Linux integration paths satisfy session permissions and desktop/application behavior? | Later isolated adapter trial; pointer/hold/release, shortcuts, multiple displays, disconnect, and manual disable | F-13, N-02 |
| R-07 | P1 | Which central mount and complete-module form factor meet comfort, mass, power, thermal, and serviceability goals? | Compare waist/chest/distributed reference placement; mock-up fit; per-module energy and fault review | N-06–N-09, U-05 |
| R-08 | P2 | What calibration/replay/data contracts support repeatable multi-session research? | Calibration repeatability, versioned metadata, opt-in capture/replay, quality labels, and privacy plan | N-01, N-02, N-11 |
| R-09 | P2 | Which future application abstractions generalize to VR, gaming, and host-mediated smart homes? | Review event semantics after desktop evidence; defer standalone connectivity | F-15 |

P0 questions are feasibility blockers for the desired interaction. Safety and data controls are prerequisites wherever relevant, irrespective of priority. R-08's minimal metadata and calibration conventions are needed from the first experiment; its later tooling can wait.

## First three experiments

The order below prioritizes the largest architecture risks. E2 can be planned while E1 runs; E3 should reuse E2's wrist/posture labels. Apparatus selection and any implementation belong to later explicit tasks. Start with available or borrowed laboratory equipment where appropriate without treating it as a production component decision.

### E1 — Off-body electromagnetic workspace and distortion characterization

**Priority 1. Hypothesis:** U-01. A candidate excitation/receiver geometry provides sufficiently observable, repeatable position over the proposed body-relative two-arm workspace without an obviously incompatible power requirement.

**Method:**

1. Agree on the workspace envelope and tracked point, representative arm poses, mounting candidates, excitation settings, and screening criterion before measurements. Draw both-arm coverage, including crossed/near-body poses. Establish apparatus limits and an off-body electrical/thermal/field review before energizing the setup.
2. Use a nonconductive fixture with independently measured receiver positions/orientations and stated ground-truth uncertainty. Any stationary metrology used here is laboratory reference equipment, not a runtime dependency of Kinestro.
3. Record stationary grid points and repeatable motion paths. Vary receiver orientation independently of position to expose ambiguities and blind regions. Repeat calibration/placement rather than reporting only the best fit. Keep evaluation poses separate from calibration poses.
4. Compare baseline conditions against controlled metallic/conductive objects and representative nearby powered electronics. Record object material, position, and distance; characterize limitations instead of assuming universal compatibility.
5. Repeat with relative motion of the reference fixture and two receivers. Record excitation timing and simultaneous receiver acquisition constraints. Evaluate generator/receiver/electronics average and peak power, plus settling/lag; do not extrapolate unmeasured wearable runtime.

**Metrics:** Full workspace coverage and dropout/ambiguity map; Euclidean positional error median, 95th percentile, and worst observed value; static jitter; dynamic lag and sample age; calibration repeatability; orientation dependence; power and temperature observations. Separate sensor error, anatomical mounting-offset uncertainty, and metrology uncertainty. Record raw signals as well as derived estimates when available.

**Proposed decision rule:** Use approximately 5 cm at the 95th percentile of positional error as an initial screening proposal over a declared workspace, with failures and coverage reported separately. This percentile makes tail error visible instead of relying on mean error alone; it is an engineering proposal for owner review, not part of the original confirmed requirement. Also require an observable solution over the agreed poses and a credible per-module energy/mass budget; their numerical limits remain to be agreed. Averages over easy points must not hide unusable regions.

**Decision consequence:** Proceed to wearable/fusion investigation only with a documented viable envelope and uncertainty. Otherwise narrow the envelope, change geometry/excitation/receiver approach, or reopen the tracking preference. Results from commercial or laboratory apparatus alone do not prove a low-cost wearable implementation; identify which constraints remain untested.

**Deliverable:** A reproducible setup description, calibration/evaluation separation, raw-data manifest, error/coverage/power report, limitations, and a recommendation to continue, revise, or reject the tested configuration. A negative result is useful evidence.

### E2 — Wrist-motion observability and fine-control feasibility

**Priority 2. Hypothesis:** U-02. The sensing arrangement provides a usable independent wrist/hand signal for small rate-control movements without requiring whole-arm movement.

**Method:**

1. Begin with a segmented mechanical fixture: hold the forearm segment fixed and vary the hand segment through labelled flexion/extension and radial/ulnar deviation. Separately vary forearm pronation/supination and whole-arm orientation. Use independent angular reference measurements with uncertainty.
2. Compare the forearm-only observations with candidate extra hand/wrist sensing or optional wrist-camera observations. Include sensor mounting shift and, for cameras, occlusion/lighting cases. Avoid counting an external ground-truth sensor as part of the tested wearable solution unless explicitly proposed as such.
3. After relevant on-body controls and participation/data arrangements, repeat comfortable neutral/small-motion poses with supported and unsupported arms, seated and standing. Label raised open hand versus similar non-activation postures to identify whether activation is observable.
4. Compare distinguishability, neutral repeatability, noise, delay, coverage, and calibration burden before selecting a rate-control signal. sEMG correlation may be explored later with E3, but it must not be treated as a direct joint-angle measurement.

**Metrics:** Reference-relative angular error where a candidate estimates angle; observable degrees of freedom; signal response with fixed forearm; cross-talk from whole-arm motion; neutral drift/jitter; occlusion/failure rate; latency; calibration effort; qualitative comfort and effort. Report unsupported axes as unobserved rather than filling them with assumed estimates.

**Proposed decision rule:** Advance a candidate only if the intended wrist motions produce reproducible distinguishable observations while a fixed forearm and incidental arm movements are appropriately separated. Fine-control angular resolution, lag, and task thresholds must be agreed after a pilot; no numerical precision is claimed now. An observed anatomical limitation can reject forearm-only sensing without a cursor demonstration.

**Decision consequence:** Select a sensing direction for later comparison, change the rate-control concept, or explicitly limit supported motions. If none supplies a usable independent signal, keep wrist control an unresolved requirement; do not disguise arm orientation as measured wrist flexion.

**Deliverable:** An observability matrix by motion and sensing arrangement, reference-labelled traces, failures, ergonomic notes, and the next sensing/mapping decision. A future cursor task can compare throughput, overshoot, neutral stability, clutch frequency, and fatigue after the signal is established.

### E3 — Discrete sEMG signal feasibility across posture and donning

**Priority 3. Hypothesis:** U-03. A deliberately small candidate command set provides repeatable signal separation from rest and incidental activity across repeated wear.

**Method:**

1. Establish skin-contact/electrical-isolation controls, participation consent, and a private data-retention plan before recording. Candidate apparatus is not a production electrode/ADC choice.
2. Define a small provisional set including rest, a possible click command, and a possible hold/release command. They are experimental labels, not the final gesture vocabulary. Record intentional commands alongside walking-like arm movement, reaching, posture changes, and relaxed non-command intervals.
3. Label command onset/offset, forearm orientation, hand pose, session, placement, and repeated donning. Repeat after removal/reapplication and on separate sessions; state participant coverage and do not generalize a single-person pilot to all users.
4. Inspect signal quality, clipping, motion artifacts, onset/offset visibility, and simple feature separation. The first study does not require building a recognizer. If later separately authorized, a baseline classifier must be evaluated on held-out sessions/donnings rather than random overlapping windows from the same recording.

**Metrics:** Signal/contact quality, artifact rate, trial-to-trial and session-to-session variability, command/rest overlap, apparent onset/offset delay, and usable coverage. Later continuous recognition should report per-command precision/recall and confusion, false commands per idle duration, missed releases, held-state errors, and decision latency. Signal separation alone is not a measured false-click rate.

**Proposed decision rule:** Continue toward a minimal vocabulary only when both command transitions and sustained holds are distinguishable from realistic negatives across repeated donning. Otherwise reduce/change the vocabulary, investigate placement/calibration, or reopen the sensing approach. Set quantitative false-action, missed-release, and latency limits before later continuous evaluation.

**Decision consequence:** Choose the next discrete-command research scope and calibration burden. Keep continuous muscle-force estimation outside the initial scope. Do not claim desktop command reliability from cued isolated trials.

**Deliverable:** Label protocol, private recording manifest, signal-quality/separability report, confounds, and a recommendation on vocabulary and future recognition evaluation. Publish only data covered by explicit consent and agreed licensing.

## Evidence and milestone gates

For each future experiment record its date, operator, research/requirement IDs, hypothesis, apparatus/configuration versions, calibration, repetitions and sampling plan, ground truth and uncertainty, conditions, raw-data location/access, analysis method, results including failures, limitations, and decision. Separate measured outcomes from simulation and literature. Leave participant identifiers and raw physiological/video recordings outside Git.

| Milestone | Dependencies | Exit evidence and next decision |
| --- | --- | --- |
| M0 — Foundation | Owner brief | Linked vision/requirements/architecture/backlog/ADRs; uncertainties explicit; reviewable branch and PR. Owner review remains separate from preparation. |
| M1 — Tracking and wrist feasibility | E1, E2 | Declared workspace/error/energy limits and observability report; viable sensing path or explicit architectural revision. No integration gate passes solely on enthusiasm. |
| M2 — Discrete commands and interaction | E3 and R-05, informed by M1 | Minimal command and activation/deactivation candidates, negative-activity evidence, mapping comparisons, comfort notes, and proposed quantitative acceptance budgets |
| M3 — Host contract validation | Separately authorized implementation; enough M1/M2 evidence to define contracts | Hardware-free replay/synthetic tests demonstrate time/quality handling, event order, role reassignment, deactivation, held-action cancellation, feedback expiry, and selected Linux adapter behavior |
| M4 — Integrated wearable research prototype | Evidence-based component selection, energy/mass budget, on-body safety review, M3 | Two forearm modules plus central wearable and host tested across standing/seated/walking use; measured latency, error, runtime, false actions, and limitations against agreed criteria |

Planning and contract research may overlap, but hardware integration should not bypass unresolved feasibility or safety gates. Failure should change a hypothesis or requirement through review, not be relabelled a success. No dates, purchases, components, or implementation stack are committed here.

## Assumptions and choices for owner review

- **Licensing and data:** Software/firmware (MPL-2.0), original hardware design sources (CERN-OHL-W-2.0), and documentation (CC-BY-4.0) are approved in [ADR-0006](adr/0006-open-source-licensing.md). Any publishable dataset or physiological/video recording still requires separate licensing, privacy, and consent decisions; external materials retain their applicable licenses.
- **Tracking envelope:** Agree on practical hand-to-reference distances and poses, receiver versus anatomical reference point, and E1's proposed 95th-percentile interpretation of the approximate 5 cm target.
- **Budgets:** Define tolerable latency, jitter, false actions, missed releases, complete-module mass/comfort, and the central module's mass/power envelope. Confirm how the aspirational 4–6-hour runtime applies to each module and workload.
- **Mounting and interaction:** No waist/chest/distributed mount is selected. Approve trial variants, deactivation candidates, neutral/recenter behavior, and supported/raised-arm comfort tasks.
- **Prototype safeguards:** Review inactive startup, manual host disable, release-on-loss, and explicit reactivation as proposed operating policy. These were added as engineering proposals, not claimed as decisions in the brief.
- **Trials and resources:** Agree on available/borrowed apparatus, experiment budget, participant coverage, safety review responsibility, private recording storage, consent, and retention before collection. A solo pilot is assumed to be exploratory, not representative evidence.

## Initial technical references

These sources motivate research design; none validates Kinestro or selects a component. Links were checked on 2026-11-13.

- [NDI — How Electromagnetic Tracking Works](https://www.ndigital.com/wp-content/uploads/2021/11/DOC-10007384-Rev001-How-EM-Works-Infographic-Web.pdf): manufacturer explanation of a varying-field generator/receiver architecture. Use as a principle reference; its clinical system is not evidence for the proposed wearable constraints.
- [Miljković and Isaković — Effect of the sEMG electrode (re)placement and feature set size on the hand movement recognition](https://arxiv.org/abs/2005.02105v2): original study of electrode repositioning and retraining. It motivates repeated-donning evaluation rather than guarantees robustness for Kinestro.
- [Rumman et al. — FORS-EMG](https://arxiv.org/abs/2409.07484v2): original dataset study across forearm orientations. It motivates posture-conditioned recording and evaluation; its published recognition results are not project targets or measurements.
- [Linux kernel — uinput](https://docs.kernel.org/input/uinput.html): official userspace virtual-input interface documentation, relevant to R-06. Backend selection and desktop/session behavior remain to be tested.
