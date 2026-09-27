# 2026-09-27: show FlyBatch, then take it outside (P-48)

| Field | Value |
|---|---|
| Date | 2026-09-27 |
| Author | Mert Efe Şensoy, with the engineer (an AI coding agent, D-522) |
| Phase / gate | None: P-41's open-source launch, not a Section 9 phase (D-617). Plan of record P-48 (D-629) |
| Owner decisions relied on | D-617 to D-655 (this session); D-479 and D-600 (naming rule), D-478 (one author), D-488 (P-41), D-516, D-519, D-520, D-522, D-544, D-545, D-573, D-601 |
| Requirements touched | NFR-LIC-01 (the notices register and `tools/lint_ntc.py`), NFR-MNT-01 unchanged; no requirement text changed |
| Open items closed | None in Appendix B. P-41 items 8 (D-625), 9 (D-636), 22 (D-635), 29 (D-639) and 39 (D-623) closed, item 11 answered again (D-634) |

## 1. Problem / motivation

The repository had been public since 2026-09-10, truthful and replicable
after P-41's slices A to F, and nobody outside had found it: on 2026-09-27
the traffic API showed 0 stars, 0 forks and one unique visitor, the owner.
There was no release, no FAQ, no write-up, no picture of what the project
simulates and no explanation of how it works that did not require reading an
860 KB specification. Five of the release's entry items were still open,
one of them (item 8, FlyWire) blocking any publication of the network files.

The owner asked for all of it at once (D-617), then asked for more (D-621):
images, demonstrations, an architecture explainer, a polished site, and a
backlink and outreach strategy. P-48 revision 2 (D-629) is the plan that
answered both.

## 2. What changed

| File | Change |
|---|---|
| `docs/ONFLY-SRS.md` | D-617 to D-655, VL-144, P-48 and P-49 in Appendix A.2, and a "Name" row in the front matter (D-637, D-638); no requirement text |
| `docs/plan/2026-09-27-open-source-outreach.md` | P-48, the plan of record (revision 2) |
| `docs/plan/2026-09-27-outreach-channels.md` | P-49, the backlink and outreach proposal, adopted as listed (D-646) |
| `docs/plan/2026-09-24-open-source-launch.md` | P-41: status line, H0 note, items 8, 9, 11, 22, 29 and 39 marked, check 11.7 accepting either name, CAN-11's new limit (D-649) |
| `THIRD_PARTY_NOTICES.md`, `REUSE.toml`, `LICENSES/`, `reference/shiu/results/NOTICE.md`, `data/networks/NETWORKS-NOTICE.md`, `data/README.md`, `CITATION.cff`, `reference/shiu/rerun.py` | Item 8 as D-625 decided: the FlyWire-derived inventory under CC BY-NC 4.0, the networks under CC BY 4.0; `LICENSES/CC-BY-NC-4.0.txt` added, the pending placeholder removed; the demo and Pages tools registered in section 7 |
| `tools/lint_ntc.py` | Check 7: every file that states item 8's status states D-625's; eight tools added to the register list |
| `README.md`, `docs/overview.md`, community files, `CITATION.cff`, `CHANGELOG.md`, `REPLICATING.md`, `.github/ISSUE_TEMPLATE/*`, `docs/README.md`, `docs/lab.md` | The rename to FlyBatch in public text (D-638), a visual tour, links to the new documents, the first tag `v0.5.1` (D-634), and the pre-release as the networks' source |
| `prep/calibrate.py`, `prep/extract.py`, `prep/seeds.py`, `tools/g0.py` | Item 22 (D-635): records store repository-relative paths; `g0` masks the home directory as `~` |
| `tests/test_fixt.py`, `tests/test_seeds.py`, `tests/test_g0.py`, `Makefile` | Item 22's tests; `test_g0.py` in `prep` (D-640) |
| `docs/architecture.md`, `docs/diagrams/*.svg` | The architecture explainer and four hand-written diagrams (D-627, D-628) |
| `tools/netpic.py`, `tests/test_netpic.py`, `docs/media/srext-network.png` | The picture of the subcircuit, its test, and the `netpic` target |
| `tools/demo/demo.sh`, `tools/demo/demo.tape`, `docs/media/demo-linux.*`, `docs/media/demo-windows.gif` | The terminal demonstration and its two recordings (D-631, D-643), with `demo-linux` and `demo-windows` targets |
| `docs/media/mvs-*.png`, `docs/media/captures/*.txt` | Two stills from TK5 and the captured text they were drawn from (D-632) |
| `tools/lint_reg.py`, `docs/FAQ.md`, `docs/writeup.md` | The register lint (D-622) in `make test` as `reglint`, and the two texts it holds (D-650) |
| `site/index.html`, `site/style.css`, `site/build.sh`, `.github/workflows/pages.yml` | The Pages site and its deploy (D-627, D-630, D-655) |
| `docs/testers.md` | The W1a tester guide (D-626) |

Kept private in the ignored `local/outreach/`: the VCF Berlin talk and
exhibit drafts (D-644), the 40C3 proposal (D-645), the W1a invitation and the
pre-release notes before publication.

## 3. Implementation approach

**Order.** P-48 put slice G's entry items first, because the pre-release
depended on them, then the material the owner asked to see, then the
research, the site and the tester kit, each ending with its checks run.

**Test first where there was code.** Every check added this session was
shown failing before it passed: `lint_ntc.py`'s check 7 (8 of 25 self-test
cases red against the old code), the tool-list additions (4, then 3 tools
unnamed), item 22's `RepoPaths` tests (1 failure and 5 errors), the
`seeds.py` test, `test_g0.py` (6 red), `test_netpic.py` (import error) and
`lint_reg.py` (8 of 13 red against a stub).

**`cal.repo_rel(path)` and `cal.repo_abs(stored)`** (`prep/calibrate.py`).
`repo_rel` returns a path under the repository as a forward-slash path
relative to its root, and an absolute path unchanged when it lies outside
the tree or on another drive, because that cannot be made portable and
hiding it would be worse. `repo_abs` returns an absolute stored path
unchanged, so records written before D-635 still resolve, and joins a
relative one to the repository root whatever the current directory is. The
nine writers in `extract.py` store through `repo_rel`; every reader that
hands a stored path to the engine resolves it through `repo_abs`, on both
sides of the job-result lookup, so the keys still match.

**`g0.tilde(value)` and `g0.merge()`.** `tilde` replaces the home directory,
in either slash form, in every string of a nested record; `merge` applies it
to the section it writes and leaves the sections already in the file alone,
because those are the evidence D-635 keeps.

**`lint_reg.py`.** A paragraph is a run of non-blank lines outside code
fences; a table's header row is not a paragraph and each body row is its
own. Every paragraph must cite `CAN-nn`, `D-nnn` or `VL-nnn`; each cited id
must exist (CAN ids in P-41 5.1, D- and VL-rows in the SRS); no 5.2 phrase
may appear outside a heading, even negated, compared after case folding and
with hyphens and whitespace collapsed. The negation rule is strict on
purpose: a quoted fragment of an answer must not say the phrase either.

**`netpic.py`.** It reuses the live view's geometry and projection and
`layout/netread.py`'s verified decode, so the picture's neurons sit where
the live view puts them and its connections are the file's own. Every count
printed is computed from the data, and the PNG is written without timestamp
or version metadata so that two renders are byte-identical.

**The site.** One hand-written page, no scripts and no web fonts, whose
sentences are register sentences with their CAN ids in comments. `build.sh`
copies the page and exactly the images it references and fails if any local
link does not resolve, so a renamed image fails the deploy.

**The rename.** Public prose only: a word-boundary substitution that left
identifiers (`ONFLYENG`, `ONFLYDRV`, `ONFLY_NOSKIP`, `onfly_oracle`), file
names, the SRS's name and every quotation of the `ONFLY test:` line the
Makefile still prints untouched, then the former name stated once per
document.

## 4. Mathematical / numerical details

No numerical code changed. The kernel, the float layer and every network
are as they were; the fingerprints the demonstrations and captures show are
Section 8.4's golden values.

## 5. Design decisions

Every choice with a real alternative was the owner's and is recorded with
what was offered: the scope (D-617, D-621), the licence split (D-625), the
version (D-634), the paths (D-635), the name and its reach (D-636 to D-638),
the recorders (D-631, D-643), the site's build (D-630), the pre-release as
the testers' source (D-626), the lab terms (D-632), the affiliation stance
(D-647) and the finding's record (D-649). Against the engineer's
recommendation: D-626, D-631, D-636, D-637, D-643, D-644, D-647 and D-655.

The engineer chose, within the approved plan: the diagrams in
`docs/diagrams/` rather than `docs/media/`, because the register marks
`docs/media/` MaleCNS-derived and the schematics are not; `reglint` in
`TESTS` but not `NONET`, because D-622 asked for `make test` and changing
`NONET` would change a count `test_onfres.py` pins as measured; `netpic`'s
test outside `make test`, because matplotlib is not in `requirements.txt`;
and re-recording the Linux demonstration rather than editing its `.cast`
header, which had held a personal path.

## 6. Verification

Every result below was run in this session. Platform for all x86-64 Windows
results: Windows 11, MinGW.org gcc 6.3.0 (32-bit), GNU Make 3.82.90, Python
3.13.14; `make test` exercises SOFT3E, SOFT2C and NATIVE.

| Check | Command | Result |
|---|---|---|
| The suite, after W1 | `ONFLY_NOSKIP=1 mingw32-make test` | exit 0, `28 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT` (before `reglint` existed) |
| The suite on the tagged commit `8426699` | `ONFLY_NOSKIP=1 mingw32-make test` | exit 0, `29 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT` |
| Notices (item 8, the tool list) | `python tools/lint_ntc.py --self-test`; `python tools/lint_ntc.py` | `29 checks, 0 failed`; `names 6 components, 15 item 8 paths and 35 tools` |
| Register lint | `python tools/lint_reg.py --self-test`; `python tools/lint_reg.py` | `13 checks, 0 failed`; both texts cite only ids that exist |
| Item 22 | `python tests/test_fixt.py`; `python tests/test_seeds.py`; `python tests/test_g0.py` | 31, 14 and 6 tests OK |
| The picture | `mingw32-make netpic` | `test_netpic` 6 OK; 501 neurons, 10,783 connections (5,949 excitatory, 4,834 inhibitory) |
| The name guard | `python tools/lint_name.py --tree` | tree clean; the pre-commit and commit-msg hooks passed on every commit |
| CI on the branch | `gh run list --branch claude/onfly-senior-engineer-3e9602` | `success` on every completed run |
| MVS captures, TK5 under Hercules 4.9.1, GCCMVS, SOFT2C | `python tools/mvstx.py`, then `--rate 200` | G-16: screen `BAF81D91` shown 38 s in while JOB 418 still ran, no report, `FAIL` (VL-144); G-17: `STILL RUNNING` six times, `FP=F9C7EE77` after 196 s, JOB 420's report agrees on the fingerprint and both readouts, `PASS` |
| TK5 down | process, ports 8038 and 3505, log | no `hercules` after 123 s, both ports closed, `Configuration released` |
| Demonstrations | `tools/demo/demo.sh` under asciinema (WSL, gcc 15.2.0) and VHS (Windows) | `FP=BAF81D91` from NATIVE, SOFT3E and SOFT2C on both; the manifests read `X86LINUX` and `WIN32` |
| Pre-release | `gh release view v0.5.1-rc.1`; anonymous `curl -fsSLO` of each asset; `sha256sum -c SHA256SUMS`; `lint_name.py --message` on the body | prerelease true, tag at `8426699`, four assets; both `OK`; guard exit 0; `CC BY 4.0` twice in the body |
| Tester guide, Task A, fresh clone of the tag in `C:\Users\senso\fb-rc` (D-656) | the guide's own commands | clone, venv (numpy 2.4.4, pandas 2.3.3, pyarrow 21.0.0), download, `sha256sum -c`, `fixtures.py --from` and `--check`, R0 (`run_tx: 25 identical`, `run_mvsrun: 62 passed`), `testfloat`, and `ONFLY_NOSKIP=1 mingw32-make test` all exit 0, closing `29 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT`; R1 979 s wall clock |
| Site | `bash site/build.sh build/site`, served locally | 13 files, every local link resolves; 8 images loaded, no horizontal overflow at 348 px, dark theme |

**What this does not prove.** Nothing ran on IBM Z hardware or z/OS (VL-139).
The demonstration and captures show the engine's existing behaviour; no
Section 8.3 row was re-run for this work. The Linux demonstration is a
Linux x86-64 run under WSL with gcc 15.2.0, a data point outside Section 8.3
(D-554). The dry run is the owner's host and toolchain following the guide,
not an outside replication (VL-05). The MVS captures are from Hercules on a
laptop, and one G-17 run. Web facts in P-49 are true on 2026-09-27 only.

## 7. Related docs

- `docs/ONFLY-SRS.md`: Appendix A.1 D-617 to D-655; A.2 P-48, P-49; D VL-05,
  VL-139, VL-144
- `docs/plan/2026-09-27-open-source-outreach.md` (P-48),
  `docs/plan/2026-09-27-outreach-channels.md` (P-49),
  `docs/plan/2026-09-24-open-source-launch.md` (P-41)
- `docs/implementations/2026-09-27-phase-e-reevidence-051.md`: the engine
  0.5.1 evidence the pre-release stands on
