# Vision

## Product philosophy

Kinestro is a **Wearable Spatial Input System**, grounded in **Dirigokinesis — Natural Spatial Human–Computer Interaction**. It explores conductor-like control: natural, expressive, precise hand movements that manipulate digital objects and interfaces.

The long-term ambition is to support interaction without traditional physical controllers such as mice and keyboards. The first useful demonstration is a conventional Linux desktop, but the architecture should support more than pointing: contextual commands, two-hand interaction, future VR and gaming, and smart-home integration mediated by the Linux host.

Modularity serves research. A sensor, estimator, gesture method, or application adapter should be replaceable without redefining the entire platform. Comfort and predictable intent matter as much as tracking precision. No sensing feasibility or ergonomic benefit has been established yet.

## Intended experience

1. The user wears a module on each forearm and a central reference module on the body, then calibrates the body-relative workspace and comfortable neutral pose.
2. Raising an open hand, like a conductor preparing an orchestra, activates interaction. Haptic feedback confirms the mode; a subtle visual indicator may reinforce it.
3. The pointing hand uses broad relative arm movement for positioning and small wrist-orientation deviations for cursor velocity. A virtual touch plane relates movement to the flat display surface.
4. Discrete muscle-based gestures may click, hold a button, or issue commands. The contextual hand supplies modifiers, shortcuts, workspace switching, or window management.
5. A separate gesture deactivates interaction and releases held actions. The user can rest their arms during normal use; activation must not require a continuously raised posture.

This is the confirmed interaction intent. The activation detector, deactivation gesture, gesture vocabulary, neutral/recenter behavior, and mapping algorithms are open. Reliable recognition of an open hand is itself a sensing question. Default right-hand pointing and left-hand context must be configurable.

The position and rate modes need a clear policy for selection or combination. Clutching, dead zones, gain curves, rate limits, mode transitions, and prevention of unintended movement require experiments. A virtual touch plane is a conceptual mapping surface, not a requirement for a physical touch surface or external camera. Body-relative coordinates do not automatically establish where a display is; screen association and recalibration remain open.

## Use cases and priorities

| Priority | Scenario | Main question |
| --- | --- | --- |
| Initial | Standing before a large display | Can broad selection and fine pointing remain comfortable and predictable? |
| Initial | Multiple flat displays | How does the user select or traverse displays without cursor jumps? |
| Initial | Sofa use with a computer connected to a television | Can the user control the desktop with supported arms and small movements? |
| Initial | Moving within a room | Can the body-relative reference preserve control while walking, turning, or sitting down? |
| Where feasible | Conventional desk use | How much do nearby conductive or metallic objects affect performance? |
| Future | VR applications and games | Which platform-independent actions and coordinate semantics can be reused? |
| Future | Smart-home control through the Linux host | How do explicit commands map to host-mediated integrations? |

Compatibility with metal desks and chairs is not fundamental to the initial concept. Environmental sensitivity still needs measurement and clear operating limits. Walking use requires distinguishing intended hand action from incidental arm swing, rather than assuming that a body-relative reference removes all motion artifacts.

## Boundaries

The initial design does not require absolute world coordinates, room-scale SLAM, stationary cameras, tracking stations, a chest camera, standalone IoT connectivity, or all computation on microcontrollers. Optional cameras near the wrists may be investigated for hand motion relative to the forearm; they are neither required nor selected.

The central wearable's location is undecided: waist, chest, or a distributed arrangement with waist electronics/batteries and torso coils. Electromagnetic positioning is the preferred research direction, not a proven basis for a product. IMU and sEMG complement the investigation without closing every observability gap.

The foundation succeeds when collaborators can tell what is intended, what is decided, what is uncertain, and which experiment should resolve the next uncertainty. See [requirements](requirements.md) for classifications and [research backlog](research-backlog.md) for the evidence plan.
