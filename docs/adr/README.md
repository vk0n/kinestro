# Architecture decision records

These records capture established direction from the owner's foundation brief. **Accepted** means a project decision is established, not that engineering feasibility is proven. All initial records are dated 2026-11-13.

| Record | Status | Decision |
| --- | --- | --- |
| [0001](0001-linux-host-and-module-boundaries.md) | Accepted | Required Linux host and three wearable modules; host-centered initial processing |
| [0002](0002-body-relative-tracking.md) | Accepted | Body-relative tracking without runtime room infrastructure |
| [0003](0003-modular-pipeline-and-input-events.md) | Accepted | Replaceable sensing, separated processing, hardware-independent events, and future hardware-free testing |
| [0004](0004-desktop-first-interaction.md) | Accepted | Linux desktop first, configurable hand roles, and explicit interaction activation/deactivation |
| [0005](0005-documentation-first-and-license-deferral.md) | Accepted | Documentation-first foundation; evidence before hardware commitments; owner-selected licensing |

Electromagnetic positioning, BLE, mounting location, optional cameras, component choices, algorithms, event schemas, and numerical acceptance budgets are not accepted implementation decisions. Track them in [requirements](../requirements.md) and [research backlog](../research-backlog.md) until evidence and owner review support a decision.

For future ADRs use a sequential number, descriptive filename, date, status (Proposed, Accepted, Superseded, or Rejected), context, decision, alternatives, consequences, and revisit conditions. Link affected requirements and evidence. Preserve superseded history and link the replacement record. A later owner task may explicitly change scope; this index is not an approval barrier to authorized work.
