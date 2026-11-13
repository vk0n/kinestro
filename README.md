# Kinestro

**Wearable Spatial Input System** · **Research foundation; no prototype validated**

Kinestro explores **Dirigokinesis — Natural Spatial Human–Computer Interaction**: conductor-like hand movements, body-relative spatial tracking, and muscle-based gestures for interacting with digital environments. The ambition is a modular input platform that can grow from Linux desktops to VR, gaming, and smart-home integration through a Linux host.

Natural, expressive control is the product goal. Cursor control is the first application, rather than the limit of the platform.

## Initial concept

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

## Contributing and licensing

Start with the requirements and research backlog. Propose a measurable question, method, and decision consequence before adding implementation or selecting hardware. Keep technical documentation and code comments in English. Record evidence and limitations; distinguish literature results from Kinestro measurements.

Kinestro is intended to become an open-source hardware and software project. **Software, hardware, and documentation license choices are pending an explicit owner decision.** No license is selected or granted by this foundation; no `LICENSE` file is introduced.
