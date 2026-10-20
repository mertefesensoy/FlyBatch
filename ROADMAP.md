# Roadmap: the open areas

FlyBatch's phases A to E and G are complete (README, Status). What is left
falls into two kinds: work one maintainer cannot cover alone, listed here
for anyone to take up, and work that is blocked, listed at the end so
nobody spends time on it.

Each area names its issues. An issue labelled `good first issue` needs no
lab and no decision; one labelled `proposal` needs the owner's decision
before the work starts (CONTRIBUTING.md, "What needs no decision"). Every
result is reported with its platform, compiler and version, and float
backend, and with what it does not prove.

## 1. Platforms and compilers nobody has tried

FlyBatch's results are recorded on x86-64 Windows (MinGW gcc 6.3.0), Linux
x86-64 (gcc 15.2.0 under WSL2), Linux s390x under QEMU and MVS 3.8j under
Hercules. macOS and arm64 are untested, and no clang result is recorded.

- **Run the tester task on your setup:** the tester matrix, one issue per
  setup ([#4](https://github.com/mertefesensoy/FlyBatch/issues/4)). A result from a setup the matrix does not have is
  registered as its own verification-limit row and credited to you (SRS
  D-684, D-681).
- **A platform setting for arm64 and macOS**, and a CI runner for one
  ([#20](https://github.com/mertefesensoy/FlyBatch/issues/20), a proposal). The Makefile's `ONFPLAT` knows `x86w`, `x86l` and
  `s390x` only.
- **Other compilers:** clang on Linux ([#21](https://github.com/mertefesensoy/FlyBatch/issues/21), and [#19](https://github.com/mertefesensoy/FlyBatch/issues/19) for what the run
  manifest calls it), and a compile-only probe with tcc, Open Watcom or
  MSVC ([#22](https://github.com/mertefesensoy/FlyBatch/issues/22)).
- **Stewards.** Once someone has contributed to a platform, the owner may
  name them its steward: they review that platform's pull requests first
  and are named beside its results (SRS D-682).

## 2. A build without SoftFloat 2c

`make test-no2c` already runs every check that never compiles Berkeley
SoftFloat Release 2c, whose terms ask the user to indemnify its author (SRS
D-679). It does not test the engine. A switch that drops 2c from the engine
targets too, so an engine contributor never compiles it, is approved in
principle and needs its plan (SRS P-52).

## 3. MVS 3.8j and Hercules

For people who run their own MVS 3.8j on Hercules. All of it is emulated:
FlyBatch has not run on IBM Z hardware.

- **Another MVS 3.8j system**, such as TK4- or MVS/CE ([#31](https://github.com/mertefesensoy/FlyBatch/issues/31)), and where
  GCCMVS and JCC come from, in `docs/lab.md` ([#32](https://github.com/mertefesensoy/FlyBatch/issues/32)).
- **Widen the GCCMVS reproducer** ([#30](https://github.com/mertefesensoy/FlyBatch/issues/30)). The fault SRS VL-145 records was
  shown with one program: other structure sizes, other constants and later
  GCCMVS releases have not been tried.
- **ACC-6's Hercules CPU clock off Windows** ([#24](https://github.com/mertefesensoy/FlyBatch/issues/24), a proposal), and the
  job-card user and password, today TK5's published defaults, from the
  environment ([#26](https://github.com/mertefesensoy/FlyBatch/issues/26), a proposal).

## 4. The science, measured on x86-64

The science checks have been run on x86-64 only. Two acceptance criteria
were changed after the results were seen (SRS D-202, D-340, D-341), and
agreement with Shiu et al. is in shape, not magnitude (README, Limits).

- **A null-model control** ([#44](https://github.com/mertefesensoy/FlyBatch/issues/44), a proposal): the same measurement on a
  degree-preserving rewired copy of the 501-neuron network, to test whether
  the MN9 response depends on MaleCNS's wiring. An independent review of
  the project named its absence.
- **Review the stimulus and readout cell-type mapping** ([#27](https://github.com/mertefesensoy/FlyBatch/issues/27)).
- **Run the R2b regeneration recipe end to end**, from the MaleCNS data
  ([#28](https://github.com/mertefesensoy/FlyBatch/issues/28)), and **re-run Shiu et al.'s protocol in a brian2 environment**
  ([#29](https://github.com/mertefesensoy/FlyBatch/issues/29)).

## 5. Tooling, CI and documentation

- Checks that never run in CI ([#33](https://github.com/mertefesensoy/FlyBatch/issues/33)), the Windows TestFloat build's need
  for `rm` ([#34](https://github.com/mertefesensoy/FlyBatch/issues/34)), the claims-register check's scope ([#35](https://github.com/mertefesensoy/FlyBatch/issues/35)), and pinning
  the transitive Python packages ([#25](https://github.com/mertefesensoy/FlyBatch/issues/25)).
- Documentation a newcomer trips over: [#36](https://github.com/mertefesensoy/FlyBatch/issues/36) to [#40](https://github.com/mertefesensoy/FlyBatch/issues/40).
- The Pages site's accessibility: [#41](https://github.com/mertefesensoy/FlyBatch/issues/41) to [#43](https://github.com/mertefesensoy/FlyBatch/issues/43).

## Blocked: not open for contributions

- **z/OS and IBM CICS (phases F and H).** The project does not have IBM Z
  access yet, so there is nothing to build or test there. When that
  changes, the README will say so with a date.
- **The 3270 demonstration under INTERCOMM** cannot be reproduced from
  this repository: INTERCOMM's licence has a non-commercial clause and its
  code is kept out of the tree (SRS D-132).
