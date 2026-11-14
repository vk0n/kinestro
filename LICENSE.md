<!--
SPDX-FileCopyrightText: 2026 Vladyslav Kononiuk
SPDX-License-Identifier: CC-BY-4.0
-->

# Kinestro licensing

Kinestro — Wearable Spatial Input System is an open-source hardware and software project implementing Cyberdirigokinesis — Natural Spatial Human–Computer Interaction. The owner-approved policy is **openness with reciprocity**, with permissively reusable documentation subject to attribution.

## Approved policy and current scope

| Material | Approved license | Application |
| --- | --- | --- |
| Software and firmware authored for Kinestro | [Mozilla Public License 2.0](LICENSES/MPL-2.0.txt) (`MPL-2.0`) | Covers the current isolated E1 Python research code/tests and associated dependency/ignore files; apply explicitly to future original software/firmware files when added. |
| Original open hardware design source files | [CERN Open Hardware Licence Version 2 — Weakly Reciprocal](LICENSES/CERN-OHL-W-2.0.txt) (`CERN-OHL-W-2.0`) | Apply explicitly to original hardware design sources when they are added. |
| Project-authored documentation | [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt) (`CC-BY-4.0`) | Applies to the current documentation through each file's SPDX header. |

The current repository contains documentation and isolated numerical Python research, with explicit file-level licensing. It contains no production application, firmware, drivers, or hardware design sources. The approved policy guides future contributions; storing a license text does not license files that do not yet exist. It also does not make every file available under all three licenses. Future source files must receive their own appropriate licensing information when created.

Current project-authored Markdown files, including `README.md`, `AGENTS.md`, this overview, and documentation under `docs/` and `research/`, are licensed under `CC-BY-4.0`. Original derived synthetic E1 CSV/JSON/SVG report artifacts are narrowly assigned CC-BY-4.0 through the research directory's `REUSE.toml`; this does not assign licensing to external or participant datasets. Source snippets or external materials added later require their own appropriate treatment; file extensions alone do not determine their license.

## Permissions and obligations

All three approved licenses permit commercial use under their terms. These summaries explain the selection; the complete linked license texts govern.

- **Software and firmware:** MPL-2.0 provides file-level reciprocity. Distributed covered source and modifications remain available under MPL-2.0; distribution of covered executable code requires making the covered source available as specified in section 3.2. Larger works may combine MPL-covered files with separately licensed material under section 3.3. Preserve required notices. This policy adds no Exhibit B notice or other restrictions.
- **Hardware design sources:** CERN-OHL-W-2.0 provides weak reciprocity for covered design sources and products. Preserve notices, identify modifications, and provide the required Complete Source and Source Location information when conveying modified sources or products, as applicable under sections 3 and 4. The definitions of Complete Source, Available Component, and External Material determine the reciprocal scope; this is not a requirement to relicense every independent component in a larger system.
- **Documentation:** CC-BY-4.0 permits sharing and adaptation, including commercial reuse. When sharing, retain supplied attribution, notices, and license information, link to the material where reasonably practicable, and indicate modifications as required by section 3. There is no ShareAlike requirement. Do not add downstream restrictions contrary to the license.

## Attribution and file-level metadata

The owner has confirmed **Vladyslav Kononiuk** as the name to use for current documentation attribution. The documentation was created in **2026**, as recorded in the repository history. Current documentation headers therefore identify `2026 Vladyslav Kononiuk` and `CC-BY-4.0`. This does not assert ownership of third-party works or future contributors' contributions.

When reusing current documentation, identify the work as **Kinestro documentation**, attribute **Vladyslav Kononiuk**, link to the [project repository](https://github.com/vk0n/kinestro) and [CC-BY-4.0](LICENSES/CC-BY-4.0.txt), and identify your changes where applicable. These are attribution details for applying the license, not additional licensing conditions.

For each future project-authored file, include the appropriate SPDX license identifier and verified copyright notice. Prefer unobtrusive HTML comment headers for Markdown. Use adjacent `.license` files for formats that cannot carry comments, or narrowly scoped `REUSE.toml` annotations when justified. Preserve existing third-party notices and distinguish separately licensed snippets. No blanket future-directory classification is introduced by this foundation.

## External materials, data, and branding

- Third-party dependencies and contributed external materials retain their applicable licenses and attribution requirements. Review provenance and compatibility before inclusion; this overview does not relicense them.
- Referenced papers, datasets, web pages, and other linked resources are not relicensed by Kinestro's documentation license. Official license texts in `LICENSES/` are reproduced unchanged under their own terms, not relicensed as project documentation.
- Datasets and physiological/video recordings require separate licensing, privacy, consent, retention, and publication decisions before release. Neither the documentation policy nor the software/hardware policy assigns a default license to those data or supplies participant consent.
- Copyright licensing of a file does not automatically license **Kinestro**, **Cyberdirigokinesis**, names, logos, or branding as trademarks, or imply endorsement. This statement creates no additional restriction on rights the approved licenses grant.

## License text provenance and REUSE status

The complete, unmodified plain-text licenses are copied from the SPDX License List's maintained [license-list-data](https://github.com/spdx/license-list-data) repository:

| Local text | SPDX source |
| --- | --- |
| [CC-BY-4.0](LICENSES/CC-BY-4.0.txt) | [Canonical text](https://raw.githubusercontent.com/spdx/license-list-data/main/text/CC-BY-4.0.txt) |
| [MPL-2.0](LICENSES/MPL-2.0.txt) | [Canonical text](https://raw.githubusercontent.com/spdx/license-list-data/main/text/MPL-2.0.txt) |
| [CERN-OHL-W-2.0](LICENSES/CERN-OHL-W-2.0.txt) | [Canonical text](https://raw.githubusercontent.com/spdx/license-list-data/main/text/CERN-OHL-W-2.0.txt) |

License texts carry no added Kinestro headers. Per-file documentation headers make the current assignments explicit without a global override that could accidentally cover external material.

At the owner's request, license texts were included ahead of software and hardware sources. MPL-2.0 now covers the E1 research code; CERN-OHL-W-2.0 still has no covered hardware source files. [REUSE Specification 3.3](https://reuse.software/spec-3.3/#license-files) disallows unused license texts; this deliberate remaining policy exception prevents claiming full REUSE compliance. Report `reuse lint` results honestly. Do not label documentation with unrelated licenses or create placeholder source files merely to silence an unused-license finding. Recheck when real hardware files are introduced. The original documentation-only context remains historical in ADR-0006.

See [ADR-0006](docs/adr/0006-open-source-licensing.md) for the decision and its relationship to the historical licensing deferral.
