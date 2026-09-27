# 2026-09-27: Phase E re-evidenced on the 0.5.1 engine

| Field | Value |
|---|---|
| Date | 2026-09-27 |
| Author | Mert Efe Şensoy (owner); engineering session under the owner's decisions |
| Phase / gate | Phase E (COMPLETE since D-348), re-evidenced; no phase opens or closes (D-605) |
| Owner decisions relied on | D-605 to D-616 (this session); D-474 to D-476, D-526, D-570, D-573 as precedent and context |
| Requirements touched | ACC-1 to ACC-7; ACC-5's Section 8.3 rows 1, 2, 3, 3b, 4, 5, 6 and 7; TX-01 (MVS half), TX-02, TX-04; NFR-PERF-01, NFR-PERF-02, NFR-OBS-01; FR-BAT-01, FR-BAT-04, FR-BAT-06; SR-CAL-05 (reporting). Code: `prep/acc4.py` (D-612) |
| Open items closed | none |

## 1. Problem / motivation

`ONF_ENGVER` moved from 0.5.0 to 0.5.1 on 2026-09-26 (D-573), together with
`ONF_MEMLIM` (D-567, D-568) and, under JCC only, `ONF_MAXPAY`'s MVS bound
(D-572). That session re-ran Section 8.3 row 6's `srext` half and TE-08 on
TK5 and recorded rows 4, 5, 7 and row 6's `path` half as not re-run (D-570);
D-576 left them so. ACC-6 and ACC-7 had last run on 0.5.0 (JOB 403 and JOB
404, 2026-09-25).

So the engine a first tag (P-41 slice G) would carry had never been measured
on most of the matrix ACC-5 names. Row 7 was the most exposed: D-572 changed
JCC's object code, and no JCC build of 0.5.1 existed.

## 2. What changed

| File | Change |
|---|---|
| `prep/acc4.py` | `--out` (D-612): `output_path()` resolves the record a measuring run writes before the run starts, and refuses `acc4.json`, which D-526 keeps as written; `build_parser()` split out of `main()` so the option can be tested |
| `tests/test_disc.py` | Class `OutPath`, eight checks, written first and shown failing (8 of 8) before the change |
| `data/calibration/acc4-v051.json` | New: this session's full-brain ACC-4 re-measurement (D-609, D-612) |
| `data/calibration/acc1-candidate.json`, `acc3-srext.json` | Rewritten in place by their tools (D-613); `elapsed_s` is the only field that moved |
| `data/phase-e/v051/mvs/` | New (D-610): row 6's GCCMVS recordings and listings, both halves, and the ACC-6 and ACC-7 listings and tool output |
| `data/phase-e/v051/jcc/` | New (D-610): row 7's JCC recordings and listings, both halves |
| `docs/plan/2026-09-27-phase-e-reevidence-051.md` | P-47, the plan of record (D-608), with the answers appended |
| `docs/ONFLY-SRS.md` | D-605 to D-616 in A.1; P-47 in A.2; VL-143 in Appendix D; a dated note on Section 9.2's Phase E row, authorised by D-616 |
| `docs/implementations/2026-09-27-phase-e-reevidence-051.md` | This document |

## 3. Implementation approach

Every criterion was re-run, none cited. The order, fixed by P-47 and D-609:

1. **L0**, the strict x86-64 suite, before anything else.
2. **L1**, the science on x86-64 before any lab started, so the two-hour
   ACC-4 campaign contended with no TK5 job: ACC-1 and ACC-2, ACC-3, then
   ACC-4 re-measured on the full brain from MaleCNS feathers staged and
   verified by `tools/fixtures.py` and removed afterwards (D-614).
3. **L2**, TK5: this tree's ONFLYENG and ONFLYDRV installed first, because
   BUZZ and TX-04 run whatever is installed in `HERC01.ONFLY.LOADLIB`; then
   ACC-6 alone on a quiet host; ACC-7; and each half of rows 6 and 7, each
   judged by the tools' own comparisons against the x86-64 recording
   (`data/phase-d/x86w`) and Section 8.4.
4. **L3**, the s390x guest's `make test`, overlapping L2's `path` runs once
   ACC-6 had landed (D-611).

**Which engine ran is read, not assumed.** Every MVS listing's NFR-OBS-01
manifest was read for `ENGINE VERSION 0.5.1` and its compiler line. BUZZ and
TX-04 print no listing file of their own, so their listings were cut from
TK5's printer file (`prt/prt00e.txt`) by job **number** as well as name, with
a scratch helper using the START and END JOB banner patterns
`mvsjcc --recover` uses; JES2 repeats the START banner on the separator
page, so the cut runs from the job's first START to its last END.

**`output_path(out, variant)`** (D-612). Inputs: the `--out` argument or
`None`, and the `--variant` name or `None`. Output: the path the run's JSON
is written to. Without `out` it is exactly what it always was, `acc4.json` or
`acc4-<variant>.json`; with `out`, a bare name is under `data/calibration/`
and a path with a directory is used as given, `out` winning over the variant
default. No side effects. It raises `SystemExit` when `out` resolves to
`acc4.json` (compared by normalised absolute path, so every spelling is
caught) or names a directory that does not exist. Both checks run before
the network is emitted, because the run is two hours long and a typo would
otherwise surface only at its last line.

## 4. Mathematical / numerical details

No formula changed. ACC-4 is computed exactly as Section 6.4 states it since
D-341 and D-448: per validation rate r, ONFLY's mean MN9 rate m_r, its
standard deviation s_r and standard error se_r = s_r / sqrt(n) over n = 30
seeds (D-353); the shape clause holds when m_r − m_r' ≤ se_r for each
successive pair r < r', and the onset clause when the lowest rate with
m_r > 1 Hz is within one sampled rate of the reference's. The magnitude
comparison |m_r − ref_r| ≤ max(0.25·ref_r, 2 Hz) is reported, not tested.

**Reproduction is judged by equality, not tolerance.** The re-measurement is
compared field by field with VL-97's record using Python `==` on the parsed
JSON numbers, so a difference in the last bit of any mean, deviation or
standard error would show. All 40 per-rate fields are equal.

## 5. Design decisions

| Question | Chosen | Alternatives | By |
|---|---|---|---|
| Scope | Phase E re-evidenced on 0.5.1 | FR-CAL-01 stretch; slice G items 11 and 22; Phase F (not runnable) | D-605, owner |
| ACC-4 route | Re-measure on the full brain | Re-evaluate VL-97's record (the engineer's recommendation) | D-609, owner, against the recommendation |
| Where ACC-4's record goes | New `acc4-v051.json` via `--out` | Move after the run; overwrite `acc4.json`, superseding D-526 | D-612, owner |
| ACC-1 to ACC-3's records | Rewritten in place | `-v051` copies | D-613, owner |
| Staging the full brain | Verified feathers, removed after | Kept; an unverifiable copied cache | D-614, owner |
| Where TK5 recordings go | `data/phase-e/v051/` | `build/` only; overwrite the 0.5.0 recordings | D-610, owner |
| Lab terms | Start, run freely, overlap after ACC-6, shut down at the end | Ask at shutdown; no overlap | D-611, owner |
| The s390x exit status the first wrapper failed to capture | Re-run with a corrected wrapper | Accept the exit status as inferred from `tools/testrun.py` | D-615, owner |
| Section 9.2's Phase E row | A dated note, text shown in full first | No Section 9.2 change | D-616, owner |
| Cutting listings by job number | Engineer's choice | By job name only, which can pick an older run | engineer |
| `--jobs 14` for ACC-4 with 2 GB available | Engineer's choice, as VL-97 ran it; results do not depend on it | Fewer workers | engineer |

## 6. Verification

Every result below was run in the 2026-09-27 session (UTC times; the host is
UTC+3). Platform, compiler and float backend are stated for each.

### 6.1 L0, x86-64 (Windows 11, MinGW.org gcc 6.3.0, GNU Make 3.82.90, Python 3.13.14)

    ONFLY_NOSKIP=1 mingw32-make test

21:08:42Z to 21:20:42Z, `MAKE_EXIT=0`, closing `ONFLY test: 28 PASS, 0 SKIP,
0 PENDING, 3 EXEMPT`. `run_gld` 20 passed on each of SOFT3E, NATIVE and
SOFT2C; `cmpgld: SOFT3E, NATIVE, SOFT2C agree on all 19 golden requests
across 2 networks`; `cmpchk [FR-SIM-10 chunk invariance]: 24 passed`;
`run_tt02: 18 of 18 operation runs passed, 781128 cases checked`;
`run_mvsrun: 62 passed`; `run_mvsjcc: 53 passed`. This gives ACC-5 rows 1
(the Python oracle), 2 (NATIVE), 3 (SOFT3E) and 3b (SOFT2C). **Three** checks
are exempt, not the five D-575 expects of a clone: this worktree carries the
owner's ignored `local/onflytx/`, so `ic3270`'s two D-132 checks ran and
passed instead of being exempt.

### 6.2 L1, x86-64 science (the same host and compiler, NATIVE, `build/runnet.exe` rebuilt from this tree)

| Criterion | Command | Result |
|---|---|---|
| ACC-1, ACC-2 | `python prep/extract.py --acc1 data/networks/onfnet-malecns-v1.0-srext.bin --label srext --jobs 14` | `ACC-1 PASS over the rates it applies to: [40, 60, 120, 200]` (13.77, 28.88, 72.07 and 91.35 Hz, 30 of 30 seeds each); `ACC-2 PASS: rate 0 produced 0 spikes across all 501 neurons`; 49 s |
| ACC-3 | `python prep/extract.py --acc3-file data/networks/onfnet-malecns-v1.0-srext.bin --label srext --jobs 8` | `ACC-3 PASS`; margins 0.85, 2.34, 3.16 and 6.33 Hz at 40, 60, 120 and 200 Hz; 40 Hz named within the reference's precision (standard error 1.54 Hz, D-357); 10 Hz excluded and reported, reference 3.67 ± 4.22 Hz, subcircuit 0.02 Hz (D-202); 79 s |
| ACC-4 | `python prep/acc4.py --jobs 14 --out acc4-v051.json` | Full 184,099-neuron network emitted at W_syn 0.2969, SHA-256 `aaa825c2...8af1`, the digest in VL-97's record; 150 runs plus rate 0 in 5,564 s; `ACC-4 shape PASS (onset onfly 10 Hz, reference 40 Hz: PASS); ACC-4 PASS`; magnitude reported outside tolerance at 10 Hz (+3.67) and 40 Hz (+9.62); ACC-2 at rate 0 `[0, 0]`; all 40 per-rate figures equal to `acc4.json`'s |
| `--out` | `python tests/test_disc.py` | 8 new checks failed before the change (`FAILED (errors=8)` of 18) and all 18 pass after |

The records' diffs: `acc1-candidate.json` `elapsed_s` 54 to 49,
`acc3-srext.json` 78 to 79, and nothing else (D-613).

### 6.3 L2, TK5 MVS 3.8j (Hercules 4.9.1.11612-SDL-gee86c4de on an Intel Core i7-13650HX; SOFT2C)

GCCMVS and JCC print no version in these listings. What ran is read from each
listing's NFR-OBS-01 manifest (`ENGINE VERSION 0.5.1`, `COMPILER GCC` or
`COMPILER JCC`, `PLATFORM MVS38J`, `FLOAT BACKEND SOFT2C`); the versions,
GCCMVS 3.2.3 at `-O1` and JCC 1.50.00, are G0's measurements (VL-86), not
re-probed today.

| Job | Command | Result |
|---|---|---|
| 407 ONFIENG | `python tools/mvsrun.py --install-eng` | every step `COND CODE 0000`; ONFLYENG from this tree in `HERC01.ONFLY.LOADLIB` |
| 408 ONFIDRV | `python tools/mvsrun.py --install-drv` | `COB` 0004 (the known IKFCBL00 warnings), every other step 0000 |
| 409 ONFTX04 | `python tools/mvsrun.py --buzz --tx04` | **ACC-6 PASS**: `STEP2 CPU 161.99 s` against 600 s; host CPU charged to Hercules 165.3 s over 165.4 s elapsed, `Certified: the host executed the guest throughout.`; FP `F9C7EE77` (G-17) |
| 410 BUZZ | `python tools/mvsrun.py --buzz` | **ACC-7 PASS**: four steps `COND CODE 0`, five fingerprints equal G-15 to G-19, `21 report line(s)`; STEP2 CPU 12 min 07.70 s, host-certified at 102% of one core |
| 411 ONFEREQ | `python tools/mvsrun.py --req` | five requests; `raw=False binary=True translated=True` against `tools/mkreq.py` |
| 412 ONFERUN | `python tools/mvsrun.py --run --out data/phase-e/v051/mvs --no-window`, then `--compare data/phase-e/v051/mvs data/phase-d/x86w` | 5 OK, 0 WARN, 0 ERROR; `mvsrun: TX-01 PASS, ACC-5 row 6 PASS` (G-15 to G-19) |
| 413 ONFJRUN | `python tools/mvsjcc.py --run --out data/phase-e/v051/jcc --no-window`, then `--compare data/phase-e/v051/jcc data/phase-d/x86w` | 22 steps `COND CODE 0000`; `mvsjcc: ACC-5 row 7 PASS (srext, measured data/phase-e/v051/jcc)` |
| 414 ONFPREQ | `python tools/mvsrun.py --net path --req` | 14 requests; `binary=True translated=True` |
| 415 ONFPRUN | `python tools/mvsrun.py --net path --run --out data/phase-e/v051/mvs --no-window`, then `--net path --compare ...` | GO `COND CODE 0008` (IR-JCL-04, G-12 and G-13); `11 OK, 1 WARN, 2 ERROR`; GO CPU 62 min 51.36 s; `mvsrun: TX-01 PASS, ACC-5 row 6 PASS` (G-01 to G-14) |
| 416 ONFJPRUN | `python tools/mvsjcc.py --net path --run --out data/phase-e/v051/jcc --no-window`, then `--net path --compare ...` | 21 steps 0000 and GO 0008; `11 OK, 1 WARN, 2 ERROR`; GO CPU 66 min 19.79 s; `mvsjcc: ACC-5 row 7 PASS (path, measured data/phase-e/v051/jcc)` (G-01 to G-14) |

Rows 6 and 7 therefore each cover all nineteen Section 8.4 requests on 0.5.1.
Jobs 415 and 416 ran while the s390x guest was building and testing (D-611),
so their CPU figures are not performance measurements; ACC-6 ran before the
guest was started. TK5 was then shut down with `script scripts/shutdown` and
verified down four ways: no Hercules process, ports 8038, 3505 and 3270
closed, and the log ending `HHC01422I Configuration released` at 02:02:11Z.

### 6.4 L3, Linux s390x (Ubuntu 24.04.5 LTS under `qemu-system-s390x` in TCG, kernel 6.8.0-139, gcc 13.3.0, GNU Make 4.3, Python 3.12.3)

The guest was booted with the 2026-09-24 session's launch script, whose 9p
export already named this worktree, and `/onfly` was checked to be this
session's tree: the SHA-256 of `prep/acc4.py` and of both networks matched the
host's.

    make ONFPLAT=s390x CC=gcc PYTHON=python3 BUILD=/tmp/b390 test

**Second run (D-615), the one reported:** `START 2026-09-27T03:49:53Z` to
`END 2026-09-27T06:19:59Z` on the guest's clock, `MAKE_EXIT=0`, closing
`ONFLY test: 25 PASS, 16 SKIP, 0 PENDING, 1 EXEMPT`. `run_gld` 20 passed on
each of SOFT3E, NATIVE and SOFT2C; `cmpgld: SOFT3E, NATIVE, SOFT2C agree on
all 19 golden requests across 2 networks`; `cmpchk [FR-SIM-10 chunk
invariance]: 24 passed`; `run_tt02: 18 of 18 operation runs passed, 781524
cases checked`; `run_eng: 32 passed` on each backend; `run_plim: 13 passed`.
This gives ACC-5 rows 4 (SOFT3E) and 5 (NATIVE). All 16 skips are D-233's
host-side class: `liclint` and `namelint` because git cannot read the 9p tree,
and fourteen `prep` checks because the guest has no numpy or pandas; those
checks ran on x86-64 in 6.1.

**The first run, and why it is not reported.** It started at 23:51:33Z and
printed the same closing line with every target PASS or SKIP, but its wrapper,
created through `wsl.exe`, `ssh` and a heredoc, had `echo "MAKE_EXIT=0"` and
both timestamps written into it when it was created. Its log therefore shows
no real exit status and no duration. `tools/testrun.py` prints the closing
line only on the path that returns 0, so exit 0 followed from the code, but the
owner chose an observed status (D-615). The corrected wrapper was written on
the host by the Write tool, moved in base64, compared by SHA-256 on both sides
(`2affad93...ac85`) and read for a literal `$rc` before it was launched.

### 6.5 Lab state at the end

TK5: `script scripts/shutdown`, then no Hercules process, ports 8038, 3505
and 3270 closed, and the log ending `HHC01422I Configuration released`. The
s390x guest: `sudo -n poweroff`, then qemu pid 627 gone, port 2222 closed,
and the console log ending at `Reached target poweroff.target`. The three
MaleCNS feathers and `signed.npz` were removed from this worktree after ACC-4
(D-614); the main checkout's originals are untouched.

### 6.6 What this does not prove

| Claim | Where it ran | Not proven |
|---|---|---|
| ACC-1, ACC-2, ACC-3 | x86-64, MinGW gcc 6.3.0, NATIVE | On any other backend or platform: the science criteria are x86-64 results; MVS proves fingerprint equality, performance and the demonstration |
| ACC-4 | x86-64, MinGW gcc 6.3.0, NATIVE, full brain | That the reference is right: it is Shiu et al.'s model re-run on a female connectome (VL-06); the magnitude gap at 10 and 40 Hz stands |
| ACC-5 rows 1 to 3b | x86-64 Windows, MinGW gcc 6.3.0 | Any other x86-64 compiler; Linux x86-64 was not run this session |
| ACC-5 rows 4, 5 | Linux s390x under QEMU TCG, gcc 13.3.0 | Real s390x hardware or its floating point (VL-01) |
| ACC-5 rows 6, 7; ACC-6; ACC-7 | TK5 under Hercules 4.9.1 on this laptop, GCCMVS and JCC, SOFT2C | Real S/370 or IBM Z hardware (VL-04); the compiler versions, which were not re-probed; each figure is one sample |
| Row 8 | nowhere | z/OS: the project does not have IBM Z access yet (VL-139) |

The CICS adapter and the Phase G components were not re-run; they are not
Phase E's criteria.

## 7. Related docs

- `docs/ONFLY-SRS.md`: Section 6.4, Section 8.3, Section 9.2's Phase E row,
  D-605 to D-616, P-47, VL-97, VL-143
- `docs/plan/2026-09-27-phase-e-reevidence-051.md` (P-47)
- `docs/implementations/2026-09-24-acc5-row7-path-resume.md`, the previous
  full re-evidencing of Phase E, on 0.5.0
- `docs/implementations/2026-09-26-fr-lod-04-limit.md`, where 0.5.1 came from
- `docs/lab.md`, for starting and stopping both labs
