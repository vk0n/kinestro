<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# ADR-0006: Open-source licensing

- Date: 2026-11-14
- Status: Accepted
- Basis: Owner's explicit licensing policy and documentation attribution confirmation
- Requirements: N-12
- Supersedes: The licensing-deferral portion of [ADR-0005](0005-documentation-first-and-license-deferral.md); its documentation-first and evidence-before-hardware decisions remain accepted

## Context

Kinestro — Wearable Spatial Input System implements Cyberdirigokinesis — Natural Spatial Human–Computer Interaction. The foundation deliberately deferred licensing until an explicit owner decision. The owner has now approved separate licenses for software/firmware, original hardware design sources, and documentation, with the philosophy of openness with reciprocity and permissive documentation reuse with attribution.

The current repository contains documentation only. A policy for future software and hardware must not be confused with an assignment to nonexistent files or with relicensing third-party material.

## Decision

Use the following owner-approved policy:

| Material | License | SPDX identifier |
| --- | --- | --- |
| Kinestro-authored software and firmware | Mozilla Public License 2.0 | `MPL-2.0` |
| Original open hardware design source files | CERN Open Hardware Licence Version 2 — Weakly Reciprocal | `CERN-OHL-W-2.0` |
| Project-authored documentation | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |

Apply CC-BY-4.0 explicitly to current project documentation through Markdown comment headers. Use the owner-confirmed attribution `2026 Vladyslav Kononiuk`; the year reflects the documentation's creation in repository history. Preserve future contributors' own verified notices rather than assigning their rights to the project owner.

Add a [licensing overview](../../LICENSE.md) and the complete, unchanged official texts in `LICENSES/`. Future software/firmware and original hardware source files must receive the relevant SPDX metadata when added; storing the texts does not license future files automatically. Retain third-party licensing and notices. Decide dataset/recording licensing, privacy, and consent separately. No automatic trademark license is granted for project names or branding.

## Rationale

MPL-2.0's file-level reciprocity preserves access to distributed modifications of covered software while allowing integration into larger works with separately licensed files. CERN-OHL-W-2.0 provides weak reciprocity for covered hardware design sources, with Complete Source and Available Component rules that support integration. Commercial use remains possible under each license's conditions.

CC-BY-4.0 makes documentation reusable and adaptable with attribution and change notices, without imposing ShareAlike. This supports dissemination of the research while keeping software and hardware reciprocity scoped to their appropriate artifacts. No extra licensing conditions, non-commercial restrictions, or additional project license options are introduced.

## Alternatives

- Continuing the deferral is no longer appropriate after explicit owner approval.
- Uniform permissive licensing for software and hardware would not express the selected reciprocal policy.
- Strong copyleft or documentation ShareAlike would impose broader reciprocal scope than the owner selected.
- A non-commercial or custom additional restriction would conflict with the approved commercial-use goal and is rejected.
- A blanket repository-wide license or broad future-directory annotations would blur current documentation, future design/code, and third-party/data boundaries. Explicit file-level assignments are clearer at this stage.

## Consequences and obligations

Follow the full texts linked from [LICENSE.md](../../LICENSE.md). In particular, preserve required notices; make MPL-covered source available when distributing covered executables; meet CERN-OHL-W's applicable modified-source and product-conveyance obligations, including required source information; and supply documentation attribution, license information, and change notices when sharing. These summaries add no conditions to the licenses.

The requested inclusion of unused MPL-2.0 and CERN-OHL-W-2.0 texts is a deliberate exception to REUSE Specification 3.3's unused-license rule while there are no software/hardware files. Current project files still receive unambiguous SPDX assignments. Do not claim full REUSE compliance, add dummy files, or mislicense documentation to hide that exception.

No source implementation, hardware commitment, sensor architecture, research hypothesis, roadmap, or performance target changes through this decision. The original licensing deferral remains visible as history in ADR-0005; its documentation-first direction is retained.

## Revisit conditions

Review file-level coverage and REUSE findings when real software, firmware, hardware sources, or external materials are added. Before distributing binaries or hardware, review the applicable source/notice obligations and required source locations. Dataset release needs its own rights and participant-data decisions. Revisit policy only through an explicit owner decision and with regard to existing license grants and contributor rights; do not imply that changing a policy revokes licenses already granted.
