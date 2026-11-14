<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Power and hardware feasibility

**Evidence class:** theoretical calculations with explicit assumptions. No coil, receiver, driver, battery, temperature, runtime, or exposure has been measured for Kinestro. These calculations constrain a laboratory investigation; they do not select production components. The simulation's baseline transmitter moment is the **RMS moment of one active sinusoidally excited axis**, not peak moment or the sum of three axes.

## Generic transmitter calculation

For a thin air-core winding with mean radius $a$, $N$ turns, RMS current $I$, bare wire diameter $d$, electrical resistivity $\rho_e$, and material density $\rho_m$:

$$m=N I\pi a^2,\qquad \ell\simeq2\pi aN,\qquad A_w=\pi d^2/4,$$
$$R_{DC}=\rho_e\ell/A_w,\qquad P_{Cu}=I^2R_{AC},\qquad M_{Cu}=\rho_m\ell A_w.$$

Here $R_{AC}$ is unknown until winding/lead/proximity losses are measured; substituting $R_{DC}$ gives only an initial copper-loss estimate. Lead length, insulation, former, connections, housing, electronics, and battery are omitted. The circular-loop magnetic moment and axial-field relations follow from the current-loop model described in [OpenStax University Physics, section 12.4](https://openstax.org/books/university-physics-volume-2/pages/12-4-magnetic-field-of-a-current-loop).

| Quantity | Explicit illustrative assumption | Calculated consequence |
| --- | --- | --- |
| Mean radius, turns, RMS current | $a=0.04$ m, $N=100$, $I=0.1$ A | $m=0.0502655$ A m² per active axis |
| Bare wire diameter | $d=0.25$ mm | Copper area $0.04909$ mm²; wire length $25.13$ m per axis |
| Nominal material values | $\rho_e=1.724\times10^{-8}$ Ω m; $\rho_m=8960$ kg/m³ | $R_{DC}=8.83$ Ω and copper mass $11.05$ g per axis |
| Current applied continuously to one axis | $0.1$ A RMS | $I^2R_{DC}=0.0883$ W per active axis |
| Three axes, all continuously active | Same current on every axis | $0.265$ W DC-resistance copper-loss estimate; $33.2$ g copper total |

The material values are nominal calculation inputs, not a characterized wire grade or a guaranteed temperature coefficient. Three real orthogonal windings need different physical paths and finite winding packs; the equal-radius model is an approximation. Most mass and power of the central wearable remain unallocated. The 300 g preliminary target concerns each forearm module, not a proven mass allowance for this transmitter.

For fixed moment, turns, and wire diameter, $I=m/(N\pi a^2)$ and the idealized copper loss scales as $a^{-3}$. Halving the radius therefore raises this estimate eightfold, despite leaving the far dipole field unchanged. Doubling current/moment raises copper loss fourfold. A simulator radius sweep at **fixed moment** must not be interpreted as a free reduction in transmitter size or power.

## Inductance, voltage, and excitation

A leading thin-bundle circular-winding estimate is

$$L\simeq\mu_0N^2a\,[\ln(8a/b_{eff})-2],\qquad
|V_{coil}|\simeq I\sqrt{R_{AC}^2+(2\pi fL)^2}.$$

The effective geometric-mean winding-pack radius $b_{eff}$ is not the bare-wire radius. Higher-order geometry and internal-inductance terms are omitted; the classical circular-coil treatment is given by [Rosa and Grover, NBS, *Formulas and tables for the calculation of mutual and self-inductance*](https://nvlpubs.nist.gov/nistpubs/bulletin/08/nbsbulletinv8n1p1_A2b.pdf). Treat the following as a sensitivity illustration, not an inductance prediction for a specified winding.

With assumed $b_{eff}=1$–$3$ mm, the baseline yields approximately $L=1.34$–$1.89$ mH. At $f=10$ kHz this means $X_L=84$–$119$ Ω and $|V_{coil}|=8.5$–$11.9$ V RMS at 0.1 A. The reactive voltage is much larger than the $0.88$ V resistive drop; a low copper-watt estimate does not establish a low-voltage, efficient driver. Voltage across a winding is not necessarily the driver supply voltage. Measure impedance, mutual coupling, self-resonance, and switching transients before choosing drive electronics.

| Excitation direction | Benefit to investigate | Unresolved engineering cost |
| --- | --- | --- |
| Sequential AC axes with coherent phase reference | Simple channel attribution; both receivers observe the same slots | Settling, motion skew, reduced observation time per axis, phase/sign calibration |
| Distinct simultaneous frequencies | Reduces sequential pose skew | Frequency-dependent gain/phase calibration, intermodulation, three active axes, channel leakage |
| Resonant AC drive | May recycle reactive energy and reduce source VA burden | Frequency/tuning drift, stored voltage, switching/settling time, coil-current regulation |
| Switched/pulsed DC | Static-field measurements and transient separation are research alternatives | Offset rejection, switching transients, sensor bandwidth, eddy-current decay and time budget |

Duty cycling is not free sensitivity. With three sequential equal slots and one axis always active, the **total** ideal copper estimate is 0.0883 W, not another factor of three lower. Idle intervals reduce it further but also reduce update rate or integration time. A 50-cycle observation at 10 kHz takes 5 ms per axis: three slots require at least 15 ms, at most 66.7 complete triads/s before settling, telemetry, estimation, or rendering. A receiver moving at an assumed 1 m/s traverses 15 mm during that triad. These are timing calculations, not achieved latency or an approved update rate.

## Receiver signal and noise implications

For a small receive coil in an approximately uniform local field, Faraday's law gives

$$V_{rx,rms}=2\pi fN_{rx}A_{rx}\,|\mathbf n\cdot\mathbf B_{rms}|,
\qquad M=\frac{N_{rx}A_{rx}\,\mathbf n\cdot\mathbf B}{I}.$$

The magnitude expression describes voltage size only: the estimator needs calibrated **signed** field projections, recovered using coherent phase and known winding polarity. One receive axis can have a directional null. Three calibrated independent axes provide the complete local vector for each identified transmitter excitation. In the reciprocal linear quasistatic model $M_{12}=M_{21}$; role reversal changes wearable power, scheduling, and electronics even when the geometric coupling is reciprocal. High-impedance receivers minimize loading, but actual coil coupling and cable pickup need measurement.

An assumed $N_{rx}=100$, $a_{rx}=5$ mm gives $2\pi fN_{rx}A_{rx}=493.5$ V/T at 10 kHz: 1 nT produces 0.493 µV RMS on an aligned axis. This is not a selected receiver. The dipole baseline gives equatorial/axial field amplitudes of about 40/80 nT at 0.5 m and 5/10 nT at 1 m; individual matrix entries can be zero despite nonzero total signal.

For a resistor at temperature $T$ with effective noise bandwidth $\Delta f$, $v_J=\sqrt{4k_BTR\Delta f}$. Amplifier voltage/current noise must also be referred through the complete input impedance; see [TI AN-104, SNVA515C, revised April 2013](https://www.ti.com/lit/an/snva515c/snva515c.pdf). With **assumed** $R=100$ Ω, $T=300$ K, and $\Delta f=100$ Hz, the resistor-only value is 12.9 nV RMS, equivalent to 0.026 nT for the illustrative receive coil. It excludes amplifier noise, coherent interference, ADC noise, calibration, and imperfect demodulation. It is not evidence that the simulation's 0.1 nT noise case is achievable.

At the same coil sensitivity, the simulation's assumed 0.1/1/10/100 nT per-entry post-demodulation RMS sweep corresponds to approximately 0.049/0.493/4.93/49.3 µV RMS. Characterize actual equivalent field noise versus integration time, not merely a sensor's bandwidth-free resolution number. ADC quantization is $V_{FS}/2^b$ before analog gain; for illustration a 3.3 V, 16-bit range has a 50 µV step. Sub-microvolt signals therefore require a justified gain/noise/dynamic-range strategy. This example selects neither ADC nor amplifier. Strong near-source signals and offsets can saturate a high-gain chain.

## Frequency, distortion, thermal, and energy limits

At 10 kHz and 1 m, $2\pi fr/c\approx2.1\times10^{-4}$: propagation phase is small in air, supporting a magnetoquasistatic spatial model. It does not justify ignoring parasitic capacitance, conductive structures, or the body. For a nominal good conductor, $\delta=\sqrt{2\rho_e/(2\pi f\mu)}$ gives copper skin-depth illustrations of 2.09/0.661/0.382 mm at 1/10/30 kHz. These are material length scales, **not metal-induced position-error predictions**. Proximity losses, surrounding metal geometry, ferromagnetic permeability/hysteresis, and induced currents require measurement or a justified field solver.

The winding estimate gives no temperature rise without thermal resistance, enclosure, ambient, and fault duty cycle. Measure both coil and driver temperatures, supply input power, current waveform, and impedance over time. At a declared total load $P$, usable battery energy must satisfy $E\ge Pt/\eta$ for runtime $t$ and delivery efficiency $\eta$. An assumed 1 W load at 90% efficiency requires at least 4.44–6.67 Wh for 4–6 hours; receiver sensing, ADC, processor, radio, haptics, conversion loss, and aging reserve are not yet known. No battery is selected and no runtime or complete mass is established.

Two passive receivers can observe a single transmitter sequence without doubling field-generator copper loss. Their acquisition and telemetry power is additional. This claim depends on adequate loading isolation and shared timing; it does not establish BLE throughput or simultaneous independent pose accuracy. The [bench plan](bench-validation-plan.md) measures these unknowns before a wearable architecture decision.
