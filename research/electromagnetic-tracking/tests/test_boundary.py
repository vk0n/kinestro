# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Boundary, ambiguity and observation-only temporal regression tests."""

import inspect
import numpy as np
import pytest
from numpy.testing import assert_allclose
from e1.boundary import (boundary_workspace, boundary_trajectories, Y_OFFSETS,
                         co_centered_hypotheses, temporal_hypotheses,
                         displaced_hypotheses, displaced_origins, residual_selection, region)
from e1.model import observe, finite_triad
from e1.estimation import observability


def test_stress_fixture_has_both_signs_exact_plane_mirrors_and_mounts():
    samples = boundary_workspace()
    assert len(samples) == 144
    assert {s.mount for s in samples} == {'waist', 'chest'}
    assert {float(s.position[1]) for s in samples} == set(Y_OFFSETS)
    by_id = {s.identity: s for s in samples}
    assert len(by_id) == 144
    for sample in samples:
        partner = by_id[sample.mirror_id]
        assert_allclose(partner.position, -sample.position, atol=0)
        assert_allclose(partner.rotation, sample.rotation, atol=0)
        assert sample.classification == 'abstract_off_body_diagnostic'
        assert np.linalg.norm(sample.position) > .25
        body_point = sample.position + sample.transmitter
        assert_allclose(body_point - sample.transmitter, sample.position)


@pytest.mark.parametrize('y', [-.1, -.005, 0., .005, .1])
def test_mirrored_measurements_for_negative_boundary_and_positive_y(y):
    p = np.array([.25, y, .15])
    r = boundary_workspace()[1].rotation
    assert_allclose(observe(p, r), observe(-p, r), rtol=1e-14, atol=1e-22)
    assert_allclose(finite_triad(p, r), finite_triad(-p, r), atol=1e-21)
    assert observability(p, r)[0] == 6


def test_y_zero_fit_has_equivalent_pair_without_asserting_arbitrary_seed_sign():
    p = np.array([.25, 0., .15])
    y = observe(p, np.eye(3))
    pair = co_centered_hypotheses(y)
    assert_allclose(pair[1].position, -pair[0].position, atol=0)
    assert max(f.residual_nt for f in pair) < 1e-6
    assert min(np.linalg.norm(f.position - p) for f in pair) < 1e-7
    # Ground truth is used for set evaluation, never selecting a returned branch.


def test_negative_y_positive_seed_is_wrong_despite_tiny_residual():
    p = np.array([-.25, -.05, -.15])
    y = observe(p, np.eye(3))
    positive, negative = co_centered_hypotheses(y)
    assert positive.success
    assert np.dot(positive.position, p) < 0
    assert np.linalg.norm(positive.position - p) > .5
    assert positive.residual_nt < 1e-6
    assert_allclose(negative.position, p, atol=1e-8)


def test_noisy_co_centered_candidates_have_identical_residual():
    rng = np.random.default_rng(42)
    y = observe([.25, -.005, .15], np.eye(3)) + rng.normal(0, 1e-9, (3, 3))
    pair = co_centered_hypotheses(y)
    assert_allclose(pair[0].residual_nt, pair[1].residual_nt, atol=1e-10)
    assert np.linalg.norm(pair[0].position - pair[1].position) > .5


def test_trajectory_fixture_crosses_both_directions_and_samples_exact_zero():
    trajectories = list(boundary_trajectories(17))
    assert len(trajectories) == 12
    for trajectory in trajectories:
        assert np.min(np.linalg.norm(trajectory.positions, axis=1)) > .25
        if trajectory.identity == 'positive_to_negative':
            assert trajectory.positions[0, 1] > 0 > trajectory.positions[-1, 1]
            assert trajectory.positions[8, 1] == 0
        if trajectory.identity == 'negative_to_positive':
            assert trajectory.positions[0, 1] < 0 < trajectory.positions[-1, 1]
        if trajectory.identity == 'along_boundary':
            assert_allclose(trajectory.positions[:, 1], 0, atol=0)


def test_previous_pose_tracks_crossing_without_truth_initialization():
    path = next(t for t in boundary_trajectories(17) if t.identity == 'positive_to_negative')
    measurements = [observe(p, r) for p, r in zip(path.positions, path.rotations)]
    pairs = temporal_hypotheses(measurements)
    estimates = np.array([p[0].position for p in pairs])
    assert_allclose(estimates, path.positions, atol=1e-7)
    assert np.max(np.linalg.norm(np.diff(estimates, axis=0), axis=1)) < .02
    assert estimates[-1, 1] < 0  # No positive-y reset after initialization.


def test_wrong_initial_branch_remains_continuously_wrong():
    path = next(t for t in boundary_trajectories(17) if t.identity == 'negative_to_positive')
    measurements = [observe(p, r) for p, r in zip(path.positions, path.rotations)]
    pairs = temporal_hypotheses(measurements, initial_hemisphere=1)
    estimates = np.array([p[0].position for p in pairs])
    assert_allclose(estimates, -path.positions, atol=1e-7)
    assert max(p[0].residual_nt for p in pairs) < 1e-6
    assert min(np.linalg.norm(e-p) for e, p in zip(estimates, path.positions)) > .7


def test_temporal_inputs_cannot_discriminate_opposite_true_trajectories():
    path = next(t for t in boundary_trajectories(9) if t.identity == 'crossing_and_rotation')
    observed = [observe(p, r) for p, r in zip(path.positions, path.rotations)]
    mirrored = [observe(-p, r) for p, r in zip(path.positions, path.rotations)]
    assert_allclose(observed, mirrored, atol=0, rtol=0)
    left, right = temporal_hypotheses(observed), temporal_hypotheses(mirrored)
    assert_allclose([p[0].position for p in left], [p[0].position for p in right], atol=0, rtol=0)
    assert set(inspect.signature(temporal_hypotheses).parameters) == {'measurements', 'initial_hemisphere'}


def test_displaced_sources_over_multiple_points_and_observation_only_starts():
    for p in ([.25, -.05, .15], [.55, .005, -.25], [-.25, 0., -.15]):
        p = np.array(p)
        y = observe(p, np.eye(3), origins=displaced_origins())
        assert np.linalg.norm(y - observe(-p, np.eye(3), origins=displaced_origins())) > 1e-9
        pair = displaced_hypotheses(y)
        index, selected = residual_selection(pair)
        assert selected is pair[index]
        assert selected.success
        assert selected.residual_nt <= max(f.residual_nt for f in pair)
    assert set(inspect.signature(displaced_hypotheses).parameters) == {'measurement'}


def test_declared_regions_do_not_hide_exact_offsets():
    assert region(-.02) == 'negative_y_lt_minus5mm'
    assert region(.02) == 'positive_y_gt_5mm'
    for y in (-.005, 0., .005):
        assert region(y) == 'near_zero_abs_y_le_5mm'


def test_noisy_crossing_retains_two_equal_residual_hypotheses():
    path = next(t for t in boundary_trajectories(17) if t.identity == 'crossing_and_rotation')
    rng = np.random.default_rng(831)
    measurements = [observe(p, r) + rng.normal(0, 1e-12, (3, 3)) for p, r in zip(path.positions, path.rotations)]
    pairs = temporal_hypotheses(measurements)
    assert max(np.linalg.norm(pair[0].position-p) for pair, p in zip(pairs, path.positions)) < .005
    for positive, mirror in pairs:
        assert_allclose(positive.residual_nt, mirror.residual_nt, atol=1e-10)
        assert_allclose(positive.position, -mirror.position, atol=0)


def test_restart_after_crossing_loses_absolute_branch_without_extra_information():
    path = next(t for t in boundary_trajectories(17) if t.identity == 'positive_to_negative')
    measurements = [observe(p, r) for p, r in zip(path.positions, path.rotations)]
    full = temporal_hypotheses(measurements)
    cut = 10
    restarted = temporal_hypotheses(measurements[cut:])
    assert_allclose([pair[0].position for pair in full], path.positions, atol=1e-7)
    assert_allclose([pair[0].position for pair in restarted], -path.positions[cut:], atol=1e-7)
