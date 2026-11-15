<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Repository instructions

## Purpose and current scope

Kinestro is a documentation-first open-source hardware and software project for a Wearable Spatial Input System implementing Cyberdirigokinesis — Natural Spatial Human–Computer Interaction: controlling digital systems through natural human movements and gestures. Cyberdirigokinesis names the broader interaction paradigm; Kinestro names the specific modular wearable implementation. Read [README.md](README.md), [requirements](docs/requirements.md), [architecture](docs/architecture.md), and the relevant [research items](docs/research-backlog.md) before changing the design.

The foundation task authorizes documentation only. Do not add application code, firmware, Linux drivers, recognition models, build scaffolding, component selections, or empty placeholder directories. Later explicit owner tasks may authorize specific experiments or implementation; keep those changes within their stated scope.

## Preserve the architectural boundaries

- A required Linux host performs fusion, coordinate estimation, gesture interpretation, interaction-state management, input-event generation, application integration, and feedback orchestration.
- The initial Kinestro system has two forearm acquisition/feedback modules and one central wearable reference module.
- Cyberdirigokinesis concerns physical movements, spatial positioning, and gestures. Voice interaction is a separate, independent concept. Do not introduce voice recognition or voice command processing as part of Cyberdirigokinesis or as a Kinestro requirement or core subsystem; interoperability with voice-controlled systems may only be an optional external integration.
- Tracking is body-relative. Do not introduce a dependency on stationary cameras, tracking stations, room infrastructure, world coordinates, or SLAM.
- Keep acquisition, estimation, interpretation, interaction policy, and output adapters separate. Preserve replaceable sensing, configurable hand roles, bidirectional communication, and future hardware-free testing.
- Do not silently promote electromagnetic tracking, BLE details, cameras, mount placement, or any algorithm into proven or final choices.
- A forearm-mounted IMU is not a direct measurement of hand orientation relative to the forearm. Do not hide this observability gap behind filtering or fusion claims.

## Decisions and evidence

Use the four classifications defined in [requirements](docs/requirements.md#classification): confirmed project decision, preliminary design preference, engineering hypothesis, and open research question. A confirmed requirement describes intent, not proof of capability.

Treat 5 cm accuracy, 300 g mass, half-forearm length, and 4–6 hours of operation as tentative targets. Do not invent measured accuracy, latency, runtime, safety compliance, or gesture reliability. New numerical thresholds must identify their rationale and proposal status.

Use stable requirement and research IDs when connecting changes to evidence. For experiments, document the hypothesis, apparatus, controls, calibration, metrics, raw-data provenance, decision criteria, limitations, and next action. Cite primary technical sources near the claims they support. External results do not validate Kinestro.

Update the relevant docs together to prevent contradictions. Record substantive established architecture changes in an ADR, including context, decision, alternatives, consequences, and revisit conditions. Accepted foundation ADRs capture the owner's brief; do not use accepted ADR status for an untested technology hypothesis. Supersede records rather than rewriting their history to hide a change.

## Working conventions

- Technical documentation and code comments must be in English; conversation may follow the owner's language.
- Use focused branches and reviewable pull requests. Preserve unrelated work and do not merge without authorization.
- Keep the repository small. Add files and directories only when they have content and a clear purpose.
- Follow the approved [licensing policy](LICENSE.md) and [ADR-0006](docs/adr/0006-open-source-licensing.md): `MPL-2.0` for Kinestro-authored software/firmware, `CERN-OHL-W-2.0` for original open hardware design sources, and `CC-BY-4.0` for project documentation. Apply the appropriate license explicitly when adding a file; do not imply that a stored license text licenses nonexistent files.
- Add correct `SPDX-License-Identifier` and `SPDX-FileCopyrightText` metadata to all future contributions. Prefer unobtrusive comment headers for Markdown and use adjacent `.license` files or narrow `REUSE.toml` annotations when a file format needs them. Current documentation attribution is owner-confirmed as `2026 Vladyslav Kononiuk`; preserve other contributors' verified notices and use appropriate years without inventing ownership.
- Keep official texts in `LICENSES/` unchanged and preserve third-party notices and applicable licenses. Do not relicense external resources or datasets through a blanket annotation. Datasets and physiological/video recordings require separate licensing, privacy, and consent decisions. Branding has no automatic trademark license. Changes to the approved policy need an explicit owner decision.
- Before a later on-body experiment, address the relevant battery, thermal, electromagnetic, skin-contact, electrical-isolation, and data-consent risks described in the requirements and experiment proposal. Do not claim certification from a bench test.
- Store no participant-identifiable recordings, credentials, or raw physiological data in Git. Agree on consent, retention, and data access before collection or publication.

## Verification and handoff

For documentation changes, check relative links and anchors, Mermaid syntax when a renderer is available, Markdown structure, requirement/ADR consistency, and `git diff --check`. Review all changed files. Do not create a test suite or CI solely to restate prose.

For licensing changes, verify SPDX identifiers and official text integrity, check every project file's license assignment, and run `reuse lint` when available. Report actual results. MPL-2.0 now covers the E1 research code; the owner-requested CERN-OHL-W text remains unused pending hardware sources. Document that exception rather than claiming full compliance or assigning false licenses to silence it.

There are currently no build or application tests. State which documentation checks actually ran and whether the architecture diagram was rendered. Future implementation tasks should add only checks appropriate to their behavior and scope.

Report changed files, architectural effects, unresolved questions, evidence or checks, and owner decisions needed. For foundation work, include the priority order of the first three experiments. Prepare a PR when repository access supports it; report the precise limitation if it does not.
