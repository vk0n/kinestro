# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Local least squares and local tangent-space observability, not global proof."""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
from .model import MOMENT, MU0, field_matrix, observe


@dataclass
class Estimate:
    position: np.ndarray
    rotation: np.ndarray
    success: bool
    evaluations: int
    residual_nt: float


def analytic_seed(measurement, moment=MOMENT, hemisphere=1):
    """Equal-moment full-triad seed; choose ±y branch WITHOUT synthetic truth."""
    y = np.asarray(measurement)
    if y.shape != (3, 3):
        raise ValueError('Analytic seed requires three TX and three RX axes')
    _, vectors = np.linalg.eigh(y.T @ y)
    direction = vectors[:, -1]
    if hemisphere * direction[1] < 0:
        direction = -direction
    strength = np.linalg.norm(y) / np.sqrt(6)
    distance = (MU0 * moment / (4 * np.pi * max(strength, 1e-30)))**(1 / 3)
    position = distance * direction
    reference = field_matrix(position, moments=moment * np.eye(3))
    rotation_t = y @ np.linalg.inv(reference)
    u, _, vt = np.linalg.svd(rotation_t)
    projected = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
    return position, projected.T


def estimate(measurement, initial=None, moment=MOMENT, origins=None, max_nfev=180):
    """Unconstrained-hemisphere fit, bounded to a declared ±2m numerical box.

    No ground-truth seed by default. Positive-y branch is an explicit prior,
    not a guarantee: optimization/noise may move across the hemisphere.
    """
    y = np.asarray(measurement)
    p0, r0 = analytic_seed(y, moment) if initial is None else initial
    initial_state = np.r_[np.clip(p0, -1.95, 1.95), Rotation.from_matrix(r0).as_rotvec()]

    def residual(x):
        p = x[:3]
        if np.linalg.norm(p) < 1e-7:
            return np.full(y.size, 1e12)
        prediction = observe(p, Rotation.from_rotvec(x[3:]).as_matrix(),
                             origins=origins, moments=moment * np.eye(3))
        return ((prediction - y) / 1e-9).ravel()

    result = least_squares(residual, initial_state,
                           method='trf',
                           bounds=(np.r_[[-2.] * 3, [-np.inf] * 3],
                                   np.r_[[2.] * 3, [np.inf] * 3]),
                           x_scale=np.array([0.5] * 3 + [1.] * 3),
                           max_nfev=max_nfev, ftol=1e-10, xtol=1e-10, gtol=1e-10)
    return Estimate(result.x[:3], Rotation.from_rotvec(result.x[3:]).as_matrix(),
                    bool(result.success), result.nfev,
                    float(np.sqrt(np.mean(result.fun**2))))


def pose_jacobian(position, rotation, axes=None, origins=None, moment=MOMENT):
    """Derivative w.r.t. 1m translations and 1rad LOCAL receiver rotations.

    Explicit scaling makes singular values comparable; no rotvec chart
    singularity is introduced. Units T per normalized state coordinate.
    """
    h = 1e-5
    columns = []
    for axis in np.eye(3):
        delta = h * axis
        columns.append((observe(position + delta, rotation, axes, origins, moment * np.eye(3))
                        - observe(position - delta, rotation, axes, origins, moment * np.eye(3))) / (2 * h))
    for axis in np.eye(3):
        plus = rotation @ Rotation.from_rotvec(h * axis).as_matrix()
        minus = rotation @ Rotation.from_rotvec(-h * axis).as_matrix()
        columns.append((observe(position, plus, axes, origins, moment * np.eye(3))
                        - observe(position, minus, axes, origins, moment * np.eye(3))) / (2 * h))
    return np.column_stack([c.ravel() for c in columns])


def observability(position, rotation, axes=None, origins=None):
    j = pose_jacobian(position, rotation, axes, origins)
    singular = np.linalg.svd(j, compute_uv=False)
    rank = int(np.sum(singular > singular[0] * 1e-7))
    condition = float(singular[0] / singular[-1]) if rank == 6 else None
    # Ideal local marginalized positional CRLB, NOT accuracy/uniqueness bound.
    _, values, vt = np.linalg.svd(j, full_matrices=False)
    covariance_per_tesla2 = ((vt.T / values**2) @ vt)[:3, :3] if rank == 6 else None
    return rank, condition, singular, covariance_per_tesla2


def orientation_error_deg(estimated, truth):
    return float(np.degrees(Rotation.from_matrix(estimated.T @ truth).magnitude()))
