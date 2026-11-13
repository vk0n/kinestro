# ADR-0003: Modular pipeline and hardware-independent events

- Date: 2026-11-13
- Status: Accepted
- Basis: Owner's project foundation brief
- Requirements: N-01, N-02, N-11, F-11

## Context

Magnetic, inertial, muscle, and optional camera sensing are under investigation. Application behavior should not be tied to a sensor brand, packet layout, or recognition technique.

## Decision

Separate sensor acquisition, state estimation, gesture interpretation, interaction policy, and application integration. Use a hardware-independent input-event boundary. Preserve replaceable sensing, configurable hand roles, bidirectional feedback, and the ability to test future software without physical hardware through synthetic/replayed observations.

## Alternatives

A direct sensor-to-cursor pipeline is smaller initially but couples acquisition to policy and makes sensing comparisons and failure reproduction harder. A separate distributed service for every boundary is not required; these are logical boundaries, not a mandate for process or deployment complexity.

## Consequences

Future contracts need units, frames, timestamps, validity/quality, discrete press/release/cancel lifecycles, and feedback semantics. Exact schemas, languages, libraries, serialization, and test tooling are deferred. The foundation adds no implementation or placeholder packages.

## Revisit conditions

Refine contracts through research and replay evidence. Change boundaries only when measured complexity or performance justifies it; preserve the ability to compare sensing approaches and reproduce failures.
