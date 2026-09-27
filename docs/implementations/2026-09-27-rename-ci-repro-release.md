# 2026-09-27: rename tidy-ups, a golden CI job, the GCCMVS reproducer, v0.5.1 preparation

| Field | Value |
|---|---|
| Date | 2026-09-27 |
| Author | Mert Efe Şensoy |
| Phase / gate | P-41 slices G (preparation only) and H; plan P-50 |
| Owner decisions relied on | D-663 (scope), D-664 (P-50 approved), D-665 (TK5 lab terms), D-666 (social preview), D-667 (golden job triggers), D-668 (CAN-14 cites VL-145); D-586, D-594, D-626, D-634, D-637, D-638, D-654 |
| Requirements touched | none; VL-127 cross-referenced, VL-142 note, VL-145 new |
| Open items closed | none |

## 1. Problem / motivation

After the rename to FlyBatch (D-637) and the outreach work of P-48, four
gaps were left, which the owner chose to close together (D-663):

1. **The rename had not reached the pictures.** The repository's social
   preview and the three live-view GIFs still said ONFLY in large type. A
   visitor's first look contradicted the page's own title.
2. **CI never checked a fingerprint.** CI's four jobs ran only what needs
   no network file (D-586), because until D-654 the networks could not be
   downloaded anonymously. The CI badge was green on a build that had not
   checked the project's central claim, the 19 golden fingerprints.
3. **The GCCMVS fault had no reproducer.** D-420 worked around a GCCMVS
   code-generation fault that turned every +0.0 in the MVS kernel into a
   subnormal, but VL-127 recorded that it was not characterised: no
   listing read, no program outside ONFLY. P-41 7.3 (a) holds the upstream
   report until a reproducer exists, and CAN-14 says "not fully
   characterised" in public.
4. **The release had no archive metadata.** P-41 G2 needs a `.zenodo.json`
   before the tag, and the release notes, the owner's Zenodo steps and the
   post-release checks had not been written.

## 2. What changed

| File | Change |
|---|---|
| `tools/liveview.py` | The frame title says FlyBatch (commit be83c58). |
| `docs/media/onfly-live-short.gif`, `onfly-live-standard.gif` | Redrawn by `make clips` with the new title (be83c58). File names kept as identifiers (D-638). |
| `docs/media/onfly-mvs-live.gif` | Redrawn from a new TK5 streaming run, followed live, with the new title. |
| `.github/workflows/ci.yml` | A fifth job, `golden`: fetch the networks from one pinned release tag, `sha256sum -c`, stage them, `make quick` strict (be83c58). |
| `README.md` | The CI badge's hover text names the golden check and says it is a smoke test (be83c58). |
| `tools/mvsgcc.py` | `--structret`: the 26-line reproducer `SR_SRC`, run under GCCMVS at `-O1` and `-O0` with the assembler listed, and under JCC, compared against the host's gcc. |
| `data/structret/gccmvs-O1.txt`, `gccmvs-O0.txt`, `jcc.txt` | The three job outputs of the reproducer, with the generated assembler. |
| `data/README.md` | A row for `structret/`. |
| `.zenodo.json` | Zenodo metadata: title, creator, MIT, a description with the third-party terms and the no-access sentence, keywords, related identifiers. |
| `docs/ONFLY-SRS.md` | D-663 to D-667 and P-50 (commit c10a3c3); VL-142's note on the golden job; VL-145; a pointer from VL-127 to VL-145. |
| `docs/plan/2026-09-27-rename-ci-repro-release.md` | The plan, P-50, approved as drafted (c10a3c3). |
| `CHANGELOG.md` | The 2026-09-27 entry gains the reproducer, the golden job, the GIFs and `.zenodo.json`. |
| `docs/plan/2026-09-24-open-source-launch.md` | CAN-14's ready phrasing, evidence and limits cite VL-145 (D-668). |
| `README.md`, `site/index.html`, `docs/architecture.md`, `docs/writeup.md` | Their account of the fault follows the new CAN-14 (D-668). |

Outside the repository and not committed: the social preview PNG (the owner
uploads it; D-594), and in the owner's private notes under `local/outreach/`
the redrafted upstream report, the v0.5.1 release notes, the Zenodo steps
and `g5-check.sh`.

## 3. Implementation approach

**The golden job** reuses what a stranger would do. It downloads
`onfnet-malecns-v1.0-srext.bin`, `onfnet-malecns-v1.0-path.bin`,
`SHA256SUMS` and `NETWORKS-NOTICE.md` from the release named by one
environment variable, `NETWORKS_TAG` (`v0.5.1-rc.1` now). It then runs
`sha256sum -c`, `tools/fixtures.py --from` and `--check`, and
`ONFLY_NOSKIP=1 make ONFPLAT=x86l PYTHON=python quick`, which builds the
engine on the three float backends and runs `tests/run_gld.py` on each. The
checksum step comes before any test, so a tampered or truncated asset fails
as a download problem, not as a fingerprint mismatch. Moving to a new
release is a one-line change.

**The reproducer, `probe_structret()`,** has this contract:

- **Input:** a running TK5 with the codepage set, as for every MVS probe in
  `tools/mvsgcc.py`.
- **Side effects:** it submits three jobs, `ONFGSR1`, `ONFGSR0` and
  `ONFJMIN`, and writes each one's full printed output to `data/structret/`.
- **Output:** exit 0 if every compiler's two lines equal the host's, and 1
  otherwise. Exit 1 is the fault reproduced, not a tool failure.
- **Invariant:** the expected values are never typed in. `sr_host()` builds
  the same `SR_SRC` with the host's gcc at `-std=c89 -O1` and runs it.

GCCCLG assembles with `PARM='DECK,NOLIST'`, so its output never showed the
generated code. The probe overrides that one step's parameter,
`PARM.ASM='DECK,LIST'`, on the EXEC card, and changes nothing else in the
procedure. JCC is driven through `tools/mvsjcc.py`'s existing mini-probe
deck, whose compile step already lists the assembler.

**The MVS GIF** was drawn the way the original was: `tools/mvsstm.py --run`
submits the streaming engine job, which writes to the `10D` punch; in
parallel, `tools/liveview.py --follow build/mvs-stream.txt --requests 5`
draws the frames as the stream arrives.

## 4. Mathematical / numerical details

The reproducer's result is a bit pattern, read as follows. `zero0` should
return two 32-bit words, both `X'00000000'`. At `-O1` its code is:

    LR    2,0              register 2 := address of the caller's result
    MVC   0(8,2),=F'0'     copy 8 bytes from the literal =F'0'

`MVC` copies exactly its length, 8 bytes. `=F'0'` is a fullword, 4 bytes, at
offset `X'54'` of the program. So bytes 4 to 7 of the result come from
offsets `X'58'` to `X'5B'`, which the listing shows to be the page-table
constant `DC A(PG0)`, the value `X'00000032'` before relocation. After the
program is loaded at address *L*, that constant holds *L* + `X'32'`. The
printed low word `X'000A5B8A'` is consistent with *L* = `X'000A5B58'`, which
is a multiple of 8, as a load address is. *L* itself was not printed, so this
last step is an inference, recorded as such in VL-145.

For ONFLY's double, the high word `0` and a low word near `X'000A....'` make
an IEEE 754 subnormal. Its exponent field is zero and its fraction is
nonzero, so its value is about 7 x 10^5 x 2^-1074, which is near 10^-318.
That is the size VL-122 observed.

## 5. Design decisions

- **Social preview content:** the logo, the name, one CAN-01 line and the
  network picture with its attribution line (D-666). Rejected alternative:
  the logo and text only.
- **When the golden job runs:** on every push and pull request (D-667), so
  that the badge means the fingerprints were checked. Rejected alternative:
  `main` and pull requests only, which saves minutes but leaves branch
  pushes unchecked.
- **One pinned tag, not the latest release:** "latest" would make an old
  commit's CI result change when a release is published. A pinned tag makes
  each commit's result reproducible. This was the engineer's choice inside
  P-50's approved text.
- **Listing through `PARM.ASM`, not a new procedure:** overriding one
  parameter keeps the reproducer on the same GCCCLG procedure a user of
  TK5 would use. A private copy of the procedure would have made the report
  depend on our copy.
- **The comparand from the host compiler:** the same reason as in every
  other `mvsgcc.py` probe. A hand-typed expected value can be wrong in the
  same way as the thing it checks.
- **CAN-14's public wording was first left alone, then changed by D-668.**
  P-50 did not authorise a claims-register change, so the commit that
  landed VL-145 kept "not fully characterised" and raised the question. The
  owner then instructed that CAN-14 cite VL-145 (D-668). The register row
  now says the fault is worked around and that a 26-line reproducer shows
  its cause, and its limits are VL-145's. The README, the site,
  `docs/architecture.md` and `docs/writeup.md` follow it. The write-up had
  to change regardless: its "there is no minimal reproducer yet" had become
  false. The write-up's new paragraph says only what the listing shows. The
  number of arguments did not matter in this program, because the
  two-argument function copies no constant. It does not claim a general
  rule.
- **Release notes, Zenodo steps and `g5-check.sh` stay in private notes**
  (P-50 R4). Nothing is published before W1a and the owner's word.

## 6. Verification

Every result below was produced on 2026-09-27 in the session that made the
change.

| # | Exit (P-50 Section 4) | Command | Result |
|---|---|---|---|
| V1 | X3 | `python tools/mvsgcc.py --structret`, TK5 MVS 3.8j under Hercules 4.9.1 | `gccmvs-O1 zero0 hi=00000000 lo=000A5B8A WRONG`; `gccmvs-O1 make2 ... ok`; `gccmvs-O0` both `ok`; `jcc` both `ok`; `host gcc: make2 hi=00000000 lo=00000000, zero0 hi=00000000 lo=00000000`; exit 1, the fault reproduced. Jobs `ONFGSR1` 424, `ONFGSR0` 425, `ONFJMIN` 426. An earlier run in the same session, without the listing, gave the same values |
| V2 | X1 | `python tools/mvsstm.py --run` and, in parallel, `python tools/liveview.py --follow build/mvs-stream.txt --requests 5 --every 8 --fps 10 --timeout 1500 --save <gif>`, TK5 under GCCMVS `-O1`, SOFT2C | `ONFERUN` JOB 427, every step `COND CODE 0000`, `ONF302I STEP SUMMARY: 5 OK, 0 WARN, 0 ERROR`, 19,909 lines, longest 80 columns, `LIVE`, G-15 to G-19 `AGREE`; `liveview: 5 of 5 requests seen`, `every fingerprint matches Section 8.4`. The GIF is 864 x 460, 130 frames at 100 ms, like the one it replaces. A middle frame compared by eye with the old one differs only in the title, now `FlyBatch - SUGR 200 Hz, seed 1, K=50` |
| V3 | X2 | CI run 36322849500 on be83c58 | Five jobs `success`. In `golden`: `gcc version 13.3.0 (Ubuntu ...)`, `onfnet-malecns-v1.0-srext.bin: OK`, `onfnet-malecns-v1.0-path.bin: OK`, `run_gld [SOFT3E backend]: 20 passed, 0 failed`, the same on NATIVE and SOFT2C, `ONFLY test: 2 PASS, 0 SKIP, 0 PENDING, 0 EXEMPT` |
| V4 | X1 | GraphQL `usesCustomOpenGraphImage`, `openGraphImageUrl`; the image fetched and compared with the file built | `true`; 1280 x 640, pixel-equal to the FlyBatch preview built under D-666 |
| V5 | X1 | `gh repo view --json repositoryTopics` | 15 topics, including `mainframe`, `jcl`, `tk5`, `mvs38j` |
| V6 | X4 | `python -m json.tool .zenodo.json` | valid |
| V7 | X5 | `ONFLY_NOSKIP=1 mingw32-make test`, x86-64 Windows 11, MinGW.org gcc 6.3.0 | exit 0, `ONFLY test: 29 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT` |
| V8 | D-665 | `script scripts/shutdown` on the Hercules console | no `hercules` process, ports 8038 and 3505 closed, the log ending `HHC01422I Configuration released` |

**What this does not prove.**

- V1 is **one program on one lab**, TK5 under Hercules, GCCMVS 3.2.3 and
  JCC 1.50.00. The code generator's rule was not read. The load address
  behind `000A5B8A` is inferred. Other structure sizes, other constants and
  later GCCMVS releases were not tried (VL-145).
- V2's timings (first `ONFSC` at +42.1 s, END banner at +1460.4 s, 1033 of
  1033 writes before it) are a **confirmation, not a reported liveness
  figure**, as D-441 ruled for the last such run. The host was also running
  `make test` at the time. Section 9.2 keeps run 1 and run 4.
- V3 is a smoke test on GitHub's gcc 13.3.0, a compiler with no row in
  Section 8.3. It is a new data point, not matrix evidence (D-586, VL-142).
- V2 covers `srext` only, as every MVS stream run has.
- Nothing here ran on IBM Z hardware; the project has no IBM Z access yet
  (VL-139).

## 7. Related docs

- `docs/plan/2026-09-27-rename-ci-repro-release.md` (P-50)
- SRS A.1 D-663 to D-667; Appendix D VL-122, VL-123, VL-127, VL-142, VL-145
- `docs/plan/2026-09-24-open-source-launch.md` (P-41): slice G, 7.3 (a), CAN-14
- `docs/implementations/2026-09-17-phase-g-stage5-mvs-live-view.md`, where
  the MVS GIF was first drawn
- `docs/implementations/2026-09-27-open-source-outreach.md` (P-48)
