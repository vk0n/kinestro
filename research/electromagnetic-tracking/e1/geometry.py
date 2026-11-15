# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Assumed anatomical sampling, not anthropometric measurements or coverage proof."""

from dataclasses import dataclass
import numpy as np
from scipy.spatial.transform import Rotation


@dataclass(frozen=True)
class Sample:
    identity: str
    scale: float
    pose: str
    hand: str
    mount: str
    shoulder: np.ndarray
    elbow: np.ndarray
    wrist: np.ndarray
    receiver: np.ndarray
    transmitter: np.ndarray
    rotation: np.ndarray

    @property
    def position(self):
        return self.receiver - self.transmitter


def unit(v):
    a = np.asarray(v, dtype=float)
    return a / np.linalg.norm(a)


def receiver_frame(direction, roll=0.0):
    """Local z follows forearm; roll [rad] is independent mounting orientation."""
    z = unit(direction)
    helper = np.eye(3)[np.argmin(abs(z))]
    x = unit(np.cross(helper, z))
    y = np.cross(z, x)
    return np.column_stack((x, y, z)) @ Rotation.from_rotvec([0, 0, roll]).as_matrix()


def workspace():
    """72 labelled points: 3 scales × 6 paired poses × 2 hands × 2 mounts."""
    samples = []
    for scale in (0.85, 1.0, 1.15):
        for side, hand in ((1, 'right'), (-1, 'left')):
            poses = {
                'rest': ([0.06 * side, 0.03, -1], [0.02 * side, 0.08, -1]),
                'raised': ([0.30 * side, 0.6, -0.2], [0, 0.2, 1]),
                'forward': ([0, 1, -0.15], [0, 1, 0.15]),
                'lateral': ([side, 0.12, 0], [side, 0.08, 0]),
                'near_torso': ([0.05 * side, 0.02, -1], [-0.8 * side, 0.45, 0.2]),
                'crossed': ([-0.2 * side, 0.3, -0.95], [-side, 0.3, 0.2]),
            }
            for pose, (upper, forearm) in poses.items():
                shoulder = scale * np.array([0.19 * side, 0.04, 0.5])
                elbow = shoulder + scale * 0.30 * unit(upper)
                wrist = elbow + scale * 0.26 * unit(forearm)
                receiver = elbow + 0.65 * (wrist - elbow)
                for mount, transmitter in (('waist', np.zeros(3)),
                                            ('chest', scale * np.array([0, 0.04, 0.32]))):
                    identity = f'{scale:.2f}-{pose}-{hand}-{mount}'
                    samples.append(Sample(identity, scale, pose, hand, mount, shoulder,
                                          elbow, wrist, receiver, transmitter,
                                          receiver_frame(forearm)))
    return samples
