# Plan: rename tidy-ups, golden CI, the GCCMVS reproducer, v0.5.1 prep (2026-09-27)

| Field | Value |
|---|---|
| Scope | D-663: four workstreams chosen by the owner after P-48 |
| Decisions it rests on | D-586 (CI is smoke tests, never Section 8.3 evidence), D-594 and D-595 (the social preview is uploaded by the owner), D-626 and D-654 (the pre-release and its assets), D-634 (first tag `v0.5.1`), D-637 and D-638 (the rename's reach), D-646 (P-49, row L11), D-420 and VL-127 (the GCCMVS fault), P-41 slice G and 7.3 (a) |
| Proposal | P-50 |
| Status | APPROVED as drafted 2026-09-27 (D-664); Q2 to Q4 answered as D-665 to D-667 |

## 1. What the survey found

| # | Finding |
|---|---|
| S1 | The repository's social preview is custom (`usesCustomOpenGraphImage` true) and still reads **ONFLY** in large type beside a live-view frame (D-595's image). The API cannot set it (D-594) |
| S2 | `tools/liveview.py:475` draws the title "ONFLY - SUGR ... Hz" into every frame, so the three GIFs the README and the site show say ONFLY: `onfly-live-short.gif` and `onfly-live-standard.gif` come from `make clips` on x86-64; `onfly-mvs-live.gif` was drawn from a stream recorded on TK5 by `tools/mvsstm.py`, and that recording is not in git, so redrawing it needs one TK5 streaming run |
| S3 | The repository has 11 topics; P-49 row L11, adopted by D-646, adds `mainframe`, `jcl`, `tk5` and `mvs38j` |
| S4 | CI runs four jobs, none with a network file (D-586, VL-142). Since D-654 the two networks can be downloaded anonymously from `v0.5.1-rc.1`, which is what P-41 G5 waited for to add a `golden` job |
| S5 | The GCCMVS fault behind CAN-14 has no minimal reproducer (VL-127), and P-41 7.3 (a) holds the upstream report until one exists. `tools/mvsgcc.py` already probes GCCMVS on TK5 by small embedded C programs compared against values computed on x86 |
| S6 | Slice G's release needs: W1a's corrections, Zenodo switched on before the tag (G2; the owner's Zenodo login), a `.zenodo.json`, release notes, `CITATION.cff`'s `version` key (D-587), and the post-release checks (G5) |

## 2. Workstreams

**R1, rename tidy-ups.** (a) A new social preview, 1280 by 640, built by the
engineer as Q3 chooses and left outside the repository for the owner to
upload, then read back. (b) `liveview.py`'s title says FlyBatch; `make
clips` redraws the two x86-64 GIFs; one TK5 run of `tools/mvsstm.py --run`
and `liveview.py --follow --save` redraws the MVS one. File names stay, as
identifiers (D-638). (c) `gh repo edit mertefesensoy/FlyBatch --add-topic
mainframe,jcl,tk5,mvs38j`, run by the engineer and read back.

**R2, a golden CI job.** A fifth job in `.github/workflows/ci.yml` on
ubuntu-latest: download the two networks, `SHA256SUMS` and
`NETWORKS-NOTICE.md` from one pinned release tag (`v0.5.1-rc.1` now, moved
by one line at each release), `sha256sum -c`, `tools/fixtures.py --from`,
then `ONFLY_NOSKIP=1 make ONFPLAT=x86l PYTHON=python quick`, which builds the
engine and checks all 19 golden fingerprints. It stays a smoke test on
GitHub's compiler, never Section 8.3 evidence (D-586); the CI badge's hover
text and VL-142 say so. The triggers are Q4's.

**R3, the GCCMVS reproducer.** Test first, as for any MVS probe: a probe in
`tools/mvsgcc.py`, a C89 program of about 20 lines comparing a no-argument
function that returns a two-word structure with the same structure returned
from a two-argument function, each printed as hex against the value computed
on x86. On TK5 it runs under GCCMVS at `-O1` (the level ONFLY uses) and at
`-O0` if that compiles, keeping the generated assembler, and under JCC. The
listings are committed beside the probe; the result becomes VL-145; P-41
7.3 (a)'s upstream report is redrafted around it in the owner's private
notes. Nothing is sent: the upstream report is wave W1b, after the release.

**R4, v0.5.1 release preparation.** A `.zenodo.json` as P-41 G2 describes
(MIT for FlyBatch's code, and the third-party terms: SoftFloat 2c's, CC BY 4.0
for the networks, CC BY-NC 4.0 for the FlyWire-derived material); release
notes for `v0.5.1` in the private notes; the owner's Zenodo steps written out;
and the G5 checks scripted. No tag, no release, no Zenodo switch: those wait
for W1a and for the owner.

**Closing.** `ONFLY_NOSKIP=1 mingw32-make test`; the name guard; no em
dashes; an implementation doc; push; `main` fast-forwarded (D-619).

## 3. Proposed text changes

| # | Where | Change |
|---|---|---|
| T1 | SRS A.1, A.2 | D-rows for the owner's answers; P-50 |
| T2 | SRS Appendix D | VL-145, the reproducer's result; VL-142's note on the golden job |
| T3 | `README.md`, `CONTRIBUTING.md`, `docs/testers.md` | Where they name CI's four jobs, five; the CI badge's hover text |
| T4 | `THIRD_PARTY_NOTICES.md` | Nothing new unless a new tool is used |

No requirement text changes.

## 4. Exit

| # | Criterion | Evidence |
|---|---|---|
| X1 | The social preview uploaded by the owner reads FlyBatch; the three GIFs say FlyBatch; the four topics present | GraphQL `usesCustomOpenGraphImage` and the image fetched; the GIFs' frames; `gh repo view --json repositoryTopics` |
| X2 | The `golden` job passes on the pushed branch and on `main` | `gh run view` with five jobs `success` |
| X3 | The reproducer ran on TK5 under GCCMVS, and JCC, with its listing kept and VL-145 written | the job output against the x86 values |
| X4 | `.zenodo.json` committed and its JSON valid; notes and steps ready | `python -m json.tool .zenodo.json` |
| X5 | Suite and checks pass; pushed; `main` fast-forwarded | `make test`, CI, `git rev-parse origin/main` |

## 5. What this will not prove

A green `golden` job on GitHub's gcc is a new data point, not a matrix row
(D-586). The reproducer characterises one GCCMVS behaviour on Hercules, not
IBM hardware. Nothing about the science changes.

## 6. Questions for the owner

| # | Question | Options | Recommendation |
|---|---|---|---|
| Q1 | This plan | Approve; change; discuss | Approve |
| Q2 | Lab terms for R1 (b) and R3 | Start TK5 detached, run the jobs without changing Hercules' configuration, shut it down at the end without a further question, as D-632; ask at each start and stop | As D-632 |
| Q3 | The social preview's content | The logo, the name, one line from CAN-01 and the network picture with its attribution line; the logo, the name and the line only | The first: it shows what the project simulates |
| Q4 | When the `golden` job runs | Every push and pull request, like the other four; only `main` and pull requests | Every push: that is what makes the CI badge mean it |
