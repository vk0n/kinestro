# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Versioned static/trajectory hemisphere stress study; python -m e1.boundary_run."""

import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
from .boundary import (boundary_workspace, boundary_trajectories, displaced_origins,
                       co_centered_hypotheses, displaced_hypotheses, residual_selection,
                       temporal_hypotheses, region, Y_OFFSETS)
from .estimation import analytic_seed, estimate, observability, orientation_error_deg
from .model import MOMENT, observe, finite_triad
from .run import write_csv

ROOT = Path(__file__).resolve().parent.parent
NOISE_LEVELS = (0., .1, 1., 10.)


def score(fitted, position, rotation, noise_nt):
    """Truth is used ONLY here, after estimation, for offline evaluation."""
    error = float(np.linalg.norm(fitted.position - position))
    wrong = bool(np.dot(fitted.position, position) < 0)
    gate = 3 * noise_nt if noise_nt > 0 else 1e-6
    return {'position_error_m': error, 'orientation_error_deg': orientation_error_deg(fitted.rotation, rotation),
            'wrong_branch': wrong, 'residual_nt': fitted.residual_nt,
            'solver_success': fitted.success, 'evaluations': fitted.evaluations,
            'wrong_pose_low_residual': bool(error > .05 and fitted.residual_nt <= gate),
            'low_residual_gate_nt': gate}


def aggregate(rows):
    errors = [r['position_error_m'] for r in rows]
    return {'attempts': len(rows), 'median_m': float(np.median(errors)),
            'p95_m': float(np.percentile(errors, 95)), 'max_m': float(np.max(errors)),
            'orientation_median_deg': float(np.median([r['orientation_error_deg'] for r in rows])),
            'orientation_p95_deg': float(np.percentile([r['orientation_error_deg'] for r in rows], 95)),
            'wrong_branch_fraction': float(np.mean([r['wrong_branch'] for r in rows])),
            'within_5cm_fraction': float(np.mean(np.array(errors) <= .05)),
            'residual_median_nt': float(np.median([r['residual_nt'] for r in rows])),
            'residual_p95_nt': float(np.percentile([r['residual_nt'] for r in rows], 95)),
            'solver_success_fraction': float(np.mean([r['solver_success'] for r in rows])),
            'wrong_pose_low_residual_fraction': float(np.mean([r['wrong_pose_low_residual'] for r in rows])),
            'median_nfev': float(np.median([r['evaluations'] for r in rows]))}


def compact_csv(path, rows):
    """Ten significant CSV digits; primary aggregates retain full JSON precision."""
    write_csv(path, [{k: format(v, '.10g') if isinstance(v, (float, np.floating)) else v
                      for k, v in row.items()} for row in rows])


def static_study(samples, trials, rng):
    rows, pairs = [], []
    for noise in NOISE_LEVELS:
        print(f'Static boundary noise {noise:g} nT', flush=True)
        for sample in samples:
            for trial in range(trials):
                perturbation = rng.normal(0, noise * 1e-9, (3, 3))
                centered_y = observe(sample.position, sample.rotation) + perturbation
                centered = co_centered_hypotheses(centered_y)
                separated_y = observe(sample.position, sample.rotation, origins=displaced_origins()) + perturbation
                displaced = displaced_hypotheses(separated_y)
                _, selected = residual_selection(displaced)
                methods = {'A_current_positive_seed': centered[0], 'C_mirror_candidate': centered[1],
                           'D_residual_selected': selected, 'D_positive_start': displaced[0],
                           'D_negative_start': displaced[1]}
                base = {'mount': sample.mount, 'sample': sample.identity, 'noise_nt': noise,
                        'y_m': float(sample.position[1]), 'region': region(sample.position[1]), 'trial': trial}
                for strategy, fitted in methods.items():
                    rows.append({**base, 'strategy': strategy,
                                 **score(fitted, sample.position, sample.rotation, noise)})
                pair_errors = [np.linalg.norm(f.position - sample.position) for f in centered]
                pairs.append({**base,
                              'co_residual_gap_nt': abs(centered[0].residual_nt - centered[1].residual_nt),
                              'co_candidate_separation_m': float(np.linalg.norm(centered[0].position - centered[1].position)),
                              'oracle_min_set_error_m': float(min(pair_errors)),
                              'displaced_residual_gap_nt': abs(displaced[0].residual_nt - displaced[1].residual_nt),
                              'displaced_candidate_separation_m': float(np.linalg.norm(displaced[0].position - displaced[1].position))})
    return rows, pairs


def group_static(rows):
    regional, offsets = [], []
    for mount in ('waist', 'chest'):
        for noise in NOISE_LEVELS:
            for strategy in sorted({r['strategy'] for r in rows}):
                selected = [r for r in rows if r['mount'] == mount and r['noise_nt'] == noise and r['strategy'] == strategy]
                for label in sorted({r['region'] for r in selected}):
                    regional.append({'mount': mount, 'noise_nt': noise, 'strategy': strategy, 'region': label,
                                     **aggregate([r for r in selected if r['region'] == label])})
                for y in Y_OFFSETS:
                    offsets.append({'mount': mount, 'noise_nt': noise, 'strategy': strategy, 'y_m': y,
                                    **aggregate([r for r in selected if r['y_m'] == y])})
    return regional, offsets


def initialization_study(samples, rng):
    rows = []
    # Fixed diagnostic subset, selected by fixture label; no seed uses its pose.
    subset = [s for s in samples if '-xz0-' in s.identity and abs(s.position[1]) <= .005]
    for noise in (0., 1.):
        for sample in subset:
            measurement = observe(sample.position, sample.rotation) + rng.normal(0, noise * 1e-9, (3, 3))
            measured_range = np.linalg.norm(analytic_seed(measurement)[0])
            for attempt in range(4):
                direction = rng.normal(size=3)
                position_seed = direction / np.linalg.norm(direction) * measured_range * rng.uniform(.7, 1.3)
                rotation_seed = Rotation.random(random_state=rng).as_matrix()
                fitted = estimate(measurement, initial=(position_seed, rotation_seed))
                rows.append({'mount': sample.mount, 'sample': sample.identity, 'noise_nt': noise,
                             'y_m': float(sample.position[1]), 'initialization': attempt,
                             **score(fitted, sample.position, sample.rotation, noise)})
    return rows


def trajectory_metrics(fits, positions, rotations, noise):
    scored = [score(f, p, r, noise) for f, p, r in zip(fits, positions, rotations, strict=True)]
    estimates = np.array([f.position for f in fits])
    errors = np.array([r['position_error_m'] for r in scored])
    wrong = np.array([r['wrong_branch'] for r in scored])
    steps = np.linalg.norm(np.diff(estimates, axis=0), axis=1)
    true_steps = np.linalg.norm(np.diff(positions, axis=0), axis=1)
    step_error = np.linalg.norm(np.diff(estimates, axis=0) - np.diff(positions, axis=0), axis=1)
    transitions = np.diff(wrong.astype(int))
    return {**aggregate(scored), 'wrong_branch_transitions': int(np.sum(transitions != 0)),
            'correct_to_wrong_transitions': int(np.sum(transitions == 1)),
            'wrong_to_correct_transitions': int(np.sum(transitions == -1)),
            'max_estimated_step_m': float(np.max(steps)),
            'max_true_step_m': float(np.max(true_steps)),
            'step_error_p95_m': float(np.percentile(step_error, 95)),
            'jump_events_over_20cm': int(np.sum(steps > .20)),
            'error_integral_m_s': float(np.trapezoid(errors, dx=.025)),
            'final_error_m': float(errors[-1]), 'final_wrong_branch': bool(wrong[-1]),
            'initial_wrong_branch': bool(wrong[0]),
            'branch_loss_after_correct_start': bool(not wrong[0] and np.any(wrong[1:]))}, scored


def separated_sequence(measurements):
    """Two observation seeds plus previous selected pose, chosen by residual only."""
    fits = []
    previous = None
    for measurement in measurements:
        candidates = list(displaced_hypotheses(measurement))
        if previous is not None:
            candidates.append(estimate(measurement, initial=(previous.position, previous.rotation),
                                       origins=displaced_origins()))
        _, previous = residual_selection(candidates)
        fits.append(previous)
    return fits


def trajectory_study(trajectories, trials, rng):
    summary, traces, plots, restarts, pair_sets = [], [], {}, [], []
    for noise in NOISE_LEVELS:
        print(f'Trajectory boundary noise {noise:g} nT', flush=True)
        for trajectory in trajectories:
            positions, rotations = trajectory.positions, trajectory.rotations
            for trial in range(trials):
                perturbation = rng.normal(0, noise * 1e-9, (len(positions), 3, 3))
                centered_y = np.array([observe(p, r) for p, r in zip(positions, rotations, strict=True)]) + perturbation
                separated_y = np.array([observe(p, r, origins=displaced_origins()) for p, r in zip(positions, rotations, strict=True)]) + perturbation
                independent = [estimate(y) for y in centered_y]
                hypotheses = temporal_hypotheses(centered_y, initial_hemisphere=1)
                temporal = [pair[0] for pair in hypotheses]
                mirror = [pair[1] for pair in hypotheses]
                displaced = separated_sequence(separated_y)
                pair_sets.append({'mount': trajectory.mount, 'path': trajectory.identity,
                                  'noise_nt': noise, 'trial': trial, 'frames': len(positions),
                                  'max_residual_gap_nt': max(abs(p[0].residual_nt-p[1].residual_nt) for p in hypotheses),
                                  'oracle_set_coverage_5cm_fraction': float(np.mean([
                                      min(np.linalg.norm(pair[0].position-p), np.linalg.norm(pair[1].position-p)) <= .05
                                      for pair, p in zip(hypotheses, positions, strict=True)])),
                                  'unresolved_hypotheses': 2})
                if trajectory.identity == 'positive_to_negative':
                    # Fixed sample-index reset; no truth-dependent reset or seed.
                    cut = len(positions)//2 + max(1, len(positions)//10)
                    restarted = [pair[0] for pair in temporal_hypotheses(centered_y[cut:])]
                    metrics, _ = trajectory_metrics(restarted, positions[cut:], rotations[cut:], noise)
                    restarts.append({'mount': trajectory.mount, 'noise_nt': noise, 'trial': trial,
                                     'reset_frame': cut, 'reset_time_s': float(trajectory.times_s[cut]), **metrics})
                methods = {'A_current_positive_seed': independent,
                           'B_previous_pose_positive_assumption': temporal,
                           'C_mirror_temporal_candidate': mirror,
                           'D_separated_multistart': displaced}
                series = {}
                for strategy, fits in methods.items():
                    metrics, scores = trajectory_metrics(fits, positions, rotations, noise)
                    summary.append({'mount': trajectory.mount, 'path': trajectory.identity,
                                    'noise_nt': noise, 'trial': trial, 'strategy': strategy, **metrics})
                    series[strategy] = (fits, scores)
                if trajectory.mount == 'waist' and trial == 0:
                    plots[(trajectory.identity, noise)] = (trajectory, series)
                    if noise in (0., 1.):
                        for frame, position in enumerate(positions):
                            row = {'path': trajectory.identity, 'noise_nt': noise, 'frame': frame,
                                   'time_s': float(trajectory.times_s[frame]), 'true_y_m': float(position[1])}
                            for label, strategy in [('A', 'A_current_positive_seed'), ('B', 'B_previous_pose_positive_assumption'),
                                                    ('D', 'D_separated_multistart')]:
                                fitted, scored = series[strategy]
                                row.update({f'{label}_x_m': float(fitted[frame].position[0]),
                                            f'{label}_error_m': scored[frame]['position_error_m'],
                                            f'{label}_wrong_branch': scored[frame]['wrong_branch'],
                                            f'{label}_residual_nt': scored[frame]['residual_nt']})
                            traces.append(row)
    return summary, traces, plots, restarts, pair_sets


def plot_results(offsets, plots, destination):
    plt.rcParams.update({'font.size': 9, 'svg.hashsalt': 'kinestro-boundary-v1', 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))
    for strategy, label in [('A_current_positive_seed', 'A: positive-y seed'), ('D_residual_selected', 'D: separated, residual choice')]:
        for noise, linestyle in [(0., '-'), (1., '--')]:
            subset = [r for r in offsets if r['mount'] == 'waist' and r['strategy'] == strategy and r['noise_nt'] == noise]
            axes[0].plot([r['y_m'] for r in subset], [r['wrong_branch_fraction'] for r in subset],
                         'o' + linestyle, label=f'{label}; {noise:g} nT')
            axes[1].plot([r['y_m'] for r in subset], [r['p95_m'] for r in subset], 'o' + linestyle)
    axes[0].set(ylabel='wrong antipodal-lobe fraction', ylim=(-.05, 1.05))
    axes[0].legend(fontsize=7)
    axes[1].set(ylabel='position P95 [m]')
    for ax in axes:
        ax.set_xlabel('true source-relative y [m]')
        ax.axvline(0, color='grey', linewidth=1)
        ax.grid(alpha=.25)
    fig.suptitle('SIMULATED abstract boundary fixtures; both signs retained in scoring')
    fig.tight_layout()
    fig.savefig(destination / 'static_boundary.svg', metadata={'Date': None})
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(11, 6.2))
    panels = [('positive_to_negative', 0., 'x'), ('negative_to_positive', 0., 'x'),
              ('along_boundary', 1., 'error'), ('far_crossing', 10., 'error')]
    for ax, (name, noise, quantity) in zip(axes.ravel(), panels, strict=True):
        trajectory, methods = plots[(name, noise)]
        for strategy, label in [('A_current_positive_seed', 'A: per-frame +y seed'),
                                ('B_previous_pose_positive_assumption', 'B: previous pose'),
                                ('D_separated_multistart', 'D: separated + multistart')]:
            fits, scores = methods[strategy]
            values = [f.position[0] for f in fits] if quantity == 'x' else [s['position_error_m'] for s in scores]
            ax.plot(trajectory.times_s, values, label=label, linewidth=1.3)
        if quantity == 'x':
            ax.plot(trajectory.times_s, trajectory.positions[:, 0], 'k--', label='true x')
            ax.axvline(trajectory.times_s[len(trajectory.times_s)//2], color='grey', linestyle=':')
        ax.set(xlabel='synthetic time [s]', ylabel='estimated x [m]' if quantity == 'x' else 'position error [m]',
               title=f'{name}; {noise:g} nT')
        ax.grid(alpha=.25)
        ax.legend(fontsize=7)
    fig.suptitle('SIMULATED trajectories: continuity and absolute branch are different claims')
    fig.tight_layout()
    fig.savefig(destination / 'boundary_trajectories.svg', metadata={'Date': None})
    plt.close(fig)
    for path in destination.glob('*.svg'):
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=20261116)
    parser.add_argument('--trials', type=int, default=2)
    parser.add_argument('--frames', type=int, default=41)
    parser.add_argument('--output', type=Path, default=Path('results/boundary-v1'))
    parser.add_argument('--figures', type=Path, default=Path('figures/boundary-v1'))
    args = parser.parse_args()
    if args.trials < 1:
        parser.error('--trials must be positive')
    if args.output.resolve() == (ROOT / 'results').resolve() or args.figures.resolve() == (ROOT / 'figures').resolve():
        parser.error('Use versioned subdirectories to preserve the baseline artifacts')
    samples, trajectories = boundary_workspace(), list(boundary_trajectories(args.frames))
    args.output.mkdir(parents=True, exist_ok=True)
    args.figures.mkdir(parents=True, exist_ok=True)
    seeds = np.random.SeedSequence(args.seed).spawn(3)
    static, pairs = static_study(samples, args.trials, np.random.default_rng(seeds[0]))
    regional, offsets = group_static(static)
    random_starts = initialization_study(samples, np.random.default_rng(seeds[1]))
    temporal, traces, plots, restarts, temporal_pairs = trajectory_study(trajectories, args.trials, np.random.default_rng(seeds[2]))
    compact_csv(args.output / 'static_regions.csv', regional)
    compact_csv(args.output / 'static_offsets.csv', offsets)
    compact_csv(args.output / 'initializations.csv', random_starts)
    compact_csv(args.output / 'trajectory_summary.csv', temporal)
    compact_csv(args.output / 'trajectory_traces.csv', traces)
    compact_csv(args.output / 'restart_summary.csv', restarts)
    compact_csv(args.output / 'trajectory_hypotheses.csv', temporal_pairs)
    fixtures = []
    for sample in samples:
        fixtures.append({'sample': sample.identity, 'mirror_id': sample.mirror_id, 'mount': sample.mount,
                         'classification': sample.classification,
                         **{f'{axis}_m': float(v) for axis, v in zip('xyz', sample.position)},
                         **{f'receiver_body_{axis}_m': float(v) for axis, v in zip('xyz', sample.position + sample.transmitter)},
                         **{f'transmitter_body_{axis}_m': float(v) for axis, v in zip('xyz', sample.transmitter)},
                         **{f'rotation_{i}{j}': float(sample.rotation[i, j]) for i in range(3) for j in range(3)}})
    compact_csv(args.output / 'workspace.csv', fixtures)
    minimum_rank = min(observability(s.position, s.rotation)[0] for s in samples)
    symmetry = max(float(np.linalg.norm(finite_triad(s.position, s.rotation) - finite_triad(-s.position, s.rotation))) for s in samples)
    evidence = []
    for noise in NOISE_LEVELS:
        for label in sorted({r['region'] for r in static}):
            for strategy in ('A_current_positive_seed', 'D_residual_selected'):
                selected = [r for r in static if r['noise_nt'] == noise and r['region'] == label and r['strategy'] == strategy]
                evidence.append({'noise_nt': noise, 'region': label, 'strategy': strategy, **aggregate(selected)})
    pair_summary = []
    for noise in NOISE_LEVELS:
        for label in sorted({r['region'] for r in pairs}):
            selected = [r for r in pairs if r['noise_nt'] == noise and r['region'] == label]
            pair_summary.append({'noise_nt': noise, 'region': label, 'attempts': len(selected),
                                 'max_co_residual_gap_nt': max(r['co_residual_gap_nt'] for r in selected),
                                 'oracle_set_coverage_5cm_fraction': float(np.mean([r['oracle_min_set_error_m'] <= .05 for r in selected])),
                                 'displaced_residual_gap_median_nt': float(np.median([r['displaced_residual_gap_nt'] for r in selected])),
                                 'displaced_near_collapsed_pair_fraction': float(np.mean([r['displaced_candidate_separation_m'] < .001 for r in selected]))})
    compact_csv(args.output / 'hypothesis_sets.csv', pair_summary)
    # Illustrate conditional local precision at a globally wrong, low-residual fit.
    diagnostic_truth = np.array([-.25, -.05, -.15])
    diagnostic_y = observe(diagnostic_truth, np.eye(3))
    diagnostic_fit = estimate(diagnostic_y)
    diagnostic_rank, _, _, covariance = observability(diagnostic_fit.position, diagnostic_fit.rotation)
    local_example = {**score(diagnostic_fit, diagnostic_truth, np.eye(3), 0.),
                     'true_position_m': diagnostic_truth.tolist(), 'estimated_position_m': diagnostic_fit.position.tolist(),
                     'local_rank': diagnostic_rank,
                     'conditional_local_position_rms_bound_at_1nt_m': float(np.sqrt(np.trace(covariance)) * 1e-9),
                     'warning': 'Local model-conditional bound, not a calibrated posterior or absolute-branch confidence.'}
    baseline = sorted((ROOT / 'results').glob('*.*')) + sorted((ROOT / 'figures').glob('*.svg'))
    result = {'classification': 'SYNTHETIC ONLY; no physical validation; E1 open', 'schema': 'boundary-v1',
              'seed': args.seed, 'trials': args.trials, 'frames_per_trajectory': args.frames,
              'dt_s': .025, 'static_pose_count': len(samples), 'trajectory_path_count': len(trajectories),
              'static_observation_count_per_model': len(pairs),
              'trajectory_observation_count_per_model': len(trajectories) * len(NOISE_LEVELS) * args.trials * args.frames,
              'random_initialization_fit_count': len(random_starts),
              'nonlinear_fit_count': len(pairs)*3 + len(random_starts)
                  + len(trajectories)*len(NOISE_LEVELS)*args.trials*(5*args.frames-1)
                  + sum(r['attempts'] for r in restarts) + 1,
              'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__, 'matplotlib': matplotlib.__version__},
              'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))},
              'baseline_commit': '6ac8d9ee2b8bb83bbad985e95d43ee623677b99e',
              'preserved_baseline_artifact_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in baseline},
              'config': {'y_offsets_m': list(Y_OFFSETS), 'noise_nt_rms_per_entry': list(NOISE_LEVELS),
                         'moment_rms_a_m2_per_axis': MOMENT, 'displaced_origins_m': displaced_origins().tolist(),
                         'region_definition': 'negative y<-.005; near-zero abs(y)<=.005; positive y>.005',
                         'common_random_noise': 'same noise realization for co-centered and separated comparisons only',
                         'strategy_C': 'retain exact antipodal partner; no residual-based selection; mirrored status is inherited, not an independent fit',
                         'strategy_B_initial_assumption': 'positive-y analytic seed at first frame only, never verified using truth',
                         'strategy_D_static': 'two approximate data-derived starts, convergence then observed residual selection',
                         'strategy_D_temporal': 'same starts plus previous selected pose after first frame; convergence/residual selection',
                         'low_residual_wrong_pose': 'error>.05m and residual<=3*noise_nt; at zero noise use1e-6nT; proxy not calibrated confidence',
                         'jump_diagnostic_m': .20, 'optimizer_settings': 'unchanged e1.estimation.estimate; ±2m box, max_nfev180'},
              'min_full_triad_local_rank': minimum_rank, 'max_finite_loop_antipodal_difference_t': symmetry,
              'wrong_fit_local_precision_example': local_example,
              'static_regional_evidence': evidence, 'hypothesis_set_evidence': pair_summary,
              'temporal_initialization_note': 'Negative-to-positive path starts on an unverified/wrong +y assumption; mirror C is not selected by truth.'}
    (args.output / 'summary.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    plot_results(offsets, plots, args.figures)
    print(f'Boundary-v1 complete: {len(pairs)} static observations/model; {len(temporal)} trajectory method/run summaries.', flush=True)


if __name__ == '__main__':
    main()
