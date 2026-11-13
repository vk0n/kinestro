# ADR-0002: Body-relative tracking without room infrastructure

- Date: 2026-11-13
- Status: Accepted
- Basis: Owner's project foundation brief
- Requirements: F-02, F-03, F-07, N-03, N-05, N-10

## Context

Priority use cases include large displays, sofa use, and movement while standing, walking, or sitting. The system must not depend on a specially equipped room.

## Decision

Track relative to a central wearable reference. Absolute world coordinates and room-scale SLAM are not initial requirements. Do not require stationary cameras, tracking stations, or room-specific infrastructure. A chest-mounted camera is not required.

## Alternatives

World-anchored optical tracking and external base stations could answer different questions but violate the initial runtime boundary. Laboratory ground-truth equipment may be used to evaluate the wearable system without becoming a product dependency.

## Consequences

Electromagnetic tracking complemented by IMU is the preferred research direction, not the accepted solution or a demonstrated 5 cm capability. Mounting location, field geometry, wrist observability, environmental sensitivity, and screen mapping remain open. Body-relative tracking alone does not determine display location or eliminate incidental walking motion. Metal desk/chair compatibility is not fundamental, but operating limitations must be measured.

## Revisit conditions

Use E1/E2 evidence to revise the sensing preference or practical envelope while preserving the infrastructure boundary. Introducing mandatory room infrastructure or world tracking would require an explicit scope change and replacement ADR.
