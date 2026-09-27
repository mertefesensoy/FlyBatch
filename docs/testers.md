# Testing the FlyBatch release candidate

Thank you for testing. This page is for the few people invited to try
FlyBatch's release candidate, `v0.5.1-rc.1`, before its first release. It is
public so that anyone can follow the same steps; only the invitations are
private (SRS D-626, P-41 W1a).

You get **one task**, A or B. Each takes about an hour. Report what you
find as an issue, even if everything worked: a clean result from someone
other than the maintainer is the most useful thing this stage can produce.

FlyBatch has not run on IBM Z hardware, and the project does not have IBM Z
access yet. You need no mainframe and no emulator for either task.

## Task A: build it from a clean clone and check the 19 fingerprints

You need: x86-64 Windows with MinGW gcc and GNU Make, or Linux x86-64 with
gcc and make; Python 3.13 or 3.14; git; about 2 GB of disk; about 20 minutes
of machine time.

**Before you build, read the SoftFloat 2c terms.** Every build of the suite
contains Berkeley SoftFloat Release 2c, whose terms restrict use to those who
accept all losses without recompense and who indemnify its author and the
International Computer Science Institute. They are in
`THIRD_PARTY_NOTICES.md`, section 3. If you do not accept them, stop here and
do Task B instead.

1. Clone the release candidate into a new directory:

       git clone https://github.com/mertefesensoy/FlyBatch.git flybatch-rc
       cd flybatch-rc
       git checkout v0.5.1-rc.1

2. Make a fresh virtual environment and install `requirements.txt` into it,
   nothing else:

       python -m venv .venv
       . .venv/Scripts/activate          (Linux: . .venv/bin/activate)
       python -m pip install -r requirements.txt

3. Download the two network files and their checksums from the
   pre-release, into a directory of your choice, check them, and place them.
   Read `NETWORKS-NOTICE.md` first: it carries the files' attribution and
   licence.

       R=https://github.com/mertefesensoy/FlyBatch/releases/download/v0.5.1-rc.1
       mkdir ../nets && cd ../nets
       curl -fsSLO $R/onfnet-malecns-v1.0-srext.bin
       curl -fsSLO $R/onfnet-malecns-v1.0-path.bin
       curl -fsSLO $R/SHA256SUMS
       curl -fsSLO $R/NETWORKS-NOTICE.md
       sha256sum -c SHA256SUMS
       cd ../flybatch-rc
       python tools/fixtures.py --from ../nets
       python tools/fixtures.py --check

   Both `sha256sum` lines must say `OK`, and `--check` must end with `srext`
   and `path` OK; `hop2` and `full` say `NOT DISTRIBUTED`, which is expected.

4. Check the recorded evidence (seconds):

       python tests/run_tx.py --compare data/phase-d/x86w data/phase-d/s390x
       python tests/run_mvsrun.py

5. Build and run the suite in strict mode (about 11 minutes on the
   maintainer's Windows laptop):

       mingw32-make testfloat
       ONFLY_NOSKIP=1 mingw32-make test

   On Linux x86-64:

       make ONFPLAT=x86l PYTHON=python3 testfloat
       ONFLY_NOSKIP=1 make ONFPLAT=x86l PYTHON=python3 test

   If that is too long, `make quick` (Linux: add `ONFPLAT=x86l
   PYTHON=python3`) builds the engine and checks only the 19 golden
   fingerprints.

6. Report it through the **replication report** issue form:
   https://github.com/mertefesensoy/FlyBatch/issues/new/choose. It asks for
   your OS, compiler and version, the closing `ONFLY test:` line with its
   SKIP count, and the fingerprints. A failure is as useful as a pass;
   paste the first error.

**What a pass shows, and what it does not.** It shows your build reproduces
the recorded fingerprints of all 19 golden requests across the three
floating-point builds. It does not show the model is right: identical
outputs show the platforms agree, not that any of them is correct (SRS
VL-05). On a compiler other than the recorded ones, your result is a new
data point, and that is exactly what is wanted.

## Task B: read the public texts against the evidence

You need: a browser and an hour.

Read, in this order: the repository `README.md`, `docs/overview.md`,
`docs/FAQ.md`, `docs/architecture.md` and `docs/writeup.md`. Then open the
claims register, Section 5 of `docs/plan/2026-09-24-open-source-launch.md`:
5.1 lists what may be said, each with its evidence and the limits that
travel with it, and 5.2 lists what is never said.

Look for any sentence that:

* says more than its evidence, or drops a limit its register entry carries;
* could be read as a claim about IBM Z hardware, IBM CICS, whole-brain
  emulation, or correctness where only agreement was shown;
* is unclear to someone who has not read the specification.

Report what you find as an ordinary issue, quoting the sentence and the
file. "Nothing found" is a useful report too.

## Questions

Use GitHub Discussions for questions, and issues for results. The
maintainer answers within 14 days (`SUPPORT.md`).
