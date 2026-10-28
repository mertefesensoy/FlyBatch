# Changelog

Entries are grouped by release, newest first; work after the latest release
sits under **Unreleased**. Each entry names the decision rows of the specification,
[`docs/ONFLY-SRS.md`](docs/ONFLY-SRS.md), that record it, and the date is
the day the work was recorded as complete. The phase letters are labels, not
an order (SRS Section 9.2).

FlyBatch has not run on IBM Z hardware, and the project does not have IBM Z
access yet (SRS VL-139). Every MVS result comes from MVS 3.8j under the
Hercules emulator, and every s390x result from Linux under QEMU, both on one
x86-64 laptop.

## Unreleased

Nothing yet.

## 0.5.1, 2026-10-29

The first release. The engine prints version 0.5.1 (D-573, D-634); every
entry below, back to the start of the project, is part of it.

### 2026-10-29

- The first release, `v0.5.1`, with the two networks, `SHA256SUMS` and
  `NETWORKS-NOTICE.md` as assets, the same files the release candidate
  `v0.5.1-rc.1` carried. The tester matrix, #4, stays open and now tests
  this release; README, `REPLICATING.md`, `docs/testers.md` and
  `SECURITY.md` point at it, and `CITATION.cff` carries its version (D-695).

### 2026-10-20

- Easier to join: the README opens with a summary line, the live view and a
  "Get involved" section; CONTRIBUTING.md opens with a welcome, says what
  needs no decision, who reviews pull requests, how contributors are
  credited and how they may use AI tools; `ROADMAP.md` lists the open
  areas; the first reply on a `good first issue` or a first pull request
  comes within 3 days (P-51, D-677, D-680 to D-686).
- `NO2C=1` builds and tests the engine on SoftFloat 3e and native without
  compiling Berkeley SoftFloat Release 2c, for anyone who does not accept
  its terms; `make test-no2c` is now `make NO2C=1 test-nonet` (D-679,
  D-690, D-692). Each 2c half left out is counted, and the closing line
  reads `ONFLY test NO2C=1:`, never the full suite's form (D-691). A
  seventh CI job, `no2c-linux`, runs it on every push (D-693).
- A dev container for GitHub Codespaces, pinned by digest, fetches and
  checks the two networks; a sixth CI job runs it on every push (D-678).
- The tester round for `v0.5.1` is public: one issue per setup, and a
  tracking issue, #4. With them, 26 contributor issues, 12 of the 41 labelled
  `good first issue`: #4 to #44 (D-676, D-683, D-687).
- The Pages site has a descriptive title and description, a canonical link
  and a link card; `CITATION.cff` and `.zenodo.json` cite Shiu et al. by DOI
  (D-688).

### 2026-09-27

- A GCCMVS code-generation fault, found in 2026-09 and worked around then,
  now has a 26-line reproducer outside FlyBatch,
  `python tools/mvsgcc.py --structret`. Its job outputs, with the generated
  assembler, are in `data/structret/`. At `-O1` an eight-byte structure of
  zeros is copied from a four-byte literal; `-O0` and JCC are right
  (VL-145). The README, the site and the write-up now say so (D-668).
- CI gained a `golden` job: on every push it downloads the two networks
  from a pinned release, checks their SHA-256 values and compares all 19
  golden fingerprints, on GitHub's compiler, as a smoke test (D-667,
  VL-142).
- The live-view animations say FlyBatch; the MVS one was redrawn from a new
  run on the emulated MVS lab. `.zenodo.json` describes the archive a
  release will make (P-50, D-663 to D-666).
- The project is renamed FlyBatch; it was called ONFLY. The program names
  ONFLYENG and ONFLYDRV, the ONF message prefix and the specification's file
  name are unchanged. The repository is now
  github.com/mertefesensoy/FlyBatch, and GitHub redirects the old address
  (D-636 to D-638).
- The FlyWire-derived material, the Shiu reference curve and the files that
  embed it, is offered under CC BY-NC 4.0; the network files stay under
  CC BY 4.0 (D-625). The first tag will be `v0.5.1` (D-634).
- Records written from now on store paths relative to the repository
  (D-635).
- A visual tour in the README, an architecture explainer with diagrams
  (`docs/architecture.md`), a picture of the subcircuit, two terminal
  demonstrations, captures from the emulated MVS lab, a FAQ and a write-up;
  `make test` holds the FAQ and the write-up to the claims register
  (D-621 to D-623, D-627, D-628, D-643, D-650).
- A GitHub Pages site built from them, `site/` (D-627, D-630).
- The site's favicon, a fruit fly on a stack of punched cards, the fly as a
  batch job, is the project's logo: at the head of the README with CI,
  site, licence and release badges, and in the site's top bar
  (D-657 to D-662).
- A guide for testers of the release candidate `v0.5.1-rc.1`,
  `docs/testers.md` (D-626).
- Found: the 3270 transaction shows a stale answer when a request repeats
  the last one run (VL-144).
- Phase E's acceptance criteria were re-evidenced on engine 0.5.1, and rows
  6 and 7 of the determinism matrix cover all nineteen golden requests on it
  (D-605 to D-616, VL-143).

### 2026-09-26

- Community files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  `SUPPORT.md`, issue and pull request templates, `CITATION.cff`, this
  changelog and a `.mailmap` (launch plan P-41, slice F; D-576 onward).
- ONFLYENG enforces FR-LOD-04's memory limit: 8,388,608 bytes on MVS 3.8j,
  no limit elsewhere. The engine version it prints is 0.5.1 (D-564 to D-575,
  VL-141).
- Replicability: `requirements.txt`, a strict test mode (`ONFLY_NOSKIP=1`),
  a counted `make test` closing line, a Linux x86-64 build (`ONFPLAT=x86l`)
  and `REPLICATING.md` (P-41 slice E, D-542 to D-563, VL-140).
- Licence and notices: `LICENSE` holds the MIT text alone,
  `THIRD_PARTY_NOTICES.md` is the register of third-party terms, and
  `REUSE.toml` annotates every path; the README and `docs/overview.md` give
  the public account (P-41 slices C and D, D-513 to D-541).

### 2026-09-25

- A committed guard keeps one name out of the repository's text (P-41
  slice B, D-500 to D-512).

### 2026-09-24

- Section 8.3's row 7, MVS 3.8j under the JCC compiler, covers all nineteen
  golden requests (D-468 to D-473, VL-138).

### 2026-09-18

- Phase G, the transaction demonstrator, is complete (D-442). A transaction
  written in `EXEC CICS` runs on x86-64 Windows under Raincode, not under
  IBM CICS; a 3270 session under INTERCOMM on the emulated MVS system starts
  a run and shows its result; and a live view draws the engine's streamed
  output.

### 2026-09-16

- Phase E, the MVS MVP, is complete (D-348): acceptance criteria ACC-1 to
  ACC-7 pass. ACC-1 to ACC-4 are x86-64 results. Two criteria were changed
  after the results were seen: ACC-3 no longer tests 10 Hz, and ACC-4 no
  longer tests magnitude (D-202, D-340, D-341, D-448).

### 2026-09-14

- Phase A, foundations, is complete (D-252).
- Phase D, big-endian, is complete (D-234): the engine builds and passes
  its tests on Linux s390x under QEMU.

### 2026-09-13

- Phase C, science on x86-64, is complete (D-206): the synaptic weight is
  calibrated for MaleCNS and the 501-neuron subcircuit is admitted as the
  MVP network (D-205).

### 2026-09-10

- Phase B, the engine and the Python reference on x86-64, is complete
  (D-47).
