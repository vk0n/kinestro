<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# ADR-0001: Required Linux host and wearable module boundaries

- Date: 2026-11-13
- Status: Accepted
- Basis: Owner's project foundation brief
- Requirements: F-01, F-04, F-05

## Context

Kinestro combines body-worn acquisition with evolving estimation and interaction research. Initial experiments need a flexible host rather than an assumption that the entire pipeline must fit on microcontrollers.

## Decision

Use two forearm modules, one per arm, and a central wearable reference module with a required Linux host. Wearables primarily acquire/transmit sensor data and execute local feedback. Initially the host performs sensor fusion, coordinate estimation, gesture recognition, interaction-state management, cursor/input generation, application integration, and feedback orchestration. Communication supports messages in both directions.

## Alternatives

All-on-MCU processing is not a project requirement. A hostless wearable or direct standalone IoT design is outside the initial architecture. Local conditioning or later processing migration remains possible when evidence justifies it.

## Consequences

Host links, timestamps, buffering, and failure handling are important system boundaries. Radio topology, software processes/language, and central-module transport remain open. This decision establishes responsibilities without selecting hardware.

## Revisit conditions

Revisit processing placement after measured bandwidth, latency, energy, privacy, or deployment constraints show a need. Changing the required host or module topology needs an explicit architecture review and replacement ADR.
