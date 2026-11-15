# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Independent limiting cases and inverse/ambiguity regressions."""

import numpy as np
import pytest
from numpy.testing import assert_allclose
from scipy.spatial.transform import Rotation
from e1.model import MOMENT, MU0, dipole_field, field_matrix, observe, loop_field, finite_triad
from e1.geometry import workspace
from e1.estimation import analytic_seed, estimate, observability, pose_jacobian, orientation_error_deg


def test_axial_equatorial_dipole_and_scaling():
    m = np.array([0., 0., MOMENT])
    a = MU0 * MOMENT / (4 * np.pi * .5**3)
    assert_allclose(dipole_field([0, 0, .5], m), [0, 0, 2 * a], atol=1e-22)
    assert_allclose(dipole_field([.5, 0, 0], m), [0, 0, -a], atol=1e-22)
    p = np.array([.2, .5, -.1])
    assert_allclose(dipole_field(2 * p, m), dipole_field(p, m) / 8, rtol=1e-14)
    assert_allclose(dipole_field(p, 3 * m), 3 * dipole_field(p, m), rtol=1e-14)


def test_antipodal_ambiguity_survives_receiver_rotation():
    p = np.array([.2, .5, -.1])
    r = Rotation.from_rotvec([.4, -.5, .2]).as_matrix()
    assert_allclose(observe(p, r), observe(-p, r), rtol=1e-14)
    assert_allclose(finite_triad(p, r), finite_triad(-p, r), atol=1e-21)


def test_rotation_invariance_and_gram_eigenvalues():
    p = np.array([.2, .5, -.1])
    r = Rotation.from_rotvec([.4, -.5, .2]).as_matrix()
    y = observe(p, r)
    a = MU0 * MOMENT / (4 * np.pi * np.linalg.norm(p)**3)
    assert_allclose(np.linalg.eigvalsh(y.T @ y), a**2 * np.array([1, 1, 4]), rtol=1e-13)
    assert_allclose(np.linalg.norm(y), np.sqrt(6) * a, rtol=1e-14)


@pytest.mark.parametrize('height', [.02, .08, .4])
def test_finite_loop_matches_independent_axis_formula(height):
    radius = .04
    ni = MOMENT / (np.pi * radius**2)
    expected = MU0 * ni * radius**2 / (2 * (radius**2 + height**2)**1.5)
    assert_allclose(loop_field([0, 0, height], [0, 0, 1], radius), [0, 0, expected], rtol=1e-12, atol=1e-20)


def test_quadrature_converges_and_far_field_approaches_dipole():
    p = np.array([.06, .07, .03])
    medium = loop_field(p, [0, 0, 1], .04, segments=128)
    fine = loop_field(p, [0, 0, 1], .04, segments=512)
    assert_allclose(medium, fine, rtol=1e-10)
    errors = []
    for distance in (.2, .4, .8):
        point = [0, 0, distance]
        exact = loop_field(point, [0, 0, 1], .04)
        errors.append(np.linalg.norm(exact - dipole_field(point, [0, 0, MOMENT])) / np.linalg.norm(exact))
    assert errors[0] > errors[1] > errors[2]
    assert errors[-1] < .004


def test_domain_and_nonmutating_normal():
    with pytest.raises(ValueError): dipole_field([0, 0, 0], [0, 0, MOMENT])
    with pytest.raises(ValueError): loop_field([.04, 0, 0], [0, 0, 1], .04)
    with pytest.raises(ValueError): loop_field([0, 0, .2], [0, 0, 0], .04)
    normal = np.array([0., 0., 2.])
    loop_field([0, 0, .2], normal, .04)
    assert_allclose(normal, [0, 0, 2])


def test_inverse_seed_is_truth_independent_and_mirror_fit_is_wrong():
    p = np.array([.2, .5, -.1])
    r = Rotation.from_rotvec([.4, -.5, .2]).as_matrix()
    y = observe(p, r)
    seed = analytic_seed(y)
    result = estimate(y)
    mirrored = estimate(y, initial=(-seed[0], seed[1]))
    assert result.success and mirrored.success
    assert_allclose(result.position, p, atol=1e-9)
    assert orientation_error_deg(result.rotation, r) < 1e-6
    assert_allclose(mirrored.position, -p, atol=1e-9)
    assert mirrored.residual_nt < 1e-6
    assert np.linalg.norm(mirrored.position - p) > 1


def test_observability_full_triad_and_reduced_axis_singularity():
    p = np.array([0., 0., .5])
    assert observability(p, np.eye(3))[0] == 6
    assert observability(p, np.eye(3), np.eye(3)[:2])[0] == 4
    assert observability(p, np.eye(3), np.eye(3)[:1])[0] <= 3


def test_marginal_crlb_matches_analytic_unknown_attitude_case():
    p = np.array([0., 0., 1.])
    _, _, _, covariance = observability(p, np.eye(3))
    a = MU0 * MOMENT / (4 * np.pi)
    assert_allclose(np.diag(covariance) * a**2, [5 / 9, 5 / 9, 1 / 54], rtol=1e-6)


def test_common_gain_is_unobservable_as_seventh_unknown():
    p = np.array([.2, .5, -.1])
    j = pose_jacobian(p, np.eye(3))
    extended = np.column_stack([j, observe(p, np.eye(3)).ravel()])
    assert np.linalg.matrix_rank(extended, tol=np.linalg.norm(extended) * 1e-7) == 6
    gained = estimate(1.1 * observe(p, np.eye(3)))
    assert_allclose(gained.position, p / 1.1**(1/3), atol=1e-9)


def test_workspace_frames_lengths_and_reference_symmetry():
    samples = workspace()
    assert len(samples) == len({s.identity for s in samples}) == 72
    for s in samples:
        assert_allclose(s.rotation.T @ s.rotation, np.eye(3), atol=1e-14)
        assert_allclose(np.linalg.det(s.rotation), 1, atol=1e-14)
        assert_allclose(np.linalg.norm(s.elbow - s.shoulder), .30 * s.scale)
        assert_allclose(np.linalg.norm(s.wrist - s.elbow), .26 * s.scale)
        assert_allclose(s.rotation[:, 2], (s.wrist - s.elbow) / (.26 * s.scale))
        assert s.position[1] > 0  # Explicit hemisphere assumption, not anatomy validation.


def test_displaced_source_breaks_exact_mirror_at_test_pose():
    p = np.array([.2, .5, -.1])
    origins = np.zeros((3, 3))
    origins[0] = [.12, 0, 0]
    difference = np.linalg.norm(observe(p, np.eye(3), origins=origins) - observe(-p, np.eye(3), origins=origins))
    assert difference > 1e-9


def test_two_receivers_do_not_make_common_gain_observable():
    from e1.run import two_receiver_diagnostic
    result = two_receiver_diagnostic(workspace())
    assert result['rank_18x12_independent_pose_jacobian'] == 12
    assert result['rank_18x13_with_unknown_common_gain'] == 12
