# SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
# SPDX-License-Identifier: MPL-2.0
"""Reproducible synthetic E1 study. Run from the research directory: python -m e1.run."""

import argparse
import csv
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
from .geometry import workspace
from .model import MOMENT, field_matrix, finite_triad, observe, loop_field, dipole_field
from .estimation import analytic_seed, estimate, observability, orientation_error_deg, pose_jacobian


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    """Errors over ALL attempted fits, not just optimizer successes."""
    errors = np.array([r['position_error_m'] for r in rows])
    return {
        'attempts': len(rows),
        'median_m': float(np.median(errors)),
        'p95_m': float(np.percentile(errors, 95)),
        'worst_m': float(np.max(errors)),
        'orientation_median_deg': float(np.median([r['orientation_error_deg'] for r in rows])),
        'orientation_p95_deg': float(np.percentile([r['orientation_error_deg'] for r in rows], 95)),
        'optimizer_success_fraction': float(np.mean([r['solver_success'] for r in rows])),
        'within_5cm_fraction': float(np.mean(errors <= 0.05)),
        'antipodal_lobe_fraction': float(np.mean([r['antipodal_lobe'] for r in rows])),
        'negative_y_fraction': float(np.mean([r['negative_y'] for r in rows])),
        'median_evaluations': float(np.median([r['evaluations'] for r in rows])),
        'p95_residual_nt': float(np.percentile([r['residual_nt'] for r in rows], 95)),
    }


def simulate(samples, name, noise_nt, repetitions, rng, mode='dipole', amount=0.0,
             moment_scale=1.0):
    rows = []
    for sample in samples:
        for trial in range(repetitions):
            # Random roll is independent of the analytic seed and the evaluation noise.
            rotation = sample.rotation @ Rotation.from_rotvec([0, 0, rng.uniform(-np.pi, np.pi)]).as_matrix()
            position = sample.position
            moments = MOMENT * moment_scale * np.eye(3)
            y = observe(position, rotation, moments=moments)
            if mode == 'finite':
                y = finite_triad(position, rotation, radius=amount)
            elif mode == 'tx_gain':
                y *= 1 + amount
            elif mode == 'tx_axis':
                moments[:, 0] = Rotation.from_rotvec([0, 0, amount]).apply(moments[:, 0])
                y = observe(position, rotation, moments=moments)
            elif mode == 'rx_gain':
                y = np.diag([1 + amount, 1 - amount, 1]) @ y
            elif mode == 'rx_nonorthogonal':
                axes = np.eye(3)
                axes[0] = [np.cos(amount), np.sin(amount), 0]
                y = observe(position, rotation, axes=axes)
            elif mode == 'rx_rigid':
                y = Rotation.from_rotvec([0, 0, amount]).as_matrix().T @ y
            elif mode == 'tx_offset':
                origins = np.zeros((3, 3))
                origins[0] = [amount, 0, 0]
                y = observe(position, rotation, origins=origins)
            elif mode == 'sequential_motion':
                y = np.column_stack([observe(position + [0, dt, 0], rotation)[:, axis]
                                     for axis, dt in enumerate((-amount / 2, 0, amount / 2))])
            elif mode == 'combined':
                y = 1.05 * np.diag([1.03, .97, 1]) @ finite_triad(position, rotation, radius=.04)
            y += rng.normal(0, noise_nt * 1e-9, y.shape)
            fitted = estimate(y, moment=MOMENT * moment_scale)
            rows.append({
                'scenario': name, 'sample': sample.identity, 'mount': sample.mount,
                'body_scale': sample.scale, 'pose': sample.pose, 'hand': sample.hand,
                'trial': trial, 'noise_nt': noise_nt, 'distance_m': float(np.linalg.norm(position)),
                'position_error_m': float(np.linalg.norm(fitted.position - position)),
                'orientation_error_deg': orientation_error_deg(fitted.rotation, rotation),
                'solver_success': fitted.success, 'evaluations': fitted.evaluations,
                'residual_nt': fitted.residual_nt,
                'antipodal_lobe': bool(np.dot(fitted.position, position) < 0),
                'negative_y': bool(fitted.position[1] < 0),
            })
    return rows


def study_observability(samples):
    rows = []
    for sample in samples:
        for count in (1, 2, 3):
            rank, condition, singular, covariance = observability(sample.position, sample.rotation,
                                                                 axes=np.eye(3)[:count])
            rows.append({'sample': sample.identity, 'mount': sample.mount, 'rx_axes': count,
                         'rank': rank, 'condition_1m_1rad': condition,
                         'smallest_sv_nt': float(singular[-1] / 1e-9),
                         'position_rms_crlb_1nt_m': None if covariance is None else float(np.sqrt(np.trace(covariance)) * 1e-9)})
    special = {}
    for count in (1, 2, 3):
        rank, condition, singular, _ = observability(np.array([0., 0., 0.5]), np.eye(3), np.eye(3)[:count])
        special[f'radial_z_rx_{count}_axes'] = {'rank': rank, 'condition': condition,
                                               'singular_values_nt': (singular / 1e-9).tolist()}
    return rows, special


def branch_and_initialization(rng):
    p = np.array([0.22, 0.43, 0.17])
    rotation = Rotation.from_euler('xyz', [0.4, -0.3, 0.7]).as_matrix()
    y = observe(p, rotation)
    seed = analytic_seed(y)
    exact = estimate(y, initial=seed)
    mirror = estimate(y, initial=(-seed[0], seed[1]))
    trials = []
    for i in range(24):
        p0 = rng.uniform(-0.8, 0.8, 3)
        r0 = Rotation.random(random_state=rng).as_matrix()
        fitted = estimate(y, initial=(p0, r0))
        trials.append({'trial': i, 'position_error_m': float(np.linalg.norm(fitted.position - p)),
                       'nearest_antipodal_error_m': float(min(np.linalg.norm(fitted.position - p), np.linalg.norm(fitted.position + p))),
                       'solver_success': fitted.success, 'evaluations': fitted.evaluations,
                       'residual_nt': fitted.residual_nt})
    # A deliberately asymmetric, calibrated displacement: one source is shifted.
    origins = np.zeros((3, 3))
    origins[0] = [0.12, 0, 0]
    displaced = observe(p, rotation, origins=origins)
    displaced_seed = analytic_seed(displaced)
    fitted_positive = estimate(displaced, initial=displaced_seed, origins=origins)
    fitted_negative = estimate(displaced, initial=(-displaced_seed[0], displaced_seed[1]), origins=origins)
    return {
        'position_m': p.tolist(),
        'antipodal_measurement_difference_t': float(np.linalg.norm(y - observe(-p, rotation))),
        'exact_seed_position_error_m': float(np.linalg.norm(exact.position - p)),
        'mirror_seed_position_error_m': float(np.linalg.norm(mirror.position - p)),
        'mirror_seed_residual_nt': mirror.residual_nt,
        'finite_loop_antipodal_difference_t': float(np.linalg.norm(finite_triad(p, rotation) - finite_triad(-p, rotation))),
        'displaced_source_mirror_measurement_difference_nt': float(np.linalg.norm(displaced - observe(-p, rotation, origins=origins)) / 1e-9),
        'displaced_positive_start_error_m': float(np.linalg.norm(fitted_positive.position - p)),
        'displaced_negative_start_error_m': float(np.linalg.norm(fitted_negative.position - p)),
        'displaced_negative_start_residual_nt': fitted_negative.residual_nt,
        'random_start_trials': trials,
        'note': 'One displaced-source pose is a diagnostic, not global uniqueness or workspace proof.'}


def two_receiver_diagnostic(samples):
    pair = [s for s in samples if s.scale == 1 and s.mount == 'waist' and s.pose == 'forward']
    joint = np.zeros((18, 12))
    common_gain = []
    for index, sample in enumerate(pair):
        joint[index * 9:(index + 1) * 9, index * 6:(index + 1) * 6] = pose_jacobian(sample.position, sample.rotation)
        common_gain.extend(observe(sample.position, sample.rotation).ravel())
    augmented = np.column_stack([joint, common_gain])
    def numerical_rank(matrix):
        singular = np.linalg.svd(matrix, compute_uv=False)
        return int(np.sum(singular > singular[0] * 1e-7))
    return {'rank_18x12_independent_pose_jacobian': numerical_rank(joint),
            'rank_18x13_with_unknown_common_gain': numerical_rank(augmented),
            'rank_relative_tolerance': 1e-7,
            'sample_ids': [s.identity for s in pair],
            'note': 'No modeled receiver coupling, radio traffic, or common calibration noise; independent observations only.'}


def plot_all(samples, coverage, aggregates, finite_rows, output):
    # Keep labels as text rather than embedding third-party font outlines.
    plt.rcParams.update({'font.size': 9, 'svg.hashsalt': 'kinestro-e1', 'svg.fonttype': 'none'})
    fig = plt.figure(figsize=(11, 4.5))
    for index, mount in enumerate(('waist', 'chest'), 1):
        ax = fig.add_subplot(1, 2, index, projection='3d')
        group = [s for s in samples if s.mount == mount]
        coords = np.array([s.position for s in group])
        colors = [np.linalg.norm(field_matrix(s.position)) / np.sqrt(6) / 1e-9 for s in group]
        dots = ax.scatter(*coords.T, c=colors, cmap='viridis', norm=matplotlib.colors.LogNorm())
        ax.scatter(0, 0, 0, marker='*', c='red', s=70)
        for sample in group:
            if sample.scale == 1:
                arm = np.array([sample.shoulder, sample.elbow, sample.wrist]) - sample.transmitter
                ax.plot(*arm.T, color='grey', alpha=0.35, linewidth=0.8)
        ax.set(xlabel='right x [m]', ylabel='forward y [m]', zlabel='up z [m]', title=f'{mount}: 36 assumed receiver points')
        fig.colorbar(dots, ax=ax, shrink=0.6, label='dipole scale a [nT RMS]')
    fig.suptitle('Synthetic body-relative workspace; no measured human geometry')
    fig.tight_layout()
    fig.savefig(output / 'workspace.svg', metadata={'Date': None})
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
    for mount in ('waist', 'chest'):
        groups = [r for r in coverage if r['mount'] == mount]
        axes[0].scatter([r['distance_m'] for r in groups], [r['scale_nt'] for r in groups], label=mount, alpha=0.7)
        noise = [.1, 1., 10., 100.]
        errors = [aggregates[f'noise_{n:g}nt'][mount]['p95_m'] for n in noise]
        axes[1].plot(noise, np.array(errors) * 100, 'o-', label=mount)
    axes[0].set(xlabel='distance [m]', ylabel='dipole scale a [nT RMS]', yscale='log')
    axes[1].set(xlabel='post-demod per-entry noise [nT RMS]', ylabel='3D error p95 [cm]', xscale='log', yscale='log')
    axes[1].axhline(5, color='red', linestyle='--', label='proposed 5 cm screen')
    for radius in sorted({r['radius_m'] for r in finite_rows}):
        group = [r for r in finite_rows if r['radius_m'] == radius]
        axes[2].plot([r['distance_over_radius'] for r in group], [100 * r['relative_field_error'] for r in group], label=f'radius {radius*100:g} cm')
    axes[2].set(xlabel='distance / coil radius', ylabel='finite vs dipole relative field error [%]', xscale='log', yscale='log')
    axes[2].set_xticks([2, 5, 10, 20], labels=['2', '5', '10', '20'])
    axes[2].xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    for ax in axes:
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7)
    fig.suptitle('SIMULATED: field, noise sensitivity and finite-coil model mismatch')
    fig.tight_layout()
    fig.savefig(output / 'sensitivity.svg', metadata={'Date': None})
    plt.close(fig)
    # Normalize generator whitespace, retaining SVG path separators as newlines.
    for name in ('workspace.svg', 'sensitivity.svg'):
        path = output / name
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=20261115)
    parser.add_argument('--trials', type=int, default=6, help='MC repetitions per anatomical point per noise level')
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--figures', type=Path, default=Path('figures'))
    args = parser.parse_args()
    if args.trials < 1:
        parser.error('--trials must be positive')
    args.output.mkdir(parents=True, exist_ok=True)
    args.figures.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    samples = workspace()
    coverage = []
    for sample in samples:
        field = field_matrix(sample.position)
        row = {'sample': sample.identity, 'scale': sample.scale, 'pose': sample.pose,
               'hand': sample.hand, 'mount': sample.mount,
               'distance_m': float(np.linalg.norm(sample.position)),
               'scale_nt': float(np.linalg.norm(field) / np.sqrt(6) / 1e-9),
               'min_tx_vector_nt': float(np.min(np.linalg.norm(field, axis=0)) / 1e-9),
               'min_abs_channel_nt': float(np.min(abs(observe(sample.position, sample.rotation))) / 1e-9)}
        for label, vector in [('position', sample.position), ('receiver', sample.receiver),
                              ('shoulder', sample.shoulder), ('elbow', sample.elbow),
                              ('wrist', sample.wrist), ('transmitter', sample.transmitter)]:
            row.update({f'{label}_{axis}_m': float(value) for axis, value in zip('xyz', vector)})
        row.update({f'rotation_{i}{j}': float(sample.rotation[i, j]) for i in range(3) for j in range(3)})
        coverage.append(row)
    write_csv(args.output / 'workspace.csv', coverage)
    all_rows = []
    for noise in (0., 0.1, 1., 10., 100.):
        name = f'noise_{noise:g}nt'
        print(f'Running {name}', flush=True)
        all_rows.extend(simulate(samples, name, noise, args.trials, rng))
    scenarios = [('gain_1pct', 'tx_gain', .01), ('gain_5pct', 'tx_gain', .05),
                 ('gain_10pct', 'tx_gain', .10), ('tx_axis_2deg', 'tx_axis', np.deg2rad(2)),
                 ('rx_gain_3pct', 'rx_gain', .03), ('rx_nonorthogonal_2deg', 'rx_nonorthogonal', np.deg2rad(2)),
                 ('rx_rigid_2deg', 'rx_rigid', np.deg2rad(2)), ('tx_offset_5mm', 'tx_offset', .005),
                 ('sequential_10ms_1mps', 'sequential_motion', .01)]
    scenarios += [(f'finite_radius_{radius:g}m', 'finite', radius) for radius in (.02, .04, .08)]
    for name, mode, amount in scenarios:
        print(f'Running {name}', flush=True)
        all_rows.extend(simulate(samples, name, 0., 1, rng, mode, amount))
    all_rows.extend(simulate(samples, 'combined_finite_gain_1nt', 1., args.trials, rng, 'combined'))
    for scale in (.5, 2.):
        name = f'moment_{scale:g}x_1nt'
        all_rows.extend(simulate(samples, name, 1., args.trials, rng, moment_scale=scale))
    aggregates = {}
    for name in sorted({r['scenario'] for r in all_rows}):
        group = [r for r in all_rows if r['scenario'] == name]
        aggregates[name] = {'all': summarize(group)}
        for mount in ('waist', 'chest'):
            aggregates[name][mount] = summarize([r for r in group if r['mount'] == mount])
    # Compact group results preserve body-size, pose, and range failures without raw MC data.
    groups = []
    for mount in ('waist', 'chest'):
        for noise in (.1, 1., 10., 100.):
            for pose in sorted({s.pose for s in samples}):
                subset = [r for r in all_rows if r['mount'] == mount and r['noise_nt'] == noise
                          and r['scenario'] == f'noise_{noise:g}nt' and r['pose'] == pose]
                groups.append({'mount': mount, 'noise_nt': noise, 'pose': pose, **summarize(subset)})
    write_csv(args.output / 'pose_summary.csv', groups)
    size_groups, range_groups = [], []
    for mount in ('waist', 'chest'):
        for noise in (.1, 1., 10., 100.):
            matched = [r for r in all_rows if r['mount'] == mount and r['scenario'] == f'noise_{noise:g}nt']
            for scale in (.85, 1., 1.15):
                subset = [r for r in matched if r['body_scale'] == scale]
                size_groups.append({'mount': mount, 'noise_nt': noise, 'body_scale': scale, **summarize(subset)})
            for low, high in ((0., .25), (.25, .5), (.5, .75), (.75, 1.)):
                subset = [r for r in matched if low <= r['distance_m'] < high]
                if subset:
                    range_groups.append({'mount': mount, 'noise_nt': noise,
                                         'min_distance_m': low, 'max_distance_m': high, **summarize(subset)})
    write_csv(args.output / 'body_size_summary.csv', size_groups)
    write_csv(args.output / 'distance_summary.csv', range_groups)
    observability_rows, special = study_observability(samples)
    write_csv(args.output / 'observability.csv', observability_rows)
    finite_rows = []
    direction = np.array([0.3, 0.4, np.sqrt(.75)])
    for radius in (.02, .04, .08):
        for ratio in (2., 3., 5., 10., 20.):
            p = direction * radius * ratio
            finite = np.column_stack([loop_field(p, n, radius) for n in np.eye(3)])
            dipole = field_matrix(p)
            finite_rows.append({'radius_m': radius, 'distance_over_radius': ratio,
                                'relative_field_error': float(np.linalg.norm(finite - dipole) / np.linalg.norm(finite))})
    write_csv(args.output / 'finite_field.csv', finite_rows)
    summary = {
        'classification': 'SYNTHETIC SIMULATION ONLY; no physical measurements',
        'seed': args.seed, 'trials_per_point_per_noise': args.trials,
        'versions': {'python': platform.python_version(), 'numpy': np.__version__,
                     'scipy': scipy.__version__, 'matplotlib': matplotlib.__version__},
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(Path(__file__).parent.glob('*.py'))},
        'config': {'moment_rms_a_m2': MOMENT, 'tx_radius_m': .04,
                   'noise_levels_nt_rms_per_entry': [0, .1, 1, 10, 100],
                   'source_model': 'free-space point dipole; inverse always point dipole',
                   'hemisphere_prior': 'positive reference-frame y; not a runtime-validated constraint',
                   'numerical_box_m': [-2, 2], 'solver_max_nfev': 180,
                   'jacobian_scaling': '1 m translations; 1 rad local rotations',
                   'noise_model': 'independent zero-mean Gaussian post-demod field-equivalent entries',
                   'model_mismatch_noise_nt': 0, 'mismatch_repetitions_per_point': 1,
                   'combined_scenario': 'finite radius .04m + common gain +5% + RX gains [1.03,.97,1] + 1nT noise'},
        'workspace_points': len(samples), 'monte_carlo_fit_count': len(all_rows),
        'workspace': {mount: {'min_distance_m': min(r['distance_m'] for r in coverage if r['mount'] == mount),
                              'max_distance_m': max(r['distance_m'] for r in coverage if r['mount'] == mount),
                              'min_scale_nt': min(r['scale_nt'] for r in coverage if r['mount'] == mount)} for mount in ('waist', 'chest')},
        'scenarios': aggregates, 'special_observability': special,
        'two_receiver_diagnostic': two_receiver_diagnostic(samples),
        'ambiguity': branch_and_initialization(rng),
        'failure_semantics': 'Optimizer failure is status=false; accuracy failure is >.05m; antipodal lobe is dot(p_hat,p_true)<0; negative_y is a separate hemisphere diagnostic; all included in errors.',
    }
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    plot_all(samples, coverage, aggregates, finite_rows, args.figures)
    print(f'Wrote {len(all_rows)} synthetic fits and figures; no hardware validation.', flush=True)


if __name__ == '__main__':
    main()
