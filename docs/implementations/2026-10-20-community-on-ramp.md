# 2026-10-20: The contributor on-ramp (P-51)

| Field | Value |
|---|---|
| Date | 2026-10-20 |
| Author | Mert Efe Şensoy (owner); drafted by the engineering agent under the owner's decisions |
| Phase / gate | None of Section 9's phases: P-41's open-source work, after slice F |
| Owner decisions relied on | D-676 to D-689; D-522, D-554, D-580, D-586, D-626, D-646, D-666 |
| Requirements touched | None. No requirement text changes |
| Open items closed | The part of P-41 item 7 that D-554 left open, how a later platform enters Section 8.3 (D-684) |

## 1. Problem / motivation

On 2026-10-20 FlyBatch had 0 stars, had never had an issue, and had 5
visitors in 14 days, all of whom landed on the specification. A visitor who
wanted to help found nothing to pick up, a governance text that read as
"there is no room for you", a first build that compiles a library whose
terms ask the user to indemnify its author, and a promised reply of 14
days. P-41's tester round, which every later outreach wave waited on, had
not started. The owner asked for an audit of what would turn FlyBatch into
a community project and approved the engineer's list of changes (D-677).
P-51, `docs/plan/2026-10-20-community-growth-audit.md`, is the audit; this
document records what was changed in the repository.

## 2. What changed

| File | Change |
|---|---|
| `README.md` | A one-line summary under the badges; the live view GIF moved to the first screen, under the unchanged no-access statement; a "Get involved" section with three ways in, a Codespaces button, the dev container, `make test-no2c` and the reply and credit promises; the rename note moved to the repository map; the specification pointer moved into "How it works"; a paragraph saying who reviews pull requests |
| `CONTRIBUTING.md` | Rewritten to open with a welcome and ways in; what needs no decision (D-685); what the decision record guarantees a contributor; who reviews (D-682); credit (D-681, D-684); AI tools (D-686); the SoftFloat 2c terms before the first build, with `make test-no2c` as the alternative; the Windows shell, `rm` and path notes; `col80`'s real scope; the name guard explained; the implementation doc required only for code, tests, the build, CI or recorded results |
| `ROADMAP.md` | New: five open areas, each with its issues, and what is blocked (z/OS and IBM CICS; the INTERCOMM demonstration) |
| `SUPPORT.md` | A first reply within 3 days for `good first issue` issues and first pull requests (D-680) |
| `docs/testers.md` | The opening says the round is a public tester matrix, not private invitations (D-676); `make test-no2c` named beside the SoftFloat 2c terms (D-679); reading reports go as comments on the reading issue, since blank issues are off |
| `.github/pull_request_template.md` | The implementation-doc item says when one is required (D-685); a new item asks for AI help to be stated (D-686) |
| `Makefile` | `NO2C`, the 15 NONET targets that never compile SoftFloat 2c, and `test-no2c` (D-679); `test-no2c` added to `.PHONY` |
| `tests/test_onfres.py` | Four checks that hold `NO2C` to NONET's order, prove from the Makefile that no NO2C target reaches 2c, prove the walk finds 2c where it is, and that no 2c-free NONET target is left out |
| `.devcontainer/devcontainer.json` | New: the dev container, `mcr.microsoft.com/devcontainers/python:3.13-trixie` pinned by digest (D-678) |
| `.devcontainer/setup.sh` | New: installs `requirements.txt`, then fetches the two networks from the release `NETWORKS_TAG` names, checks them against `SHA256SUMS` and places them with `tools/fixtures.py` |
| `.github/workflows/ci.yml` | A sixth job, `devcontainer`, running the same image and script, then `make test-nonet`, strict; a comment on `NETWORKS_TAG` saying the setup script reads it |
| `site/index.html` | A descriptive `<title>`; a 153-character description that keeps the no-access sentence; a canonical link; Open Graph and Twitter card tags; the name in the `<h1>` (D-688) |
| `site/build.sh` | Copies `social-preview.png`, which the page links by an absolute `og:image` address that the build's link check does not see |
| `docs/media/social-preview.png` | New: the D-666 social preview, 1280 by 640, its MaleCNS attribution inside the image; fetched from the copy GitHub hosts for the repository, because the original was built outside the tree; covered by REUSE.toml's `docs/media/**` CC BY 4.0 entry |
| `CITATION.cff` | The site as `url`, the fifteen topics as `keywords`, and the Shiu et al. DOI, `10.1038/s41586-024-07763-9` |
| `.zenodo.json` | The Shiu et al. DOI as `cites`, and the site as `isDocumentedBy` |
| `docs/ONFLY-SRS.md` | D-676 to D-689 in A.1; P-51 and P-52 in A.2 |
| `docs/plan/2026-09-24-open-source-launch.md` | P-41's W1a row notes D-676 |
| `docs/plan/2026-10-20-community-growth-audit.md` | New: P-51 |

## 3. Implementation approach

**`make test-no2c`.** The list was found by reading each NONET target's
prerequisites and recipe, not by running anything: a target is out if its
recipe or any prerequisite names SoftFloat 2c's flags or sources
(`SF2CFLAGS`, `SF2CSRC`, `SF2CINC`), its name map (`generated/onf2cnm.h`),
its derivation (`softfloat/derive2c.py`, `softfloat/c2c`) or its upstream
directory. Eight NONET targets reach 2c: `c04mvs`, `tt02`, `c2c`, `fp`,
`kernel`, `syn` and `eng` directly, and `shim` through its prerequisite
`fp`. The other 15 form `NO2C`, in NONET's order. `test-no2c` runs them
through `tools/testrun.py`, like `test-nonet`, so the counting, strict mode
and exemptions are unchanged.

The check in `tests/test_onfres.py` repeats that reading in code, so the
list cannot drift. `rules(text, name)` returns, for every rule whose target
is `name`, its prerequisite words and its recipe (the tab-indented lines
after the rule line, with backslash continuations). `uses_2c(text, name,
seen)` returns true if a recipe matches the 2c pattern, or if any
prerequisite does: a `$(VAR)` prerequisite is expanded through the existing
`make_list`, and every word is followed as a target in its own right, with
`seen` stopping cycles. Its contract: input the Makefile text and a target
name; output a boolean; no side effects; it relies on the Makefile's
convention that recipes start with a tab. Two further checks keep the walk
honest: it must find 2c in `shim` (through `fp`) and in `c2c`, and every
NONET target it finds free of 2c must be in `NO2C`.

**The dev container.** One script, `.devcontainer/setup.sh`, serves both
the container and its CI job, so the job checks what a newcomer gets. The
networks come from the release that `NETWORKS_TAG` in `ci.yml` names, the
line the `golden` job already reads and that moves at each release, so
there is still one place to change. The image is pinned by digest, as the
workflows pin actions to full SHAs; the CI job's comment says the two
digests must stay equal.

**The documents.** Every new sentence about what FlyBatch does or has shown
comes from P-41's claims register (Section 5.1). The README's summary line
says "subcircuit" and "emulated", because 5.2 items 5 and 15 forbid a bare
501-neuron circuit and an unscoped "same bytes". The long no-access
statement stays on the first screen, under the description and above any
build step, as P-41 3.2 requires. Where the documents name issues
(`ROADMAP.md`), they use the drafted identifiers until the issues are
filed, and are updated with the real numbers before this change is
committed.

## 4. Mathematical / numerical details

None: no formula, statistic or numerical algorithm is added or changed.
`test-no2c` runs existing checks; it computes nothing new.

## 5. Design decisions

| Decision | Alternatives | Chosen by |
|---|---|---|
| W1a becomes a public tester matrix (D-676) | Private invitations; release without testers | The owner, in free text |
| Everything opened at once (D-683) | Stage 1 first; stage 1 after the release | The owner; the engineer had recommended stage 1 |
| A dev container proven by a CI job (D-678) | The owner opens a Codespace once; ship unverified | The owner, the engineer's recommendation |
| `test-no2c` now, a full switch later (D-679, P-52) | The subset only; the full switch now | The owner; the engineer had recommended the subset only |
| A 3-day first reply for first contributions (D-680) | 14 days for everything | The owner, within D-677 |
| Named credit; outside results as their own VL-rows (D-681, D-684) | No credit; new rows in Section 8.3; sub-rows | The owner |
| Stewards review first; the owner keeps merge rights (D-682) | Merge rights through CODEOWNERS; credit only | The owner, the engineer's recommendation |
| A lighter path in CONTRIBUTING.md (D-685) | The no-decision list only; no change | The owner, the engineer's recommendation |
| Contributors' AI use allowed if disclosed (D-686) | No AI; no policy | The owner, the engineer's recommendation |
| All 41 issues filed, I-26 included, after `main` has the files they link to (D-687) | Forty, without I-26; changes first | The owner, after reading the texts |
| Site, citation and settings fixes (D-688) | Files only; later | The owner, the engineer's recommendation |
| Open Science Labs and GSoC through INCF prepared next; Brainhack Warsaw and C++Online not now (D-689) | Any of the four | The owner |
| The link card uses the D-666 preview fetched from GitHub's hosted copy | A new 2:1 render with `tools/netpic.py`; a crop of `srext-network.png` | The engineer: the preview is the image the owner already approved, and a 2:1 crop of the network picture would cut its attribution line, which P-41 7.1 rule 10 forbids |
| The test walks the Makefile rather than listing 2c targets | A fixed list of the eight 2c targets in the test | The engineer: a fixed list would pass when a new 2c target is added, which is the failure the check exists for |
| The dev container's networks come from `NETWORKS_TAG` in `ci.yml` | A second copy of the tag in the script; no networks in the container | The engineer: one line to move at a release, and `make quick` works in a Codespace |
| CONTRIBUTING.md takes the Windows notes; REPLICATING.md and `docs/testers.md` do not | Fix all three now | The engineer: the other two are a starter issue (I-20), left for a newcomer |

## 6. Verification

All on Windows 11 x86-64 with MinGW.org gcc 6.3.0 and Python 3.13.14,
from Git Bash, unless stated.

1. **The new check, failing first.** `python tests/test_onfres.py
   mingw32-make` before the Makefile change: `FAIL the Makefile defines
   NO2C`, `48 passed, 1 failed`. After it: `53 passed, 0 failed`,
   including `no NO2C target compiles SoftFloat 2c, directly or through a
   prerequisite []`, `the walk finds 2c where it is: shim through fp, and
   c2c` and `every NONET target free of 2c is in NO2C []`.
2. **`make test-no2c`, strict, from an empty `build/`:**
   `ONFLY_NOSKIP=1 mingw32-make test-no2c` closed `ONFLY test: 15 PASS, 0
   SKIP, 0 PENDING, 2 EXEMPT` in 55 s, exit 0, and `ls build | grep -i 2c`
   printed nothing: no 2c object was built. It needs no `testfloat` step.
3. **`make quick`, strict, from an empty `build/`:** `2 PASS, 0 SKIP, 0
   PENDING, 0 EXEMPT`, exit 0, 591 s with other builds sharing the machine,
   and 536 s in a second run with no other build known to be running.
   REPLICATING.md records 392 s; P-51 Q12 is about the gap.
4. **The full suite and the guards:** `mingw32-make testfloat`, then
   `ONFLY_NOSKIP=1 mingw32-make test`, exit 0 in 845 s together:
   `ONFLY test: 29 PASS, 0 SKIP, 0 PENDING, 5 EXEMPT`, the same count as
   before this change. After the site and citation edits, which came later:
   `ntclint`, `namelint`, `reglint`, `liclint` and `col80` passed again;
   `python tests/test_onfres.py mingw32-make`, `53 passed, 0 failed`;
   `.zenodo.json` parses as JSON and `CITATION.cff` as YAML;
   `bash site/build.sh` assembled 17 files with every local link
   resolving; `curl -I https://doi.org/10.1038/s41586-024-07763-9`
   answered 302 to the Nature article. `tools/lint_name.py --message` passed
   on every new file, and the U+2014 count is 0 in every added or edited
   file and in the added SRS and P-41 lines.
5. **The dev container:** not run. Docker is not on the development host,
   and no Codespace was opened. The `devcontainer` CI job runs it on the
   first push; until that job is green, the README's sentence that CI
   builds the container is a statement of what the job does, not of a
   result.

What this does not prove: anything on Linux, macOS or arm64; that the dev
container builds; that any newcomer will find the new text clearer; that
the issues will be taken. `test-no2c` passing shows the lints, evidence
checks, layout, units and decoder pass without 2c; it says nothing about
the engine, which every 2c-free run leaves untested.

## 7. Related docs

- `docs/plan/2026-10-20-community-growth-audit.md` (P-51)
- `docs/plan/2026-09-24-open-source-launch.md` (P-41), Sections 3.2, 3.4,
  5 and 7.2
- `docs/plan/2026-09-27-outreach-channels.md` (P-49)
- `docs/ONFLY-SRS.md`: A.1, D-676 to D-686; A.2, P-51, P-52; Section 8.3;
  VL-140, VL-142
