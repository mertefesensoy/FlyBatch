# Proposal: where FlyBatch can be linked and introduced (2026-09-27)

| Field | Value |
|---|---|
| Proposal | P-49 |
| Scope | D-617's outreach discovery, turned by D-621 into a backlink and outreach strategy; public by D-620 |
| Plan of record | P-48 (D-629), workstream W4 |
| Rests on | P-41's claims register (Section 5), rules for every post (7.1) and waves (7.2); D-479 and D-600 (the naming rule); D-519 (IBM roles only in posts, with the disclosure line); D-520 and D-639 (no affiliation); D-522 (the README's AI-use section) |
| Method | Four read-only research agents, one per audience, each told to post nothing, sign in nowhere and contact no one; every row below was checked on the live web on 2026-09-27 by an agent, and the two calls D-644 and D-645 act on were re-read by the engineer the same day. Rows the agents could not confirm say UNVERIFIED |
| Status | PROPOSED 2026-09-27, not decided. Every row is a candidate; nothing here is adopted until the owner says so, as a D-row |

Every fact here is true on 2026-09-27 and is re-verified before it is used
(P-41 7.1 rule 12). Channels P-41 already planned or cut are named once in
Section 6 and are not proposed again.

## 1. What this adds

P-41 Section 7 planned about twenty channels in four waves. This proposal
adds **16 link targets** and **33 introduction channels** that P-41 does not
have. It recommends adopting 14 of the 49, marks 5 to skip with the reason,
and dates the calls that close between now and December 2027. The strongest additions, one per
audience:

* **Neuroscience:** the Fly Research Portal, a curated fly-community
  directory; Open Source Brain v2; an RRID in the SciCrunch Registry; the
  Brian simulator forum, whose users run the model FlyBatch re-implements.
* **Mainframe and retro:** the Curlie Hercules category, which already lists
  FlyBatch's own toolchain; the Retro Computing Forum; VCF Berlin.
* **Developers:** Changelog News, which takes an author's own work and
  links without `nofollow`; 40C3 and SCaLE; LWN, which pays, but refuses text
  written by language models.
* **Academic and Türkiye:** Zenodo's two neuroscience communities; the FENS
  Regional Meeting 2027 in Istanbul; TÜBİTAK's 2242 student competition;
  the IEEE TEDU student branch.

## 2. The backlink strategy

A backlink is only worth having where a reader who follows it gets what the
page promised. So:

1. **One canonical target.** Every link points to the repository,
   `github.com/mertefesensoy/FlyBatch`; once they exist, the Pages site for
   people and the Zenodo concept DOI for citations. Nothing links to a
   branch, a commit or a file that may move.
2. **Followed links come from GitHub itself.** Checked in the page HTML on
   2026-09-27: a GitHub README gives `rel="nofollow"` to links that leave
   github.com, and none to links to github.com repositories. An entry in a
   curated GitHub list is therefore a followed link to the repository, while
   a link from the same list to a write-up hosted elsewhere is not. Changelog
   News's web edition carried no `rel` on its outgoing links. Every other
   site's link type is unverified.
3. **Registries before lists, lists before posts.** A registry entry (DOI,
   RRID, a software directory) lasts and is cited; a list entry lasts while
   the list is maintained; a post is read for a week. The order below
   follows that, and matches P-41's rule that irreversible steps come last.
4. **Every entry is a register sentence.** The description submitted
   anywhere is CAN-01 with the limits that travel with it, never a MUST-NOT
   (P-41 5.2), and it names the project "FlyBatch (formerly ONFLY)" until the
   old name has faded.
5. **No link schemes.** No paid links, link exchanges or requests for stars,
   votes or comments (P-41 7.1 rule 9). The owner takes part in a community
   before posting to it.

**What the September 2026 context means.** The MaleCNS release set off a
wave of fly-brain games, trading bots and NFT demos, which two fly lists and
the Fly Research Portal's news both document. A limits-first description
stands out against that. The risk is being listed beside such items; the
lists that invite them are marked below.

## 3. Deadlines, soonest first

| Date | What | Status |
|---|---|---|
| 2026-09-30 | VCF Berlin 2026 registration (festival 16 to 18 October, Berlin; 2026 special exhibition on open source in vintage computing) | Talk and exhibit drafted under D-644; the owner registers |
| 2026-10-09, 23:59 UTC | 40C3 main-stage talks (27 to 30 December, Hamburg); notification 3 November | Talk drafted under D-645; the owner submits |
| 2026-10-18 | COSYNE 2027 abstracts | Skip (Section 5, row C31) |
| 2026-10-20, then about 10-27 | FOSDEM 2027 devrooms announced, then their calls open (event 30 and 31 January 2027) | Already planned by P-41 |
| 2026-11-01 | FENS Regional Meeting 2027 symposium proposals; the abstract window runs 2026-11-01 to 2027-01-21 (meeting 26 to 29 May 2027, Istanbul) | Row C18 |
| 2026-11-01 | SCaLE 24x talks (1 to 4 April 2027, Pasadena) | Row C12 |
| 2026-11-13 | ICSE 2027 ACM Student Research Competition (Dublin, 25 April to 1 May 2027) | Row C21 |
| 2027-12-01 | Connectome 2026-2027 student competition, final stage | Row C27 |

## 4. Link targets

| # | Target | Audience; what it accepts | Rule or eligibility | Effort | Recommendation | Source, verified 2026-09-27 |
|---|---|---|---|---|---|---|
| L1 | Fly Research Portal, links and news | Fly researchers; an "online software tool or database" link type | Submitted by form; curated by a Drosophila screening-centre team | Low | Adopt at the release: fly-specific and curated | https://drosophilaresearch.org |
| L2 | Open Source Brain v2 | Computational neuroscientists; any public GitHub repository | Any signed-in user may add one; NeuroML not required | Low | Adopt at the release | https://docs.opensourcebrain.org/OSBv2/Repositories.html |
| L3 | SciCrunch Registry (RRID) | Biomedical and neuroscience researchers; software tools | Anyone may register a resource; a curator reviews it within days; no paper or DOI needed | Low | Adopt at the release, so papers and posters can cite the RRID | https://scicrunch.org/create/resource (partly verified: the site blocks automated reads) |
| L4 | Zenodo communities `ocns` and `neuroinformatics` | Researchers who cite software | A release record is offered to a community; its curators accept or decline | Low | Adopt with P-41's G2 Zenodo step; curation policies UNVERIFIED | https://zenodo.org/communities/ocns |
| L5 | ORCID works, and OpenAIRE | The owner's research record | DOI works reach ORCID automatically when the owner's ORCID is a Zenodo creator; OpenAIRE harvests Zenodo | Low | Adopt after the DOI, if the owner has or makes an ORCID | https://support.orcid.org/hc/en-us/articles/360006894594 |
| L6 | Open Computational Neuroscience Resources | 712 stars; has Simulation Software and Reproducibility sections | Contributions welcome; scope is understanding the brain | Low | Consider, under Reproducibility | https://github.com/asoplata/open-computational-neuroscience-resources |
| L7 | awesome-neuroscience | 1.7k stars; software grouped by language | One pull request per item; new categories welcome; merging is slow | Low | Consider | https://github.com/analyticalmonk/awesome-neuroscience |
| L8 | Awesome Fruit Fly Connectome | 7 stars; a "Simulations and embodied models" section | Factual one-liners; hard-to-verify claims flagged; data licence stated | Low | Consider, and only under Simulations: the list also carries viral and NFT items | https://github.com/watthem/awesome-fruit-fly-connectome |
| L9 | Curlie, Hercules category | Directory readers; 54 sites, including GCCMVS, JCC and KICKS | One suggestion of one's own site, to one category; repeats can get it excluded | Low | Adopt: durable, curated, beside FlyBatch's own toolchain | https://curlie.org/Computers/Emulators/IBM_Mainframe/Hercules/ |
| L10 | CBT Tape | MVS and z/OS programmers; free MVS software | Unlimited copying allowed (MIT fits); install notes good enough to install "without outside help"; an MVS 3.8j-only package's acceptance is UNVERIFIED | High (an XMIT package with install JCL) | Consider after the release | https://www.cbttape.org/contribute.htm |
| L11 | GitHub topics | People browsing topics | At most 20 topics; small topics keep a new repository visible (softfloat 9, tk5 5, mvs38j 2, hercules 68, mainframe 411, jcl 122) | Low | Adopt: add `mainframe`, `jcl`, `tk5`, `mvs38j` to the 11 there | https://github.com/topics |
| L12 | awesome-c | 11.5k stars; libraries, tools, reading | Programs written in C "may be in scope, but not necessarily" | Low | Consider the write-up, not the repository (that link would be `nofollow`) | https://github.com/oz123/awesome-c |
| L13 | Software Heritage | Long-term archive; permanent file-level identifiers | Save Code Now; account need UNVERIFIED | Low | Already P-41 item 37; the archive suits a bit-exact project | https://www.softwareheritage.org/how-to-archive-reference-code |
| L14 | ModelDB | Model users; any language | Public only with a valid citation; a preprint's standing UNVERIFIED | Medium | Consider after a paper | https://modeldb.science/help |
| L15 | Research Software Directory | Research software engineers, mostly Dutch | Access by request, asking for affiliation and ORCID | Low | Skip unless an affiliation is stated (Q4) | https://research-software-directory.org/documentation/users/getting-access |
| L16 | Aperta, TÜBİTAK ULAKBİM archive | Türkiye; a free DataCite DOI | ULAKBİM login; undergraduate eligibility UNVERIFIED | Low | Skip: a second DOI for the same release splits its citations | https://aperta.ulakbim.gov.tr/about |

## 5. Introduction channels

| # | Channel | Audience; what it takes | Rule | Dates | Effort | Recommendation | Source, verified 2026-09-27 |
|---|---|---|---|---|---|---|---|
| C1 | Changelog News | Developers; weekly news and podcast | Own work "encouraged"; say why it is news; no tutorials or products | Weekly | Low | Adopt in W3; links are followed | https://changelog.com/news/submit |
| C2 | Retro Computing Forum | Collectors and emulator authors; mainframes in scope | Own non-profit projects fine when sharing expertise; no cross-posting | Active | Low | Adopt in W2a | https://retrocomputingforum.com/ |
| C3 | Brian simulator forum, Projects | Brian users and spiking-network modellers | Projects of any complexity; Showcase is for things made with Brian, so Projects | Active | Low | Adopt in W2a: FlyBatch re-runs a Brian2 model, and an open thread asks how Brian2 compares with other simulators | https://brian.discourse.group/c/science/7 |
| C4 | NeuralEnsemble group | Open-source neuroscience software developers | No posting rules visible | Low volume | Low | Consider, W2a | https://groups.google.com/g/neuralensemble |
| C5 | Forum3270 BBS | 3270 and MVS hobbyists | Rules and activity UNVERIFIED | Live | Low | Consider once its activity is checked | https://www.moshix.tech/ |
| C6 | GnuCOBOL forums | COBOL programmers | Members post their own projects; no written rule found | Active | Low | Consider, and only saying plainly that GnuCOBOL is a dialect check, not the target compiler | https://sourceforge.net/p/gnucobol/discussion/ |
| C7 | FLOSS Weekly | Open-source developers; weekly interviews | Episode pages invite suggestions; contact route UNVERIFIED | Weekly | Medium | Consider, W3 | https://hackaday.com/2026/09/16/floss-weekly-episode-882-with-osadl-better-together/ |
| C8 | CoRecursive | Story-driven developer podcast | A contact address only | Active | Low | Consider, W3: the compiler-bug story is its kind | https://corecursive.com/about/ |
| C9 | LWN.net | Linux and free-software developers | Pitch first; needs a news hook; pays new authors; **refuses text written by language models** | Rolling | High | Consider only as an article the owner writes (Q3) | https://lwn.net/op/AuthorGuide.lwn |
| C10 | Mainframe Connect podcast (Open Mainframe Project) | Mainframe careers, students | Interview format; guest route UNVERIFIED | Latest episode 2026-08-17 | Medium | Consider after W2b; may need item 34's disclosure (Q5) | https://openmainframeproject.org/category/podcast/ |
| C11 | 40C3 | Hacker and technology community | No product pitches; 60-minute slots | Closes 2026-10-09 | High | **D-645**: drafted | https://content.events.ccc.de/cfp/40c3/index.en.html |
| C12 | SCaLE 24x | Community open-source conference; Kernel and Low Level Systems track | No sales pitches; about 45 minutes; free speaker pass, no travel funding | Closes 2026-11-01; event 2027-04-01 to 04 | High | Consider (Q2) | https://www.socallinuxexpo.org/scale/24x/cfp |
| C13 | VCF Berlin 2026 | European vintage-computing community | Talks 45, 60 or 90 minutes; exhibits; recorded under a Creative Commons licence; travel help on request | Closes 2026-09-30; event 16 to 18 October | High | **D-644**: talk and exhibit drafted | https://vcfb.de/2026/call_for_participation.html.en |
| C14 | VCF Berlin 2027 | As above | As above | UNVERIFIED | High | Consider as the fallback if 2026 does not happen | https://vcfb.de/2026/call_for_participation.html.en (the 2026 page; no 2027 page yet) |
| C15 | GS UK Virtual 2027 | z/OS professionals; 45-minute live talks | Educational, not vendor promotion | The 2026 call ran 2026-01-19 to 03-16; 2027 UNVERIFIED | Medium | Consider: remote, so no visa | https://sessionize.com/gs-uk-virtual-2026/ |
| C16 | Bernstein Conference 2027 | European computational neuroscience; posters and talks | Open abstract call; 2027 deadlines UNVERIFIED | 2027-09-15 to 18, Lausanne | Medium | Consider | https://bernstein-network.de/en/bernstein-conference/ |
| C17 | SfN Neuroscience 2027, Theme J | Broad neuroscience; open-source tools without new data | Submitting author must be an SfN member; a fee | 2027-10-23 to 27, Chicago | Medium to high | Consider only with a budget (Q2) | https://www.sfn.org/meetings |
| C18 | FENS Regional Meeting 2027 | Neuroscience, Türkiye and the region; posters, trainee and technical symposia | Open call; travel grants exist | Symposia close 2026-11-01; abstracts 2026-11-01 to 2027-01-21; meeting 2027-05-26 to 29, Istanbul | Medium | Adopt: the best-fitting neuroscience venue in the window, in Türkiye | https://frm2027.org |
| C19 | TÜBAS and the National Neuroscience Congress | Turkish neuroscience | Membership; abstracts through the congress; which society runs 2027 UNVERIFIED | USK 2027 UNVERIFIED | Low to medium | Consider | https://tubas.org.tr |
| C20 | TÜBİTAK 2242 student research competition | Undergraduate students, alone or in teams | Applied through e-BİDEB; advisor need UNVERIFIED | 2026 cycle closed 6 April; 2027 UNVERIFIED | Medium | Consider; check it alongside 2209-A (Q6) | https://tubitak.gov.tr/en/competitions/2242-university-students-research-project-competitions |
| C21 | ICSE 2027 Student Research Competition | Software engineering; an undergraduate category | Enrolled, ACM student membership, ICSE registration; no travel support | Closes 2026-11-13 | Medium | Consider (Q2) | https://conf.researchr.org/track/icse-2027/icse-2027-src |
| C22 | bioRxiv, Neuroscience | Preprints; confirmatory or contradictory results, not tool announcements alone | No endorsement, but an affiliation must be named | Rolling | Medium | Consider as the fallback if arXiv endorsement fails (Q4) | https://www.biorxiv.org/about/FAQ |
| C23 | OSF Preprints | Preprints | No endorsement; moderated in four to five business days | Rolling | Medium | Consider as a second fallback | https://osf.io/preprints/ |
| C24 | NeuroLibre | Executable reproducible-neuroscience preprints | GitHub-based screening; runtime limits | Rolling | High | Consider later: only the Python parts could run there | https://neurolibre.org/about |
| C25 | IMPULSE | Undergraduate neuroscience journal | Needs a faculty mentor's acknowledgement; fee UNVERIFIED | Rolling | Medium | Consider only with a mentor (Q4) | https://impulse.pubpub.org |
| C26 | Open Neuromorphic talks and hacking hours | Neuromorphic and spiking-network community | Students propose talks via Discord or email | Rolling | Medium | Consider | https://open-neuromorphic.org/getting-involved/share-your-work/ |
| C27 | Connectome 2026-2027 competition | High-school and undergraduate students | Staged research with written and video submissions; whether an existing project qualifies is UNVERIFIED | Final 2027-12-01 | Medium | Consider, eligibility first | https://clematisresearch.github.io/connectome/ |
| C28 | LKD, the Turkish Linux users' association | Turkish free-software community; mailing lists and camps | Open lists; off-topic posts removed | Winter camp 2027 UNVERIFIED | Low | Consider | https://liste.linux.org.tr/listeler.php |
| C29 | IEEE TEDU Student Branch | TEDU students; talks | Through the club | 2026-27 academic year | Low | Adopt: the cheapest local talk, and a rehearsal for the others | https://society.tedu.edu.tr/en/node/2642 |
| C30 | EDRC 2027 | European fly community, 600 to 800 delegates | Registration opens January 2027; abstract rules UNVERIFIED | Bonn, 2027 (dates UNVERIFIED) | Medium | Consider only as the European alternative to Drosophila 2027 | https://edrc2027.de |
| C31 | COSYNE 2027 | Systems and computational neuroscience | Double-blind two-page abstract | Closes 2026-10-18 | High | Skip: a re-implementation that matches only in shape makes no new claim there | https://www.cosyne.org/abstracts-submission |
| C32 | Handmade Network | Low-level programmers | Since September 2026 any AI use must be disclosed; showcases must hold no AI-generated code or prose | None | Medium | Skip: FlyBatch is built with an AI coding agent (README, D-522) | https://handmade.network/blog/p/9203-september_2026__a_new_ai_policy |
| C33 | Hacktoberfest 2026 | Event participants | No longer counts pull requests; now events about open-source AI | October 2026 | n/a | Skip | https://hacktoberfest.com/questions/ |

Also checked and skipped, with the agents' reasons: VCF forums (hardware
restorers, no Hercules threads); SHARE (a z/OS audience, speakers pay); IBM
TechXchange (its call closed on 2026-05-22; an IBM channel); VCF East and
VCF Europa (working hardware expected); JORS (a fee, and it duplicates
JOSS); ASCL (astronomy only); Papers with Code (shut down on 2025-07-24);
bio.tools (bioinformatics data processing); NeuroML-DB (NeuroML only);
EBRAINS Model Catalog (institutional accounts); INCF KnowledgeSpace (no
individual entries); NITRC (neuroimaging); libraries.io (package managers);
AlternativeTo (end-user apps); HackerNoon and OpenHub (pages unreachable);
dormant COBOL and connectomics lists.

## 6. Already in P-41, not proposed again

H390-MVS and turnkey-mvs; the awesome-fly and Awesome-Mainframes pull
requests; the neuPrint group question; the IBM Community thread and the
Open Mainframe Project Slack; Planet Mainframe; the GCCMVS and JCC
maintainers; Hacker News once, as a normal link; a Hackaday tip; dev.to;
FOSDEM 2027; FPTalks; the INCF and OCNS Software WG; comp-neuro and
Neurostars; ReScience C; JOSS from 2027-03-11; arXiv; Drosophila 2027 and
CNS*2027 posters; TÜBİTAK 2209-A; a TEDU project page; Devnot and Kommunity;
Zenodo (G2) and Software Heritage (item 37). Cut by P-41: Reddit, lobste.rs
as an active step, Bluesky and neuromatch.social.

Re-checked on 2026-09-27 for P-41: Hackaday takes creators' own projects but
not press releases; Show HN needs something people can try and forbids
asking for votes; FOSDEM 2027 is 30 and 31 January in Brussels, with
devrooms announced on 20 October.

## 7. Findings that bear on decisions already made

1. **AI-written text.** LWN and the Handmade Network refuse text written by
   language models, and Handmade refuses AI-generated code in showcases.
   D-617 has the engineer draft the FAQ and the write-up, and the README
   already says an AI coding agent builds the project (D-522). Those two
   venues are therefore open only to text the owner writes (Q3).
2. **Affiliation.** bioRxiv, the Research Software Directory and IMPULSE ask
   for an affiliation or a faculty mentor, while D-520 and D-639 keep
   FlyBatch a personal project with none (Q4).
3. **Travel.** VCF Berlin (D-644) and 40C3 (D-645) are in Germany, where a
   visa appointment from Türkiye can take longer than the time to the
   event; 40C3 offers visa help with advance notice, and VCF Berlin travel
   help on request.
4. **The hype wave.** Some lists that fit well also carry viral and NFT
   items (L8); a listing beside them is a reputational choice (Q1).

## 8. What this proposal does not prove

1. That any channel will accept FlyBatch, or that anyone will read it.
2. Anything about a site's link type beyond the two checked in its HTML.
3. Facts past 2026-09-27: every row is re-verified before use.
4. The research is the agents' reading of each page on that day; the
   engineer re-read the two calls D-644 and D-645 act on, and found one
   date the agents had wrong (VCF Berlin starts on 16 October, not 17).

## 9. Questions for the owner

| # | Question | Options | Recommendation |
|---|---|---|---|
| Q1 | This proposal | Adopt the recommendations as listed; adopt with changes; adopt only the link targets for now | Adopt as listed, each row still re-verified before use |
| Q2 | In-person events and fees in 2027 | A budget for one or two; remote and free only | The owner's call; remote ones (GS UK Virtual, FOSDEM streams) need none |
| Q3 | Venues that refuse AI-written text (LWN, Handmade) | Owner-written pieces only; skip them | Owner-written only, and only if the owner wants to write one |
| Q4 | Venues that ask for an affiliation or a mentor | "Independent researcher"; "TED University (undergraduate student)", after checking the university's policy; skip them | "Independent researcher", which keeps D-520 and D-639 |
| Q5 | Open Mainframe Project channels (Slack, the podcast) | Treat as IBM channels needing item 34's answer; treat as independent | Treat as needing item 34's answer until it is settled |
| Q6 | TÜBİTAK 2242 beside 2209-A | Ask TEDU's project office first; skip 2242 | Ask first |
