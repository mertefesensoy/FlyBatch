# Contributing to FlyBatch

Thank you for looking. FlyBatch is a personal project by Mert Efe Şensoy
with one maintainer, and it is looking for its first outside contributors.
You do not need to know MVS, COBOL or neuroscience to help. The most useful
thing anyone can do today is try FlyBatch on a setup it has never run on,
and report what happened, matching or not.

## Ways in

- **Test it on your setup.** The
  [tester matrix](https://github.com/mertefesensoy/FlyBatch/issues/4) has
  one issue per setup
  (Windows, other Linux distributions, macOS, arm64, other compilers,
  Python versions, and reading tasks that need no build). Pick one, say in
  a comment that you are taking it, and follow
  [`docs/testers.md`](docs/testers.md). These issues carry the
  `help wanted` label.
- **Fix something small.** Issues labelled
  [`good first issue`](https://github.com/mertefesensoy/FlyBatch/contribute)
  each say what done looks like and how to check it.
- **Ask a question:** GitHub Discussions.
- **Something FlyBatch does wrong:** an issue, using the bug report form.
- **Results from your own machine**, matching or not: an issue, using the
  replication report form.
- **A change to behaviour, a requirement or a recorded result:** an issue,
  using the proposal form. It carries the `proposal` label.
- **A security problem:** privately, as [`SECURITY.md`](SECURITY.md) says,
  never in a public issue.

[`ROADMAP.md`](ROADMAP.md) lists the larger open areas, and
[`SUPPORT.md`](SUPPORT.md) says what is supported and how quickly to expect
an answer. An issue labelled `good first issue`, and your first pull
request, get a first reply within 3 days (SRS D-680).

## What needs no decision

Most first contributions need nobody's decision (SRS D-685):

- reporting a result, from any platform, matching or not;
- fixing a broken link, or a sentence that misstates a recorded fact;
- adding a test for behaviour as it stands;
- fixing a bug against a requirement as it is written.

A change to a requirement, a recorded result, a dependency, the build, CI
or a licence is a proposal: open it with the proposal form first, so the
work is not wasted if the answer is no.

## How decisions are made

The contract is the specification, [`docs/ONFLY-SRS.md`](docs/ONFLY-SRS.md).
Every requirement has an ID (FR-, IR-, NR-, SR-, ACC-, NFR-), and three
kinds of record sit beside the requirements:

- **D-rows** (Appendix A.1) are decisions. The owner makes them, and each
  records the alternatives that were offered.
- **P-rows** (Appendix A.2) are proposals. A proposal stays a P-row until
  the owner decides it; it is never adopted by silence.
- **VL-rows** (Appendix D) are verification limits: what a result shows
  and, as plainly, what it does not.

What this means for you: a proposal you make is never lost and never
decided by silence. It is recorded, the owner answers it, and the answer is
written down with the alternatives that were weighed. You never need to
write a D-row yourself; the owner records the answer.

## Who reviews your pull request

People review pull requests. The owner reads, decides and merges every one.
Once a platform has a **steward** (for example for macOS or for Linux on
arm64), the steward reviews that platform's pull requests first, triages
its issues, keeps its build notes and is named beside the results it
produces; the owner merges only after the steward's review (SRS D-682). A
steward is named by the owner from people who have already contributed to
that platform. The CI checks run on every pull request.

## Credit

Testers and contributors are credited by name, with their consent: in the
release notes, in a contributors list, and for a result from a platform the
determinism matrix does not yet have, beside the README row it fills (SRS
D-681). Such a result is registered as its own verification-limit row with
its toolchain and its limits, and credited to you there too (SRS D-684). It
is a candidate for the determinism matrix of SRS Section 8.3, never an
entry by itself. Say in your report how you would like to be named, or that
you would rather not be.

## AI tools

FlyBatch itself is built with an AI coding agent, as the README says. You
may use AI tools too, if your pull request says so and you can explain
every line of it. Write issue texts and proposals yourself (SRS D-686).

## Rules the code follows

These come from the specification and are checked by `make test` where a
check exists.

- **C dialect:** C89 plus `long long` (NR-04). The engine and the soft float
  layer contain no `float` or `double` and no floating-point literals
  (NR-05); every floating-point operation goes through the `onf_fp` API in
  the order Appendix C gives (NR-07).
- **Integers:** no reliance on signed overflow; shifts and divisions only on
  non-negative values (NR-11). Multi-byte fields are decoded with explicit
  byte shifts, never pointer casts over buffers (FR-LOD-05).
- **Names:** external names are at most 8 characters, unique ignoring case
  (C-04).
- **80 columns:** files under `engine/`, `generated/`, `softfloat/`,
  `tests/`, `tools/`, `cobol/` and `cics/` stay within 80 columns, because
  some of them reach MVS through a card reader that drops everything after
  column 80 (D-93). `make col80` checks it, Python files included.
- **`third_party/`** is byte-identical to the published upstream archives
  (D-28, D-35). Pull requests that edit it are declined.
- **`generated/`** is produced from the master definition in `layout/` and is
  never edited by hand (IR-COM-01). Change the master definition and
  regenerate.
- **Writing:** new and edited public text uses no em dashes, and states only
  what the records show, with the limit that travels with it (the launch
  plan, `docs/plan/2026-09-24-open-source-launch.md`, Sections 3.4 and 5).
- **One name is kept out of this repository's text** by a committed guard,
  `tools/lint_name.py`, run by `make namelint` and by the `name-guard` CI
  job. If it reports your change, it prints only the path and line. You will
  not be told the name, and you do not need to be: rewording the reported
  line is enough. If you cannot see what to change, say so in the pull
  request and the maintainer will suggest a wording.

## Before you open a pull request

**Read the SoftFloat 2c terms first.** Every build of the engine, including
`test-nonet` and `quick`, compiles Berkeley SoftFloat Release 2c, which is
not BSD-licensed: its terms restrict use to those who accept all losses
without recompense and who indemnify its author and the International
Computer Science Institute. They are in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md), section 3. If you do
not accept them, `make test-no2c` runs the checks that never compile 2c:
the lints, the checks of the recorded evidence, the record layout and the
decoder (SRS D-679). It does not test the engine.

Run the tests in strict mode, so that a missing package or file fails
instead of passing quietly:

    ONFLY_NOSKIP=1 make ONFPLAT=x86l PYTHON=python3 test-nonet   (Linux x86-64)

    mingw32-make testfloat                          (Windows, MinGW)
    ONFLY_NOSKIP=1 mingw32-make test-nonet

On Windows, run these from Git Bash or an MSYS2 shell, not cmd.exe or
PowerShell, in a clone at a short path such as `C:\src\flybatch`: the
`ONFLY_NOSKIP=1` prefix is shell syntax, the vendored TestFloat build calls
`rm`, and a deep clone path can exceed the Windows path limit. The dev
container in `.devcontainer/` (a GitHub Codespace, for example) avoids all
three. `test-nonet` needs a C compiler, GNU Make and Python 3, and no
network file. With the two networks staged, as
[`REPLICATING.md`](REPLICATING.md) describes, run `test` instead.

Each target ends with a counted line, `ONFLY test: <p> PASS, <s> SKIP,
<q> PENDING, <e> EXEMPT`; a pass has 0 SKIP and 0 PENDING. The targets run
lowest level first and stop at the first failure (`ONFLY test: FAILED
<target>`); fix that one before reading anything after it. Paste the
counted line into the pull request with the platform, compiler and version,
and float backend it ran on.

A change to code, tests, the build, CI or a recorded result comes with an
implementation doc, `docs/implementations/YYYY-MM-DD-<slug>.md`, written
from [`docs/implementations/_TEMPLATE.md`](docs/implementations/_TEMPLATE.md).
It says what changed, why, how it was verified, and what it does not prove.
A correction to wording or a link does not need one; its pull request says
what was checked (SRS D-685).

A result is reported only from a command that was run, on the platform it
was run on. A pass on one compiler or platform is never reported as a pass
on another.

## Contribution terms

Under section D.6 of GitHub's Terms of Service, "Contributions Under
Repository License", a contribution to this repository is licensed under the
terms of the path it changes: the MIT licence in [`LICENSE`](LICENSE) for
FlyBatch's own files, and the terms
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) names for the paths it
lists (SRS D-581). No commit sign-off is required.

Two kinds of material are not accepted: anything under a non-commercial
licence, and third-party material without a licence that allows it here.
The first is why nothing derived from INTERCOMM enters this tree (SRS
D-132).

This section states the project's terms; it is not legal advice.

## Conduct

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).
