# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""SI free-space dipole and thin circular-loop Biot–Savart models.

Fields/moments are signed coherent RMS amplitudes, not total ambient field.
Receiver rotation maps local receiver coordinates into reference coordinates.
"""

import numpy as np

MU0 = 4e-7 * np.pi  # Engineering approximation; adequate at modeled precision.
MOMENT = 100 * np.pi * 0.04**2 * 0.1  # A m², illustrative RMS moment per axis.


def dipole_field(position, moment):
    """B [T] at position [m] relative to one point moment [A m²]."""
    p = np.asarray(position, dtype=float)
    m = np.asarray(moment, dtype=float)
    r = np.linalg.norm(p, axis=-1, keepdims=True)
    if np.any(r <= 1e-9):
        raise ValueError('Point-dipole field is undefined at the source')
    n = p / r
    return MU0 / (4 * np.pi) * (3 * n * np.sum(n * m, axis=-1, keepdims=True) - m) / r**3


def field_matrix(position, origins=None, moments=None):
    """Return reference-frame B columns for separately identified TX states."""
    moments = MOMENT * np.eye(3) if moments is None else np.asarray(moments)
    origins = np.zeros((moments.shape[1], 3)) if origins is None else np.asarray(origins)
    return np.column_stack([dipole_field(np.asarray(position) - o, m)
                            for o, m in zip(origins, moments.T, strict=True)])


def observe(position, rotation, axes=None, origins=None, moments=None):
    """Signed field-equivalent observation [T], RX rows by TX-state columns."""
    axes = np.eye(3) if axes is None else np.asarray(axes)
    return axes @ np.asarray(rotation).T @ field_matrix(position, origins, moments)


def loop_field(position, normal, radius, moment=MOMENT, segments=256):
    """Periodic midpoint quadrature of a thin circular winding with fixed moment.

    N*I = moment/(pi*radius²). No winding thickness, core, conductor, receiver
    area, or induced-current interactions. Points on/very near wire excluded.
    """
    if radius <= 0 or segments < 16:
        raise ValueError('Positive radius and at least 16 segments required')
    normal = np.array(normal, dtype=float, copy=True)
    length = np.linalg.norm(normal)
    if not np.isfinite(length) or length <= 0:
        raise ValueError('Finite nonzero loop normal required')
    normal /= length
    point = np.asarray(position, dtype=float)
    height = np.dot(point, normal)
    rho = np.linalg.norm(point - height * normal)
    if np.hypot(rho - radius, height) < radius * 1e-6:
        raise ValueError('Observation too close to ideal thin wire')
    helper = np.eye(3)[np.argmin(abs(normal))]
    u = np.cross(normal, helper)
    u /= np.linalg.norm(u)
    v = np.cross(normal, u)
    angle = (np.arange(segments) + 0.5) * 2 * np.pi / segments
    wire = radius * (np.cos(angle)[:, None] * u + np.sin(angle)[:, None] * v)
    dl = radius * 2 * np.pi / segments * (-np.sin(angle)[:, None] * u + np.cos(angle)[:, None] * v)
    d = np.asarray(position) - wire
    distance = np.linalg.norm(d, axis=1)
    if np.any(distance < radius * 1e-6):
        raise ValueError('Observation too close to ideal thin wire')
    ni = moment / (np.pi * radius**2)
    return MU0 * ni / (4 * np.pi) * np.sum(np.cross(dl, d) / distance[:, None]**3, axis=0)


def finite_triad(position, rotation, radius=0.04, moment=MOMENT, segments=256):
    fields = np.column_stack([loop_field(position, n, radius, moment, segments)
                              for n in np.eye(3)])
    return np.asarray(rotation).T @ fields
