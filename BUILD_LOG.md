# Verified build and upload log

Date: 2026-10-19 (UTC date). Source of truth: the public GitHub repository and Actions logs.

## Remote publication

- Initial README: `6637c10f2463f2034ec68d33ff3a117fec2d327f`.
- Python engine, CLI and CI foundation: `d988c28cfadf129e990e3643b777aaf95f42277a`.
- Tests, API, security and architecture docs: `4ebd77e97b2ac3561a72eceb506ebe4d9e883de0`.
- Expanded README: `d8c7a004a66ed1ee37a69eb17942aa71f5e479ff`.
- Candidate research: `70bc09a7fb1c7fd0667b0e0f465b2ecc94a415f3`.

## Observed remote checks

On `d8c7a004`, [GitHub Actions run 39256131889](https://github.com/aradmanamnaoon/study-sentinel/actions/runs/39256131889) completed successfully:

- Python 3.11.17 install: PASS.
- `python -m pytest -q`: **15 passed, 1 dependency deprecation warning** in 1.51s.
- `python scripts/count_loc.py`: **331 first-party nonblank/noncomment Python source lines**, excluding tests, scripts, docs, blank and comment-only lines.

No performance, scientific validity, statistical calibration, deployment, dependency-security scanning, static type-checking or accessibility audit is claimed as passed.

## Known differences from initial packaged prototype

GitHub connector uploaded the working Python modules and documentation as UTF-8 files. It did **not** byte-for-byte import the original standalone ZIP from the previous chat. The example CSV and generated example reports from that ZIP are absent from the remote; `study-sentinel demo` regenerates equivalent classes of examples. Only verified remote content counts toward remote completeness.

## Incomplete work

The requested 10,000-line substantive source milestone is **not met**: verified shortfall **9,669** lines at the above audited commit. This is an early proof of concept, not the flagship release gate. Dependency versions are bounded, not fully locked. See docs/CONTINUATION.md.
