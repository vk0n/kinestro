<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Kinestro

**Wearable Spatial Input System** · **Research foundation; no prototype validated**

Kinestro is an open-source hardware and software project implementing **Cyberdirigokinesis — Natural Spatial Human–Computer Interaction**: controlling digital systems through natural human movements and gestures. Cyberdirigokinesis is a coined term for the broader interaction paradigm of physical movements, spatial positioning, and gestures; Kinestro is its specific modular wearable implementation.

Kinestro explores conductor-like hand movements, body-relative spatial tracking, and muscle-based gestures. The ambition is a modular input platform that can grow from Linux desktops to VR, gaming, and smart-home integration through a Linux host.

Voice interaction is a separate, independent concept. Voice recognition and voice command processing are outside Cyberdirigokinesis and are not Kinestro requirements or core subsystems. Voice-controlled systems may complement Kinestro through optional external integration.

Natural, expressive control is the product goal. Cursor control is the first application, rather than the limit of the platform.

## Initial Kinestro system

- Two forearm modules acquire sensing data and provide haptic feedback.
- A central wearable module provides a body-relative reference; an electromagnetic field generator is the preferred research candidate.
- A required Linux host estimates motion, interprets gestures, manages interaction state, generates input events, and sends feedback commands.
- Operation must be self-contained on the body plus the host, without stationary cameras, tracking stations, or room-specific infrastructure.

The proposed interaction combines broad arm-position control with fine wrist-orientation rate control over a virtual touch plane. Raising an open hand activates interaction; a separate deactivation gesture remains to be defined. Sustained raised arms must not be required. The right hand defaults to pointing and the left to context and modifiers; roles remain configurable. sEMG initially targets discrete commands such as clicks and holds.

## Evidence and status

This repository contains the technical foundation and research plan only. It contains no application code, firmware, drivers, trained recognition model, selected components, or validated performance results.

| Classification | Current position |
| --- | --- |
| Confirmed project decisions | Linux host; two forearm modules plus central wearable; body-relative tracking; modular sensing and hardware-independent events; desktop first |
| Preliminary design preferences | Electromagnetic tracking complemented by IMU; BLE communication; modular, potentially 3D-printed enclosures |
| Engineering hypotheses | Wearable electromagnetic tracking can support the intended workspace; fine wrist control and discrete sEMG commands can be robust and comfortable |
| Open research questions | Tracking observability, range, distortion, power, wrist sensing, latency, gesture vocabulary, mapping, and mounting position |

Approximately **5 cm position accuracy** for broad movements, **300 g maximum target mass per forearm module** (preferably much less), approximately **half-forearm length**, and **4–6 hours of operation** are preliminary or aspirational targets. They are not demonstrated capabilities or frozen acceptance criteria. Fine cursor control needs separate evaluation; broad tracking accuracy does not establish pointing usability.

## Documentation

| Document | Purpose |
| --- | --- |
| [Vision](docs/vision.md) | Product philosophy, interaction, and use cases |
| [Requirements](docs/requirements.md) | Confirmed scope, tentative targets, and verification intentions |
| [Architecture](docs/architecture.md) | Modules, Mermaid diagram, data flow, and conceptual contracts |
| [Research backlog](docs/research-backlog.md) | Priorities, first three experiments, milestones, and owner review items |
| [Architecture decisions](docs/adr/README.md) | Accepted decisions and their rationale |
| [Agent instructions](AGENTS.md) | Guidance for future repository work |

## Research roadmap

| Milestone | Exit evidence |
| --- | --- |
| M0 — Foundation | Coherent vision, requirements, architecture, accepted decisions, and actionable experiment proposals ready for owner review |
| M1 — Feasibility | Body-relative electromagnetic tracking characterized on a bench; wrist observability assessed; sensing alternatives and limits recorded |
| M2 — Interaction evidence | Discrete-command signal feasibility, comfortable activation/deactivation, virtual-plane and rate-control mappings evaluated |
| M3 — Host contract validation | In a separately scoped implementation task, replay/synthetic input exercises estimation boundaries, state handling, feedback, and a Linux input adapter without hardware |
| M4 — Integrated research prototype | Only after evidence-based component selection and safety review: two forearm modules, central wearable, and host evaluated together |

The [first three proposed experiments](docs/research-backlog.md#first-three-experiments) are electromagnetic workspace characterization, wrist-motion observability, and discrete sEMG signal feasibility. No schedule or procurement commitment is implied.

## Contributing

Start with the requirements and research backlog. Propose a measurable question, method, and decision consequence before adding implementation or selecting hardware. Keep technical documentation and code comments in English. Record evidence and limitations; distinguish literature results from Kinestro measurements.

## Licensing

Kinestro follows **openness with reciprocity**: software and firmware use [MPL-2.0](LICENSES/MPL-2.0.txt), original open hardware design sources use [CERN-OHL-W-2.0](LICENSES/CERN-OHL-W-2.0.txt), and project documentation uses [CC-BY-4.0](LICENSES/CC-BY-4.0.txt). Commercial use is permitted under each license's terms.

Current files are documentation licensed through SPDX headers. Software and hardware license texts establish the approved policy; future source files need explicit licensing when added. See [LICENSE.md](LICENSE.md) for scope, attribution, third-party/data exclusions, trademark boundaries, and the current unused-license exception to full REUSE compliance.
