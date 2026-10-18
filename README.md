# touchstone-passivity-check

Check sampled one/two-port Touchstone S-matrix gain with an explicit singular-value report.

For: RF engineers reviewing a small exported network capture before model use. Element magnitudes alone can hide coupled gain; reviewers need the worst sampled matrix and the exact tolerance convention.

## Quickstart

Python3.10+; no runtime packages/network. Building the wheel needs setuptools from the normal Python registry.

```sh
git clone https://github.com/nripankadas07/touchstone-passivity-check.git
cd touchstone-passivity-check
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/touchstone-passivity-check example.s2p --ports 2
```

The example intentionally exits 1: sample 0 passes, sample 1 has maximum singular value 1.4 and power gain 1.96.

Windows equivalents use `.venv\Scripts\python.exe` and `.venv\Scripts\touchstone-passivity-check.exe`; Windows/macOS have not been executed by this release's Linux CI.

## Contract

ASCII Touchstone 1.0 subset, one or two ports explicitly declared with --ports. A single option line explicitly specifies frequency units, S, RI/MA/DB and shared positive real R. Two-port order is S11,S21,S12,S22. The largest eigenvalue of S^H S gives power gain; the square root must be at most 1+tolerance (default 1e-9). Reciprocity is informational, not a passivity requirement. Continuations are supported; frequency must strictly increase and may start at zero.

Report JSON goes to stdout. Exit0 means a valid report without documented findings, exit1 a valid report with findings, exit2 invalid/unsupported input or I/O failure with stderr and no partial report. This is a bounded read-only inspection tool; the optional example generator only creates an explicitly named new file.

## Limits

1 MiB, 4096 samples, numeric token length64, frequency<=1e15 Hz, shared R<=1e6 ohms, RI components/MA magnitudes<=1000, DB -600..60, MA/DB angles<=360000 degrees. Tolerance0..0.001. No Touchstone2 keywords, noise records, per-port/complex reference, impedance/gamma/modal annotations, renormalization, interpolation, causality or uncertainty assessment. Passing sampled data is not physical-device certification.

## Verify

```sh
python3 -m unittest -v test_behavior
python3 -m compileall -q .
python3 -m pip wheel --no-deps --wheel-dir dist .
python3 -m venv /tmp/touchstone-passivity-check-check
/tmp/touchstone-passivity-check-check/bin/python -m pip install --no-deps dist/*.whl
python3 verify_installed.py /tmp/touchstone-passivity-check-check/bin/python
```

Installed-command checks run outside the checkout. See [validation](VALIDATION.md), [research](RESEARCH.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), [security](SECURITY.md) and [license](LICENSE).

Original implementation, prose and invented fixtures developed with AI assistance. MIT license. No verified production adoption or performance-superiority claim.
