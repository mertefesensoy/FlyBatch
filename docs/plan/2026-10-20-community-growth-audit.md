# Audit: what keeps FlyBatch from becoming a community project (2026-10-20)

| Field | Value |
|---|---|
| Proposal | P-51 |
| Scope | Why nobody has joined FlyBatch, what makes the repository easier to join, where its links can live, which issues a newcomer can take, and where it can be advocated so that it gains contributors, not only visitors |
| Rests on | P-41 (the launch plan: its claims register, Section 5; its rules for every post, 7.1; its waves, 7.2); P-48; P-49, adopted as D-646; D-522 (AI use disclosed); D-580 (support channels and the 14-day answer); D-626 and D-654 (the pre-release); D-647 (affiliation only where a venue requires one); D-648 (venues that refuse AI-written text); D-651; D-652 (Open Mainframe Project channels count as IBM channels) |
| Method | The engineer's own measurements of the repository with `gh` and the build, and three read-only research agents, one each for links, contributor issues and advocacy venues; the first and third used sub-agents of their own. Every agent was told to post nothing, sign in nowhere, contact no one, file nothing, and to mark every web fact "verified 2026-10-20" or UNVERIFIED. The engineer re-read the sources the top recommendations rest on. The agents' full reports, with every row and URL, are kept in the owner's private notes |
| Status | Section 5 ADOPTED by D-677, with D-676 and D-678 to D-686 decided on the way. Of Section 9's questions, Q1 to Q3 and Q14 are answered by D-688 (Q14 as a pin only), and Q4 to Q6 by D-689; the rest are open |

Every web fact here is true on 2026-10-20 and is re-verified on the day it
is used (P-41 7.1 rule 12). Nothing in P-49 is proposed again; where a P-49
row has changed, Section 6 says so.

## 1. What this finds, in brief

1. **Nobody has found FlyBatch yet, and a visitor who wanted to help would
   find nothing to pick up.** On 2026-10-20 the repository has 0 stars, 0
   forks, 0 watchers and has never had an issue. It had 5 visitors in 14
   days, and every one of them landed on the specification, not the README
   or the site.
2. **The gate to every contributor route is a backlog of labelled issues.**
   Both outside research strands found it independently: GitHub's
   `/contribute` page, up-for-grabs.net, CodeTriage, CodeDay Labs,
   Brainhack project forms and the mentorship umbrellas all key on open,
   labelled issues. FlyBatch had none.
3. **Every outreach wave waited on a step that had not happened.** P-41's
   W1a tester invitations were never sent, so `v0.5.1`, its DOI and the
   later waves were all waiting. The owner turned W1a into a public tester
   matrix (D-676), which is also the first contributor backlog.
4. **The on-ramp put people off before their first command.** The
   governance text read as "there is no room for you"; every build,
   `test-nonet` included, compiles SoftFloat 2c, whose terms ask the user
   to indemnify its author; the promised reply was 14 days; on Windows the
   build needs a POSIX shell, `rm` and a short path, and nothing said so.
   Section 3 lists what was done about each.
5. **One independent page already reviews FlyBatch**, under its old name,
   and names the single best science task for a contributor: a null-model
   control on a rewired copy of the network (Section 7.1).
6. **The routes most likely to produce a contributor** are a Brainhack
   Warsaw team (a committee assigns 4 to 8 people to an accepted project),
   Google Summer of Code through INCF (which needs a second named mentor),
   Open Science Labs, and, once issues exist, up-for-grabs.net and CodeDay
   Labs (Section 8).

## 2. Measured on 2026-10-20

| # | Finding | Source |
|---|---|---|
| M1 | 0 stars, 0 forks, 0 watchers; no issue ever; pull requests: two merged (the owner's), one open (Dependabot) | `gh repo view`; `gh pr list --state all`; `gh api search/issues` |
| M2 | 5 views from 5 unique visitors in the 14-day window; referrer Google, 2; **all 5 views of `docs/ONFLY-SRS.md`** | `gh api .../traffic/views`, `.../popular/referrers`, `.../popular/paths` |
| M3 | Discussions on, with GitHub's six default categories and no post; the release candidate was never announced there | GraphQL `discussionCategories` |
| M4 | The labels `good first issue` and `help wanted` exist and label nothing; `/contribute` says the repository "doesn't have any good first issues, yet" | `gh label list`; the page fetched anonymously |
| M5 | Only the pre-release `v0.5.1-rc.1`; GitHub's "latest release" is empty; W1a's invitations not sent; VCF Berlin 2026 and 40C3 not submitted; the ICSE 2027 SRC entry submitted | `gh release list`; the owner's answers on 2026-10-20 |
| M6 | Community profile 100%: README, licence, code of conduct, CONTRIBUTING, SECURITY, SUPPORT, issue forms, CITATION.cff | `gh api .../community/profile` |
| M7 | Before this audit the specification was 1,552 lines and 161,543 words, with decisions numbered to D-674; 63 implementation docs; 20 plans | `Measure-Object`; `docs/README.md` |
| M8 | `make quick`, strict, from an empty `build/`, Windows 11, MinGW.org gcc 6.3.0: 591 s in this session and 615 s in the issues agent's clone, both while other builds shared the machine, and 536 s in a second run with no other build known to be running; REPLICATING.md records 392 s. `make test-no2c`, strict, from an empty `build/`, same host: 55 s, `15 PASS, 0 SKIP, 0 PENDING, 2 EXEMPT`, no SoftFloat 2c object built | This session's runs |
| M9 | Strict `test-nonet` on a clean clone on the same host stops at `tt02` unless `mingw32-make testfloat` runs first; from cmd.exe the TestFloat build stops at `rm -f`; a clone into a 178-character directory fails with "Filename too long" | The issues agent's runs in a scratchpad clone |

## 3. Why nobody joined, and what was done

| # | Finding | What was done | Decision |
|---|---|---|---|
| F1 | No issue to pick up (M1, M4) | 41 issues: a tester matrix of 15 (a tracking issue and 14 setups) and 26 contributor issues; 12 are labelled `good first issue` (no lab, no decision) and 10 are proposals; all read by the owner and filed together once `main` has the files they link to | D-676, D-683, D-687 |
| F2 | CONTRIBUTING.md said "Contributors never write D-rows", which reads as "no room for you" | Rewritten to open with a welcome and to say what the record guarantees: a proposal is never lost or decided by silence. It now lists what needs no decision at all | D-677, D-685 |
| F3 | Every build compiles SoftFloat 2c, whose terms ask for indemnification; `docs/testers.md` told a tester who refuses to stop | `make test-no2c`, the 15 targets that never compile 2c, held to that by a test that reads the Makefile (M8); a full switch for the engine targets approved for later | D-679, P-52 |
| F4 | A 14-day answer (D-580) | A first reply within 3 days on any `good first issue` and on anyone's first pull request | D-680 |
| F5 | No credit, no ownership | Named credit with consent; outside results registered as their own VL-rows; platform stewards who review first | D-681, D-684, D-682 |
| F6 | The README's first screen spent its space on the rename and had no invitation to take part | A one-line summary, the live view on the first screen, a "Get involved" section with three ways in, a Codespaces button, the rename note moved to the repository map | D-677 |
| F7 | A toolchain to install before anything runs | A dev container pinned by digest, with the networks fetched and checked, proven by a CI job on every push | D-678 |
| F8 | Windows needs a POSIX shell, `rm` and a short path (M9) | Said in CONTRIBUTING.md; REPLICATING.md and `docs/testers.md` are a starter issue | D-677 |
| F9 | The project is built with an AI agent (D-522) and said nothing about contributors' own AI use; mentorship programmes penalise AI-written proposals | AI help allowed if disclosed and explainable; contributors write issue texts and proposals themselves | D-686 |
| F10 | No public list of what is open | `ROADMAP.md`: five open areas and what is blocked (z/OS and IBM CICS, because the project does not have IBM Z access yet) | D-677 |
| F11 | `quick` is not quick on Windows (M8), so P-41 W3's gate, "an outside tester ran `make quick` on a clean machine in under 5 minutes", is unmet on the recorded toolchain | Not changed: Section 9, Q12 | open |

## 4. The checks a newcomer meets, in order

| Step | Command | Time measured | What it needs |
|---|---|---|---|
| R0 | `python tests/run_tx.py --compare data/phase-d/x86w data/phase-d/s390x`, `python tests/run_mvsrun.py`, `python tests/run_mvsjcc.py` | under 2 s each | Python 3 and git; no compiler, no package |
| No 2c | `ONFLY_NOSKIP=1 mingw32-make test-no2c` | 55 s | a C compiler, GNU Make, Python 3 |
| Suite without networks | `mingw32-make testfloat`, then `ONFLY_NOSKIP=1 mingw32-make test-nonet` | 3 min 28 s for `test-nonet` (one run, agent's clone) | as above, and acceptance of the 2c terms |
| Fingerprints | `ONFLY_NOSKIP=1 mingw32-make quick` with the networks staged | 536 to 615 s in three runs (M8) | as above, and the two networks |

All on Windows 11 x86-64 with MinGW.org gcc 6.3.0; the Linux and dev
container paths were not run in this session (the CI job of D-678 runs the
container on the first push).

## 5. Making the repository easier to join (ADOPTED by D-677)

The engineer's list, approved as a whole by the owner on 2026-10-20. Status
is as of this change.

| # | Item | Status |
|---|---|---|
| 1 | A one-line summary under the badges, from CAN-01 and CAN-02 | Done (README) |
| 2 | The live view GIF on the first screen, under the long no-access statement P-41 3.2 keeps there | Done (README) |
| 3 | The rename note moved to the repository map | Done (README) |
| 4 | A "Get involved" section with three ways in | Done (README) |
| 5 | A dev container, one click from the README | Done (D-678); proven when its CI job first runs |
| 6 | A build without SoftFloat 2c | Done as a subset (D-679); the full switch is P-52 |
| 7 | `make quick` as the first command | In the README's dev container paragraph; its time is a finding (F11) |
| 8 | Issues to pick up | Drafted, to be filed after the owner reads them (D-683) |
| 9 | A first reply within 3 days for first contributions | Done (SUPPORT.md, README, CONTRIBUTING.md; D-680) |
| 10 | Named credit | Done in CONTRIBUTING.md (D-681, D-684) |
| 11 | CONTRIBUTING.md opening with a welcome | Done (D-685, D-686) |
| 12 | A pinned "Start here" discussion and an announcement of the tester call | Drafted for the owner; posting is the owner's |
| 13 | Platform stewards | Done in CONTRIBUTING.md (D-682); none named yet |
| 14 | `v0.5.1` once the tester results are in | Waits on the tester matrix (P-41 slice G) |
| 15 | `ROADMAP.md` | Done |
| 16 | Who reviews pull requests | Done (README, CONTRIBUTING.md) |

## 6. Links: what changed since P-49, and what is new

### 6.1 P-49's sixteen link targets

FlyBatch is listed on none of them; only L11 (topics) is done.

| # | Target | Status on 2026-10-20 | Blocker now |
|---|---|---|---|
| L1 | Fly Research Portal | Refuses automated reads (HTTP 403) | The release (P-49's gate) |
| L2 | Open Source Brain v2 | Rule unchanged; needs no release by its own rule; the application host moved to `www.v2.opensourcebrain.org` | The owner's sign-in; the release is P-49's gate, not the site's |
| L3 | SciCrunch Registry (RRID) | Refuses automated reads | The owner's sign-in; no release needed by its rule |
| L4 | Zenodo communities | **Changed:** `ocns` is closed to non-members and holds meeting abstracts; `neuroinformatics` is open and asks for OSI-licensed software | The DOI; drop `ocns` (Q10) |
| L5 | ORCID and OpenAIRE | **P-49 corrected:** a DOI reaches ORCID only after the owner grants DataCite permission in ORCID | The DOI and an ORCID |
| L6, L7, L8, L12 | The four curated lists P-49 marked "consider" | Live; L7 has an open pull request adding another fly connectome simulator; L8's viral section still lists a trading bot and an NFT collection | The owner's choice, in W2a |
| L9 | Curlie, Hercules category | Every directory page answered HTTP 503 | The site's return; suggest `github.com/mertefesensoy/FlyBatch`, never the redirecting old URL |
| L10 | CBT Tape | **New:** contributors are asked for a postal address and a telephone number | The release, an XMIT package, and Q9 |
| L13 | Software Heritage | Not archived | P-41 item 37 |
| L11 | GitHub topics | Done: 15 of 20; five free slots | Q3 |
| L14 to L16 | ModelDB, Research Software Directory, Aperta | Unchanged | As P-49 says |

### 6.2 New: the platforms that send contributors

| Platform | Rule | FlyBatch must first have | Recommendation |
|---|---|---|---|
| GitHub `/contribute` | Lists open `good first issue` issues automatically | Labelled issues | Fills itself when the issues are filed |
| up-for-grabs.net | A YAML file by pull request; maintainers willing to guide newcomers; a curated list of small tasks | At least five issues under one label | Adopt after the issues |
| CodeTriage | Emails subscribers one open issue a day; the owner adds the repository by GitHub sign-in | Open issues | Adopt after the issues |
| CodeDay Labs | Matches students to issues tagged for it | Labelled issues; its cost is unknown | Ask its terms first |
| goodfirstissue.dev | At least 3 labelled issues and at least 10 contributors | 10 contributors | Later |
| awesome-for-beginners | Asks that personal projects not be added | n/a | Skip |

### 6.3 New: FlyBatch's own surfaces

1. **The site's `<head>` is thin:** the title is the bare word "FlyBatch",
   the description is 275 characters and is cut before its no-access
   sentence, there is no canonical link and no Open Graph or Twitter card,
   and the page's `<h1>` does not contain the name. A card image must keep
   the MaleCNS attribution inside it (P-41 7.1 rule 10), so a 2:1 crop of
   `srext-network.png` will not do; the D-666 social preview would.
2. **The repository description puts "emulated" near character 250.** A
   search result shows about 155 characters, so the snippet reads "from
   x86-64 to MVS 3.8j" without it.
3. **`CITATION.cff` and `.zenodo.json` lack the Shiu et al. DOI**, and
   `CITATION.cff` lacks the site and keywords. Zenodo reads `.zenodo.json`
   at release, so this must land before the `v0.5.1` tag or the first
   record keeps the gap.
4. **Search sends people to the specification** (M2), which opens with the
   old name and the tagline D-523 kept. D-523 is not reopened here (Q13).
5. **The owner's GitHub profile** neither mentions nor pins FlyBatch; an
   entry there would carry P-41 7.1 rule 4's disclosure line, because the
   profile shows the owner's IBM roles.
6. **Wikipedia is not a target.** Its conflict-of-interest guideline
   strongly discourages editing about one's own work, and a repository is
   a self-published source. Nobody should add FlyBatch, and nobody should
   be asked to.

## 7. Findings that bear on decisions already made

1. **An outside review exists.** An independent MaleCNS projects page
   (https://franklinbaldo.github.io/malecns/, reviewed 2026-09-26, before
   the pre-release) carries a card for ONFLY with followed links to the old
   repository URL, which redirects. It names two gaps: the network files
   were not distributed (closed since by `v0.5.1-rc.1`), and there is no
   rewired or random-network control showing that the result depends on
   MaleCNS's wiring. The second is drafted as a proposal issue (I-26).
   Whether to tell the page's author about the rename is Q11.
2. **AI-text policies reach further than D-648.** deRSE27 disqualifies
   abstracts with substantial AI-generated content; OSnews's editor has
   written against AI; GSoC, Open Science Labs, Outreachy and GirlScript
   penalise AI-written contributor proposals. D-686 answers the last group.
3. **Discord has been blocked in Türkiye since 2024-10-09** (no lifting
   found; its status in October 2026 is UNVERIFIED). Several communities
   below organise on Discord; FlyBatch's own inbox stays GitHub Discussions
   (D-580).
4. **Google Summer of Code needs 18 months of project history and two
   mentors**, so FlyBatch can enter only through an umbrella organisation,
   and only with a second named mentor. Outreachy costs USD 8,000 per
   intern; Google Season of Docs has ended; the MLH Fellowship has no
   open-source track. The Open Mainframe Project's mentorship is an IBM
   channel under D-652 and waits on P-41 item 34.
5. **P-41 W3's `make quick` gate is unmet on Windows** (F11).

## 8. Where to advocate for contributors

### 8.1 Ranked by how likely each is to produce a contributor

Likelihood is the engineer's judgement from how each venue works, not a
measurement. Rows 1, 2 and 4 to 9 need the issue backlog first.

| Rank | Venue | Why it can yield contributors | Effort | Date to act |
|---|---|---|---|---|
| 1 | Brainhack Warsaw 2027, as a team leader | A committee assigns 4 to 8 participants to each accepted project for three days; travel support possible | High: in person in Warsaw, 19 to 21 March 2027; a Schengen visa from Türkiye | Team-leader registration 2026-11-08 to 2026-12-08 |
| 2 | Google Summer of Code 2027 through INCF | One contributor for 175 or 350 hours; candidates' pull requests before selection | High: a second named mentor and contact twice a week from May to August | A co-mentor by mid-December 2026; INCF's expression of interest about 2027-01-19 (2026 pattern) |
| 3 | Open Science Labs affiliation | Rolling unpaid internships; a GSoC umbrella if INCF declines | Low; a README acknowledgement and quarterly checks | Any time; before about 2027-01-31 for its GSoC route |
| 4 | CodeDay Labs | Matches students to tagged issues | Low to medium; cost unknown | After the issues |
| 5 | A first-contribution workshop with a campus developer club in Ankara | Students make a first pull request in the room | Low to medium; no travel | Spring term 2027 |
| 6 | A university senior-project topic | A student team works on FlyBatch for two terms | Medium | Ask February to May 2027 |
| 7 | OHBM Brainhack 2027, a hybrid project | Participants join listed projects | Medium; a neuroimaging audience | From March 2027 |
| 8 | Kharagpur Winter of Code 2026 | Students pick registered projects for about six weeks | Low | Late November 2026, if it runs (UNVERIFIED) |
| 9 | up-for-grabs.net | A standing listing newcomers browse | Low | After five labelled issues |
| 10 | C++Online 2027, a talk | Remote; C and portability developers | Medium; an owner-written abstract is advisable | Submit by 2026-11-20 |

Next in line: Summer of Reproducibility (eligibility to ask first), a
poster at the International Symposium on Brain and Cognitive Science 2027,
an online talk at Research Software Asia Australia 2027, a news email to
the Retro Computing Roundtable podcast after the release.

### 8.2 Deadlines to 2026-12-31

| Date | What | Status |
|---|---|---|
| 2026-10-27 | FOSDEM 2027 devroom calls open (event 30 and 31 January, Brussels); Retrocomputing and Open Research ran in 2026 | P-41's; Q8 |
| 2026-10-31 | FOSDEM stands close; deRSE27 abstracts close (AI-written content refused) | Recommend skipping both |
| 2026-11-01 | FENS Regional Meeting 2027 symposia close; its abstracts run to 2027-01-21 | P-49 C18, adopted |
| 2026-11-03 | 40C3 notification | Not submitted |
| 2026-11-08 | Brainhack Warsaw team-leader registration opens | Q4 |
| 2026-11-11 | TÜBİTAK 2209-A applications close | P-41 item 41 |
| 2026-11-13 | ICSE 2027 SRC closes; SERS 2027 at ICSE closes | SRC submitted |
| 2026-11-16 | FOSDEM main track closes | P-41's |
| 2026-11-20 | C++Online 2027 talks close | Q6 |
| about 2026-12-01 | FOSDEM devroom calls close (2026 pattern) | Q8 |
| 2026-12-08 | Brainhack Warsaw team-leader registration closes | Q4 |
| mid-December | INCF's GSoC call (2026 pattern) | Q5 |

## 9. Open questions for the owner

| # | Question | Options | Recommendation |
|---|---|---|---|
| Q1 | The site's `<head>`: a descriptive title, a short description that keeps the no-access sentence, a canonical link, the name in the `<h1>`, and an Open Graph card using the D-666 social preview | Adopt; adopt without the card; leave it | Adopt |
| Q2 | `CITATION.cff` and `.zenodo.json`: the Shiu et al. DOI, the site URL and keywords, before the `v0.5.1` tag | Adopt now; at the tag; leave it | Adopt now |
| Q3 | The repository description reordered so "emulated" falls in its first 155 characters, the short no-access form kept word for word; up to five small exact topics | The owner changes both settings; one of them; neither | Both |
| Q4 | Brainhack Warsaw 2027 as a team leader | Register 2026-11-08 to 12-08 and plan the visa; skip to 2028 | Register, if term time and travel allow |
| Q5 | Google Summer of Code 2027 through INCF, and Open Science Labs | Find a second mentor by mid-December and affiliate with OSL now; OSL only; neither | Affiliate with OSL now; INCF only with a named co-mentor |
| Q6 | C++Online 2027, remote, closes 2026-11-20 | An owner-written abstract on C89 portability; skip | The owner's call |
| Q7 | A pinned "Start here" discussion and an announcement of the tester matrix | Post both when the issues are filed; later | Both, when the issues are filed |
| Q8 | FOSDEM 2027 | A devroom talk if Retrocomputing or Open Research is accepted; skip | Decide when the devrooms are published (P-41 7.2's slip rule) |
| Q9 | CBT Tape asks for a postal address and a telephone number | Provide them when L10 comes up; skip L10 | The owner's call |
| Q10 | Zenodo's `ocns` community is closed to non-members | Drop it, keep `neuroinformatics`; ask for membership | Drop it |
| Q11 | The outside review links the old name and predates the pre-release | Leave it; after the release, one factual note to its author about the rename and the release assets, never asking for a different rating | Leave it |
| Q12 | P-41 W3's gate, `make quick` in under 5 minutes, is unmet on Windows | Restate it per platform, measured on Linux first; propose a faster `quick` as its own plan; keep it | Restate it per platform |
| Q13 | Search lands on the specification, which opens with the tagline D-523 kept | Keep D-523; add one line under the tagline pointing to the README's no-access statement; replace it | The owner's call; D-523 is not reopened here |
| Q14 | The owner's GitHub profile | An entry with P-41 7.1 rule 4's disclosure line, and a pin; a pin only; neither | An entry and a pin |
| Q15 | Search Console verification, the only way to see whether any of this changes what search shows | Verify the site by a meta tag; skip | Verify |
| Q16 | Labels beyond the existing set (`replication`, `tester-matrix`, `needs-lab`, platform labels) | `replication` and `tester-matrix` now; all of them; none | The first two |

## 10. What this does not prove

1. That any issue will be taken, any list will accept FlyBatch, or any
   venue will produce a contributor.
2. Anything about a site that refused automated reads (the Fly Research
   Portal, SciCrunch, Curlie on the day), or about link types beyond the
   page HTML that was read.
3. That the dev container works: it was not run here, because Docker is
   not on the development host. Its CI job proves it on the first push.
4. Linux timings: every time in Sections 2 and 4 is from one Windows host,
   with other work running for some of them.
5. 2027 dates marked as following a 2026 pattern, and anything after
   2026-10-20. Every row is re-verified on the day it is used.
6. That Google has indexed the site or the repository: only Search Console
   can say.

## 11. Related docs

- `docs/ONFLY-SRS.md`: A.1, D-522, D-554, D-580, D-626, D-646 to D-654,
  D-676 to D-686; A.2, P-41, P-48, P-49, P-51, P-52; Section 8.3; VL-140
- `docs/plan/2026-09-24-open-source-launch.md` (P-41), Sections 3.2, 3.4,
  5, 7
- `docs/plan/2026-09-27-outreach-channels.md` (P-49)
- `CONTRIBUTING.md`, `ROADMAP.md`, `SUPPORT.md`, `docs/testers.md`
- `docs/implementations/2026-10-20-community-on-ramp.md`
