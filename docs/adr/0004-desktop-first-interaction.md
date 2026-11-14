<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# ADR-0004: Desktop-first interaction with configurable hand roles

- Date: 2026-11-13
- Status: Accepted
- Basis: Owner's project foundation brief
- Requirements: F-08–F-13, F-15

## Context

Kinestro aims at expressive spatial input beyond an alternative mouse. A conventional Linux desktop with one or several flat displays provides the initial interaction target.

## Decision

Start with Linux desktop interaction. Raise an open hand to activate; provide a separate deactivation gesture whose form remains undecided. Do not require continuously raised hands. Default to right-hand cursor control and left-hand context/modifiers, with configurable roles. Explore combined arm-position and wrist-orientation rate control through a virtual touch plane. Initially use sEMG for discrete commands rather than continuous force estimation. Use haptics as primary confirmation, with subtle visual state indication.

Keep VR, gaming, and Linux-host-mediated smart-home integrations as future extensions. Do not add direct standalone IoT connectivity to the first prototype.

## Alternatives

VR-first interaction, a fixed gesture vocabulary, a fixed handedness, or a position-only cursor mapping would prematurely narrow the intended research. Physical mouse emulation alone would not capture the longer-term platform intent.

## Consequences

Wrist sensing, activation observability, deactivation, holds/releases, comfort, mapping gains, monitor selection, and unintended-action prevention need experiments. No interaction algorithm, recognizer, Linux backend, or guaranteed ergonomic benefit is selected. The proposed safe-state policy remains a proposal in the requirements.

## Revisit conditions

Use E2/E3 and later interaction studies to refine sensing, gestures, and mapping. Review any scope change that removes configurable roles, requires sustained arm elevation, or changes the first application target.
