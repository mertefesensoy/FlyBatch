# Plan: Phase E re-evidenced on the 0.5.1 engine (2026-09-27)

| Field | Value |
|---|---|
| Scope | D-605: Phase E's exit criteria, ACC-1 to ACC-7, re-evidenced by runs made in this session on the engine D-573 moved to 0.5.1 |
| Decisions it rests on | D-605 scope, D-606 branch, D-607 push; D-474 to D-476 and D-482, D-483 as precedent for how the same criteria were re-evidenced on 0.5.0 |
| Proposal | P-47 |
| Status | APPROVED as drafted 2026-09-27 (D-608); answers in Section 8 |

## 1. Why

`ONF_ENGVER` moved from 0.5.0 to 0.5.1 on 2026-09-26 (D-573), with
`ONF_MEMLIM` (D-567, D-568) and, under JCC only, a new `ONF_MAXPAY` bound
(D-572). The session that made the change re-ran ACC-5 row 6's `srext` half
and TE-08 on TK5 (D-570) and recorded rows 4, 5, 7 and row 6's `path` half
as not re-run. D-576 left them so. ACC-6 and ACC-7 were last evidenced on
0.5.0 (JOB 403 and JOB 404, 2026-09-25).

Row 7 is the most exposed row: D-572 changed JCC's object code, and no JCC
build of 0.5.1 has ever been made. A first tag (P-41 slice G) would carry an
engine whose Section 8.3 rows were not all measured on it.

## 2. What the survey found

| # | Finding |
|---|---|
| S1 | All four networks are present and verified: `python tools/fixtures.py --check` reports `all 4 networks present and verified against MANIFEST.json` |
| S2 | The committed MVS recordings, `data/phase-e/mvs/` (row 6) and `data/phase-e/jcc/` (row 7), are 0.5.0's. `tests/run_mvsrun.py` and `tests/run_mvsjcc.py` read them, and `tools/row7amend.py` wrote Section 8.3 row 7's text and VL-138 from them. Overwriting them changes what those tests and that text are checked against |
| S3 | ACC-6 (`--buzz --tx04`) and ACC-7 (`--buzz`) run the ONFLYENG **installed** in `HERC01.ONFLY.LOADLIB`; nothing is compiled in those jobs. Which version is installed there now is not recorded. The engine must be installed from this tree first, and each listing's `ONF002I ENGINE VERSION` line read as `0.5.1` |
| S4 | The s390x guest's launch script from the 2026-09-24 session already exports this worktree's path over 9p (the worktree directory is the same one D-469's session used). Nothing outside the repository needs editing; the script is copied into this session's scratchpad |
| S5 | ACC-6 is a timing verdict. D-466 recorded a contended `path` run costing 2.5 times an uncontended one, so ACC-6 runs first, on a quiet host |
| S6 | Costs are **estimates** from the last recorded runs, not measurements: TX-04 about 4 min of CPU (235.21 s, JOB 403); BUZZ about 25 min (JOB 404); row 6 `srext` about 17 min wall; row 7 `srext` about 16 min (940.9 s); row 6 `path` about 63 min of CPU (FR-BAT-06); row 7 `path` about 80 min of `GO` CPU (JOB 402). The s390x `make test` takes hours under TCG |

## 3. Slices

**L0, x86-64 baseline.** `ONFLY_NOSKIP=1 mingw32-make test` on x86-64 Windows,
MinGW gcc 6.3.0, SOFT3E, SOFT2C and NATIVE. Evidences Section 8.3 rows 1, 2, 3
and 3b, and checks the committed rows 6 and 7 recordings are unchanged.
Expected closing line `28 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT`.

**L1, x86-64 science, before any lab starts.**

    python prep/extract.py --acc1 data/networks/onfnet-malecns-v1.0-srext.bin --label srext --jobs 14
    python prep/extract.py --acc3-file data/networks/onfnet-malecns-v1.0-srext.bin --label srext --jobs 8
    python prep/acc4.py --reeval data/calibration/acc4.json      (Q2 (a))

**L2, TK5 (Hercules 4.9.1, GCCMVS 3.2.3 at `-O1`, JCC 1.50.00, SOFT2C).**
Start Hercules detached (D-477), set `codepage 819/1047` and confirm it, then
in this order:

1. `python tools/mvsrun.py --install-eng` and `--install-drv`, so BUZZ runs
   this tree's engine (S3).
2. `python tools/mvsrun.py --cards` and `--net path --cards`.
3. **ACC-6**, alone on a quiet host: `python tools/mvsrun.py --buzz --tx04`.
4. **ACC-7**: `python tools/mvsrun.py --buzz`.
5. **Row 6 `srext`**: `python tools/mvsrun.py --req`, then
   `--run --out <D6>`, then `--compare <D6> data/phase-d/x86w`.
6. **Row 7 `srext`**: `python tools/mvsjcc.py --run --out <D7>`, then
   `--compare <D7> data/phase-d/x86w`.
7. **Row 6 `path`** and **row 7 `path`**: the same with `--net path`.

Every listing is read for `ENGINE VERSION 0.5.1` and for its compiler line.
`<D6>` and `<D7>` are fixed by Q3.

**L3, Linux s390x under qemu-system-s390x (TCG), gcc 13.3.0.** Start the
guest after ACC-6 has landed, mount `/onfly`, and run

    make ONFPLAT=s390x CC=gcc PYTHON=python3 BUILD=/tmp/b390 test

for rows 4 (SOFT3E) and 5 (NATIVE). Whether it overlaps L2's `path` runs is Q4.

**L4, the record.** VL-143 registers every measurement with its platform,
compiler, backend, job number and CPU figure; the D-rows; P-47 struck in A.2;
the implementation doc `docs/implementations/2026-09-27-phase-e-reevidence-051.md`;
memory. Commit, push to the session branch, fast-forward `main` (D-607).

**L5, the labs down** as Q4 settles, verified down four ways (TK5) and by
the console log and port 2222 (guest).

**Final turn.** `ONFLY_NOSKIP=1 mingw32-make test` again, exit 0 shown, and
`git diff --stat`.

## 4. SRS text changes this plan asks to be authorised

| # | Text | Where |
|---|---|---|
| T1 | D-rows for this session's owner answers | Appendix A.1 |
| T2 | P-47, struck when approved, pointing at its D-row | Appendix A.2 |
| T3 | VL-143, registering the measurements of L0 to L3 | Appendix D |
| T4 | A dated note on Section 9.2's Phase E row saying Phase E was re-evidenced on 0.5.1 (D-605, VL-143). **Its exact text is drafted after the runs and put to the owner before it is written**, as P-34 was for Phase G | Section 9.2 |

No requirement sentence changes. Section 8.3's row texts are not edited by
this plan.

## 5. Exit, criterion by criterion

| Criterion | Evidence this session | Platform |
|---|---|---|
| ACC-1, ACC-2 | `--acc1` prints `ACC-1 PASS` and `ACC-2 PASS` | x86-64, NATIVE |
| ACC-3 | `--acc3-file` prints `ACC-3 PASS`, 10 Hz excluded and reported (D-202), standard errors reported (D-357) | x86-64, NATIVE |
| ACC-4 | `acc4.py` prints `ACC-4 PASS` | per Q2 |
| ACC-5 | Rows 1, 2, 3, 3b by L0; rows 4, 5 by L3; rows 6, 7 by L2's four comparisons, 19 of 19 requests each. Row 8 empty (Phase F) | as listed |
| ACC-6 | `ACC-6 PASS`, certified by the host clock | TK5, GCCMVS |
| ACC-7 | four steps at `COND CODE 0`, five fingerprints G-15 to G-19, `ACC-7 PASS` | TK5, GCCMVS |

## 6. What this will not prove

* Nothing about z/OS or IBM Z hardware: row 8 stays empty and the project
  does not have IBM Z access yet (VL-139).
* TK5 results are MVS 3.8j under Hercules on this laptop (VL-04), and s390x
  results are QEMU's emulation (VL-01). Each lab figure is one sample.
* ACC-1 to ACC-4 are x86-64 NATIVE results; the MVS rows prove fingerprint
  equality, performance and the demonstration, not the science criteria.
* Under Q2 (a), ACC-4 is a re-evaluation of VL-97's stored measurement, not
  a re-measurement (D-475).
* The CICS adapter and the Phase G components are not re-run; they are not
  Phase E's.

## 7. Open questions for the owner

* **Q1.** Approve this plan as drafted, change it, or discuss it.
* **Q2.** ACC-4: (a) re-evaluate VL-97's stored full-brain record (D-475);
  (b) re-measure on the 184,099-neuron brain, about two hours of x86 and
  heavy on RAM (VL-97: 6,971 s).
* **Q3.** Where L2's recordings go: (a) a new tracked directory
  `data/phase-e/v051/mvs` and `data/phase-e/v051/jcc`, leaving 0.5.0's
  recordings and the tests that read them untouched; (b) `build/` only, the
  evidence living in VL-143 and the doc, as D-570's session did; (c) overwrite
  `data/phase-e/mvs` and `data/phase-e/jcc`, re-running `row7amend.py` and
  amending the texts written from them.
* **Q4.** The labs: may TK5 and the s390x guest be started and jobs run
  freely, the guest's `make test` overlap L2 once ACC-6 has landed, and both
  be shut down at the end of the lab work without a further question?

## 8. Answers (added after approval)

Approved as drafted by D-608. Q2 to Q4 are answered by D-609 (ACC-4 is
re-measured on the full brain, in L1), D-610 (the TK5 recordings go to
`data/phase-e/v051/mvs` and `data/phase-e/v051/jcc`) and D-611 (the lab
terms as asked). Three further answers were needed on the way, all in L1:

* D-612: the re-measure writes `data/calibration/acc4-v051.json` through a
  new `prep/acc4.py --out`, written test first in `tests/test_disc.py`;
  `acc4.json` stays as D-526 keeps it. L1's ACC-4 command is therefore

      python prep/acc4.py --jobs 14 --out acc4-v051.json

* D-613: `acc1-candidate.json` and `acc3-srext.json` are rewritten in place
  and committed, as `e2ab256` did.
* D-614: the input is staged with
  `python tools/fixtures.py --malecns annotations neurotransmitters weights`
  and removed, with the signed cache, after ACC-4.
