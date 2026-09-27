# Changelog

FlyBatch has no release yet, so every entry sits under **Unreleased**, newest
first. Each entry names the decision rows of the specification,
[`docs/ONFLY-SRS.md`](docs/ONFLY-SRS.md), that record it, and the date is
the day the work was recorded as complete. The phase letters are labels, not
an order (SRS Section 9.2).

FlyBatch has not run on IBM Z hardware, and the project does not have IBM Z
access yet (SRS VL-139). Every MVS result comes from MVS 3.8j under the
Hercules emulator, and every s390x result from Linux under QEMU, both on one
x86-64 laptop.

## Unreleased

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
