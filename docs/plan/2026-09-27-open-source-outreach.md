# Plan: show ONFLY, then take it outside, under P-41 (2026-09-27)

| Field | Value |
|---|---|
| Scope | D-617 as revised by D-621: slice G's open entry items; an architecture explainer and visual material; the FAQ and the write-up; a backlink and outreach strategy; a GitHub Pages site; a W1a tester kit with a pre-release. Not a Section 9 phase |
| Decisions it rests on | D-617 to D-628; P-41 (D-488), its claims register (5), rules (3.4, 7.1) and checks (11); D-479 and D-600 (the naming rule); D-478 (one author); D-516 (CC BY 4.0 for ONFLY's data); D-519 (IBM roles not in the repository); D-522 (AI use); D-544, D-545, D-573 (version, assets, engine 0.5.1) |
| Proposal | P-48, revision 2. Revision 1 was not approved (D-621) |
| Status | APPROVED as drafted 2026-09-27 (D-629); Q2 to Q4 answered as D-630 to D-632. Carried out the same day, D-633 to D-656 decided on the way; the exits and their evidence are in `docs/implementations/2026-09-27-open-source-outreach.md` |

## 1. Why

The repository has been public since 2026-09-10 and P-41's slices A to F
made it truthful, licensed, replicable from a clone and ready for
contributors. Nobody outside has found it: on 2026-09-27 the traffic API
reports 0 stars, 0 forks, 0 watchers, one unique visitor in its 14-day window
and `github.com` as the only referrer. No release exists.

The owner's answer to revision 1 (D-621) is that a truthful repository is not
enough: ONFLY needs images, demonstrations and an explanation of how its
architecture works, presented well, and then a strategy for where links to
it can live and where it can be introduced. D-622 to D-628 settle how.

## 2. What the survey found

| # | Finding |
|---|---|
| S1 | `gh repo view` on 2026-09-27: the description ends with the short no-access statement; 11 topics; Discussions on; `latestRelease` null; no issues, no discussions |
| S2 | No `docs/FAQ.md`, write-up or architecture document exists. The visual material in the tree is three GIFs in `docs/media/` (`onfly-live-short.gif`, `onfly-live-standard.gif`, `onfly-mvs-live.gif`); SRS 2.1 and 2.2 hold the data flow and the component table as text |
| S3 | Soma coordinates for all 501 `srext` neurons are in `data/geom/srext-geom.json` (482 measured, 19 placed and flagged), with each neuron's role, so a rendering needs no new data. matplotlib 3.10.7 and pillow 12.2.0 are pinned in `requirements-live.txt` and installed on this host |
| S4 | P-41 H0 lists "the maintainer's IBM roles" among the FAQ's answers, but D-519 keeps the roles out of the repository. The FAQ follows D-519 |
| S5 | Slice G's entry items. Closed: 4 (D-522), 5 (D-545), 8 (D-625, this session), 14 (D-502), 20 (D-516), 23 (D-518), 39 (D-623). **Open:** 11, the version, because D-573 moved `ONF_ENGVER` to `"0.5.1"` (`engine/src/onflyeng.c:125`) while D-544 named the first tag `v0.5.0`, which `REPLICATING.md` still says; 22, absolute paths; 9, the Onfly name (D-528); 29, the rights check (the non-affiliation text is D-520) |
| S6 | Item 22: six tracked data files hold the owner's absolute paths (`data/calibration/acc3-biasnet.json`, `acc3-compensated.json`, `acc3-constbias.json`, `acc3-fitbias.json`, `seeds.json`, `data/g0/inventory.json`). The self-check P-41 found disabled is fixed: `prep/extract.py`'s `verify_comparand` refuses before writing when the measured artifact is absent (P-41 E7). Which writers still record absolute paths is not yet read |
| S7 | Item 8's paths are marked `LicenseRef-FlyWire-Pending` in `REUSE.toml` (lines 123 and 130) with `LICENSES/LicenseRef-FlyWire-Pending.txt`; `THIRD_PARTY_NOTICES.md` section 6, `reference/shiu/results/NOTICE.md` and `tools/lint_ntc.py` (its `ITEM8` inventory) describe the status as open |
| S8 | CI runs on every push to any branch, with `permissions: contents: read`. A Pages deployment by workflow needs `pages: write` and `id-token: write` in its own job |
| S9 | Every channel, rule and date in P-41 Section 7 was web-sourced on 2026-09-24 and is marked "re-verify at time of use" (7.1 rule 12) |

## 3. Workstreams, in order

Each step ends with its checks run and their output shown. Every file added
or edited obeys P-41 3.4: no em dashes, plain and measured prose, register
sentences only, the naming rule. Every image that shows MaleCNS-derived data
carries P-41 7.1 rule 10's attribution line inside the image.

**W1, slice G entry items.** First, because W6's pre-release depends on them.
(a) **Item 8, as D-625 decided:** `THIRD_PARTY_NOTICES.md` section 6,
`reference/shiu/results/NOTICE.md`, `data/README.md` and
`data/networks/NETWORKS-NOTICE.md` state the split; `REUSE.toml` marks the
item 8 paths `CC-BY-NC-4.0`, with `LICENSES/CC-BY-NC-4.0.txt` taken from the
SPDX licence list and `LicenseRef-FlyWire-Pending` removed once nothing uses
it; `tools/lint_ntc.py` and its tests change first, shown failing, then
passing. (b) **Items 11, 22, 9 and 29** are put to the owner, each with its
facts: for 11, where the version is printed and named; for 22, which writers
record absolute paths; for 9, the Onfly company and any trademark record,
re-verified on the web this session; for 29, what the check asks the owner to
confirm. The work each answer needs is done and tested.

**W2, architecture and visual material (D-627 step one, D-628).**
`docs/architecture.md` explains the system from SRS 2.1, 2.2, 4, 5 and
Appendix C in plain language, with diagrams: data flow from MaleCNS to the
three platforms; the engine as ports and adapters; the three-step MVS job and
its return codes; the determinism matrix with its filled rows. Diagrams are
hand-written SVG under `docs/media/`, on a light card so they read in
GitHub's light and dark themes. A rendering of the 501-neuron subcircuit is
drawn by a new `tools/netpic.py` from `data/geom/srext-geom.json` with
matplotlib, coloured by role. The terminal demonstration is recorded by the
method Q3 chooses, from real commands and their real output on x86-64. The
MVS captures are taken on TK5 under the terms Q4 sets. `README.md` gains a
short visual tour linking all of it. Each new tool gets a test.

**W3, FAQ and write-up (D-622, D-623).** `docs/FAQ.md` answers P-41 H0's
questions but the IBM roles (S4); the write-up, 1,500 to 2,500 words, is
`docs/writeup.md`. Every factual sentence comes from P-41 5.1 and cites its
CAN id or SRS row. `tools/lint_reg.py` is written test first and run by
`make test` through a `reglint` target. Each text is shown to the owner in
full and committed only as approved.

**W4, backlink and outreach strategy (D-620, D-621).** Researched on the web
in this session by the engineer and by read-only research subagents split by
audience (neuroscience and connectomics; mainframe and retro computing;
general developers; academic and research-software indexes; the owner's
region). Two kinds of target: **link targets**, places a durable link to
ONFLY can live (curated lists, software and model registries, directories,
wikis, topic pages), and **introduction channels** (groups, forums,
newsletters, podcasts, events, journals). For each: URL, audience, what it
accepts, its self-promotion rule, cost, dates, fit with P-41 7.1, the wave it
belongs in, effort for one maintainer, a recommendation and the date
verified. Channels P-41 already chose or cut are listed with a pointer, not
re-proposed. The result is `docs/plan/2026-09-27-outreach-channels.md`,
recorded as P-49. Nothing is posted, no account is created, nobody is
contacted. The owner decides what to adopt; each answer is a D-row.

**W5, the Pages site (D-627 step two).** A landing site built from W2 and W3
by the mechanism Q2 chooses, linking to the repository, the FAQ, the
architecture explainer, the write-up and `REPLICATING.md`, carrying the long
no-access statement (P-41 3.2) and the attribution lines. The owner switches
Pages on in the repository settings; the engineer reads the setting back and
fetches the published page anonymously.

**W6, W1a tester kit and pre-release (D-626).** `docs/testers.md` gives each
tester one task, as P-41 W1a says: a clean-clone R0 and R1 with a
`replication_report` issue, or a read of the README, overview, FAQ,
architecture and write-up against P-41 Section 5. The invitation text goes to
the gitignored `local/` (P-41 7.3). Then the pre-release: its tag name, notes
and assets are put to the owner before it is made; P-41 11.1 runs on the
tagged commit and 11.3 on the tag message and notes first; the assets are
`srext`, `path`, `SHA256SUMS` and `NETWORKS-NOTICE.md`. After publication,
P-41 11.4 and 11.11 run, and a dry run follows the guide from a fresh clone
in the session scratchpad with a fresh virtual environment from
`requirements.txt` only and the networks downloaded anonymously from the
pre-release, on x86-64 Windows with MinGW.org gcc 6.3.0. Sending invitations
is the owner's.

**Closing.** `ONFLY_NOSKIP=1 mingw32-make test`; the committed guard over the
tree and every new commit message; 11.13's em dash count over every added or
edited file; an implementation doc; push to the branch, CI read back, `main`
fast-forwarded (D-619).

## 4. Proposed text changes

| # | Where | Change | Requirement text? |
|---|---|---|---|
| T1 | SRS A.1 | D-rows for each owner answer, from D-629 | No |
| T2 | SRS A.2 | P-48 revision 2 (this plan) and P-49 (the channel proposal) | No |
| T3 | `docs/plan/2026-09-24-open-source-launch.md` | Status line; H0 and W1a notes citing D-617, D-621, D-626; items 8, 11, 22, 9, 29 and 39 marked as their D-rows say | No |
| T4 | `THIRD_PARTY_NOTICES.md`, `REUSE.toml`, `LICENSES/`, the two notices, `data/README.md` | Item 8 as D-625 decided | No |
| T5 | `README.md`, `REPLICATING.md` | The visual tour and links; the version wording if item 11 changes it | No |
| T6 | `Makefile` | A `reglint` target in `test` (D-622); `netpic` and the demo target if Q3 makes one | No |
| T7 | `.github/workflows/` | A Pages workflow, only if Q2 is (a) | No |

No SRS requirement text changes under this plan.

## 5. Exit

| # | Criterion | Command or evidence |
|---|---|---|
| X1 | Item 8's notices, `REUSE.toml` and `LICENSES/` agree with D-625, and the notice check passes | `python tools/lint_ntc.py`; `python tests/test_ntc.py` or its current test |
| X2 | Items 11, 22, 9 and 29 each put to the owner and recorded, and the work each needs done with its tests passing | the D-rows; the named tests |
| X3 | `docs/architecture.md`, the diagrams, the rendering, the terminal demo and the MVS captures committed; each new tool's test passes | the tests; the files listed in `git diff --stat` |
| X4 | `docs/FAQ.md` and `docs/writeup.md` committed as approved; the register lint passes | `python tools/lint_reg.py`; its test |
| X5 | P-49 committed, every candidate carrying a URL and a verified date of 2026-09-27, and the owner's decision recorded | a count of candidate rows against verified-date cells; the D-row |
| X6 | The Pages site published and fetched anonymously | `gh api repos/mertefesensoy/ONFLY/pages`; an anonymous fetch |
| X7 | The pre-release published and its assets verified anonymously; the tester guide dry-run from a fresh clone exits 0 | P-41 11.4 and 11.11; the dry run's transcript excerpt |
| X8 | The suite and the checks pass; pushed; CI read; `main` fast-forwarded | `ONFLY_NOSKIP=1 mingw32-make test` exit 0; `python tools/lint_name.py --tree`; 11.13 count 0; `gh run view`; `git rev-parse origin/main` |

## 6. What this plan will not prove or change

1. No new science and no new platform result; Section 8.3 is untouched.
2. No IBM Z result; row 8 stays empty; nothing about the access request.
3. No post, no account, no contact, no invitation sent by the engineer.
4. No final release and no DOI: the pre-release is for W1a, and slice G's
   release still waits for W1a's corrections.
5. D-625 is ONFLY's stated position, not legal advice, taken without the
   qualified input P-41 3.5 advised.
6. Web facts in P-49 and item 9 are true on 2026-09-27 only and are
   re-verified before use (P-41 7.1 rule 12).
7. The dry run shows the kit works on the owner's host and toolchain; it is
   not an outside replication (VL-05).
8. The MVS captures show the emulated lab; they are not IBM Z evidence
   (VL-139).

## 7. Open questions for the owner

| # | Question | Options | Recommendation |
|---|---|---|---|
| Q1 | This plan | Approve; change; discuss | Approve |
| Q2 | How the Pages site is built | (a) hand-written static HTML and CSS in `site/`, deployed by a workflow using GitHub's own Pages actions pinned to full SHAs; (b) Pages serving `/docs` from `main` through GitHub's default Jekyll theme; (c) MkDocs Material, a new Python build dependency | (a): no build tool to trust, full control of the design, and every page passes the same guard as the tree |
| Q3 | How the terminal demonstration is recorded | (a) a script that runs the real commands, keeps their real output and timing, and draws the frames with pillow, already pinned; (b) asciinema and agg under WSL, two new tools; (c) VHS, a new tool | (a): no new dependency, and the frames can only show what the commands printed |
| Q4 | Lab terms for the MVS captures | (a) start TK5 detached, run the BUZZ job and the 3270 flow as the captures need without changing the Hercules configuration, and shut it down at the end without a further question, as D-611 did; (b) ask before each start and stop; (c) no lab run: captures from the committed listings and the existing MVS GIF only | (a) |

## 8. Related docs

- `docs/ONFLY-SRS.md`: 2.1, 2.2, 4, 5, 8.3, Appendix C; A.1 (D-478, D-479,
  D-488, D-515, D-516, D-519, D-520, D-522, D-528, D-544, D-545, D-573,
  D-587, D-600, D-611, D-617 to D-628); A.2 (P-41, P-48, P-49); D (VL-05,
  VL-139)
- `docs/plan/2026-09-24-open-source-launch.md`: P-41, Sections 3.2, 3.4, 4
  (H0, W1a, G), 5, 7, 10, 11
- `REPLICATING.md`, `README.md`, `docs/overview.md`, `THIRD_PARTY_NOTICES.md`
- `docs/implementations/_TEMPLATE.md`
