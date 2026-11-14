<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# ADR-0005: Documentation-first foundation and owner-selected licensing

- Date: 2026-11-13
- Status: Partially superseded by [ADR-0006](0006-open-source-licensing.md) for licensing deferral; documentation-first direction remains accepted
- Basis: Owner's project foundation brief
- Requirements: N-09, N-11, N-12

Historical record: the context and decision below describe the original 2026-11-13 deferral. The owner has since approved the licenses recorded in ADR-0006 and [LICENSE.md](../../LICENSE.md). Only the licensing deferral is superseded; the documentation-first and evidence-before-hardware decisions remain in effect.

## Context

Core feasibility, component suitability, performance, and wearable risks are unresolved. Kinestro intends open-source hardware/software development, but the owner has not chosen licenses.

## Decision

Make the initial repository documentation-first: vision, requirements, conceptual architecture, research experiments, and established decisions. Explicitly distinguish confirmed decisions, preliminary preferences, hypotheses, and open questions. Add no application code, firmware, drivers, recognition model, component commitments, or empty placeholder directories in the foundation. Keep technical documentation and code comments in English.

Leave software, hardware, and documentation license choices pending an explicit owner decision. Do not create a license file or imply that public visibility grants a selected license.

## Alternatives

Immediate implementation, component procurement, or selecting a conventional license by default would turn untested assumptions or an undecided ownership choice into project commitments.

## Consequences

The first milestone provides an actionable evidence plan, not a running prototype. Future explicit tasks may authorize experiments and implementation incrementally. Experiments need relevant wearable-safety and data-handling preparation. Performance targets remain targets until measured; literature is motivation rather than validation.

## Revisit conditions

The owner may authorize later research/implementation tasks and explicitly select licenses. Record substantive resulting architecture decisions with linked evidence. Document licensing choices before adding license files or asserting reuse terms.
