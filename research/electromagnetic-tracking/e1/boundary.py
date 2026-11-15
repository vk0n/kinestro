# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Boundary fixtures and observation-only ambiguity strategies for E1.

The stress fixtures are abstract off-body positions, not invented anatomy.
Estimator/continuation functions deliberately receive no true position or pose.
"""

from dataclasses import dataclass, replace
import numpy as np
from scipy.spatial.transform import Rotation
from .estimation import analytic_seed, estimate
from .model import observe

Y_OFFSETS = (-.10, -.05, -.02, -.005, 0., .005, .02, .05, .10)
XZ_POINTS = ((.25, .15), (-.25, -.15), (.55, -.25), (-.55, .25))
MOUNTS = {'waist': np.zeros(3), 'chest': np.array([0., .04, .32])}
RX_ROTATIONS = (np.eye(3), Rotation.from_euler('xyz', [35, -25, 70], degrees=True).as_matrix())


@dataclass(frozen=True)
class BoundarySample:
    identity: str
    mirror_id: str
    mount: str
    position: np.ndarray
    rotation: np.ndarray
    transmitter: np.ndarray
    classification: str = 'abstract_off_body_diagnostic'


def boundary_workspace():
    """144 poses; exact antipodal pairs at every orientation and both mounts.

    Same source-relative fixtures under each body mounting transform intentionally
    represent the same free-space physics. They are not anatomical coverage data.
    """
    samples = []
    for mount, source in MOUNTS.items():
        for xz_index, (x, z) in enumerate(XZ_POINTS):
            for y_index, y in enumerate(Y_OFFSETS):
                for rotation_index, rotation in enumerate(RX_ROTATIONS):
                    identity = f'{mount}-xz{xz_index}-y{y_index}-r{rotation_index}'
                    mirror = f'{mount}-xz{xz_index ^ 1}-y{len(Y_OFFSETS)-1-y_index}-r{rotation_index}'
                    samples.append(BoundarySample(identity, mirror, mount, np.array([x, y, z]),
                                                  rotation.copy(), source.copy()))
    return samples


def region(y):
    """Disjoint coarse groups; exact offsets are also reported separately."""
    if abs(y) <= .005 + 1e-12:
        return 'near_zero_abs_y_le_5mm'
    return 'positive_y_gt_5mm' if y > 0 else 'negative_y_lt_minus5mm'


def displaced_origins():
    """Existing diagnostic layout: only the x-directed source shifts +0.12m x."""
    origins = np.zeros((3, 3))
    origins[0] = [.12, 0, 0]
    return origins


def mirrored_estimate(fitted, measurement):
    """Exact equivalent hypothesis of a co-centered fit, even for noisy data.

    This is algebraic duplication, not a second independent optimizer success.
    """
    counterpart = replace(fitted, position=-fitted.position.copy(), rotation=fitted.rotation.copy())
    residual = (observe(counterpart.position, counterpart.rotation) - measurement) / 1e-9
    counterpart.residual_nt = float(np.sqrt(np.mean(residual**2)))
    return counterpart


def co_centered_hypotheses(measurement, initial=None):
    fitted = estimate(measurement, initial=initial)
    return fitted, mirrored_estimate(fitted, measurement)


def displaced_hypotheses(measurement):
    """Two data-derived starts; never use true position, attitude, or branch."""
    p0, r0 = analytic_seed(measurement)
    origins = displaced_origins()
    candidates = (estimate(measurement, initial=(p0, r0), origins=origins),
                  estimate(measurement, initial=(-p0, r0), origins=origins))
    return candidates


def residual_selection(candidates):
    """Prefer converged fits, then smallest observed residual; stable index tie."""
    index = min(range(len(candidates)), key=lambda i: (not candidates[i].success,
                                                      candidates[i].residual_nt, i))
    return index, candidates[index]


def temporal_hypotheses(measurements, initial_hemisphere=1):
    """Continue the previous fitted pose, retaining its exact antipodal partner.

    First-state information is ONLY the declared sign assumption, ±y, applied
    to the analytic observation seed. This is not verification of that sign.
    No per-frame y constraint, sign reset, truth-based gating or motion oracle.
    Opposite-branch continuation is represented by exact symmetry, not a second
    independent information source. On numerical failure the returned estimate
    is retained and used next; failure/recovery is scored by the caller.
    """
    if initial_hemisphere not in (-1, 1):
        raise ValueError('Initial hemisphere must be an explicit +1 or -1 assumption')
    initial = None
    output = []
    for measurement in measurements:
        if initial is None:
            initial = analytic_seed(measurement, hemisphere=initial_hemisphere)
        candidates = co_centered_hypotheses(measurement, initial)
        output.append(candidates)
        initial = (candidates[0].position.copy(), candidates[0].rotation.copy())
    return output


@dataclass(frozen=True)
class Trajectory:
    identity: str
    mount: str
    times_s: np.ndarray
    positions: np.ndarray
    rotations: np.ndarray
    transmitter: np.ndarray
    classification: str = 'abstract_off_body_diagnostic'


def boundary_trajectories(frames=41):
    """Six paths per mount; 25ms synthetic samples, not achieved acquisition rate."""
    if frames < 9 or frames % 2 != 1:
        raise ValueError('Use an odd number of frames, at least 9, to sample y=0')
    t = np.linspace(0, 1, frames)
    y = .12 * (1 - 2 * t)
    for mount, source in MOUNTS.items():
        paths = {
            'positive_to_negative': np.column_stack((np.full(frames, .32), y, np.full(frames, .18))),
            'negative_to_positive': np.column_stack((np.full(frames, .32), -y, np.full(frames, .18))),
            'along_boundary': np.column_stack((.25 + .3 * t, np.zeros(frames), .15 + .03 * np.sin(2*np.pi*t))),
            'near_boundary': np.column_stack((np.full(frames, .42), .002 * np.sin(6*np.pi*t), np.full(frames, .20))),
            'crossing_and_rotation': np.column_stack((.32 + .03 * np.sin(np.pi*t), y, .18 + .04 * np.sin(2*np.pi*t))),
            'far_crossing': np.column_stack((np.full(frames, .8), y, np.full(frames, .3))),
        }
        for name, positions in paths.items():
            rotations = np.repeat(RX_ROTATIONS[1][None, :, :], frames, axis=0)
            if name == 'crossing_and_rotation':
                angles = np.column_stack((.4*np.sin(2*np.pi*t), .5*np.sin(np.pi*t), .8*t))
                rotations = Rotation.from_euler('xyz', angles).as_matrix()
            yield Trajectory(name, mount, np.arange(frames) * .025, positions,
                             rotations, source.copy())
