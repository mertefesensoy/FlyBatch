# FlyBatch: frequently asked questions

FlyBatch was called ONFLY until 2026-09-27 (D-637). Every answer below cites
the rows that evidence it: D-rows are decisions and VL-rows verification
limits in the specification, `docs/ONFLY-SRS.md`, and CAN ids are entries of
the claims register in `docs/plan/2026-09-24-open-source-launch.md`. A check,
`tools/lint_reg.py`, fails the build if an answer cites nothing or cites a
row that does not exist (D-622).

## What is FlyBatch?

It simulates the sugar-to-feeding circuit of the male fruit fly: a
501-neuron subcircuit taken from the MaleCNS v1.0 connectome, run with the
leaky integrate-and-fire model of Shiu et al. (2024) in a portable C89
engine with a COBOL batch driver (CAN-01).

A request names a sugar rate, a duration and a random seed; the answer says
what the two MN9 feeding motor neurons do, with a CRC-32 fingerprint of the
whole response. The same 19 golden requests give the same fingerprints on
x86-64, on Linux s390x under QEMU and on MVS 3.8j under Hercules (CAN-02).

## Is this a brain upload, or whole-brain emulation?

No. FlyBatch runs 501 neurons, the ones most active in the sugar-to-feeding
response, with one fitted input term standing in for the neurons it leaves
out (CAN-01, D-205). They were drawn from the 184,099-neuron annotated
MaleCNS network, which holds 39.0% of the dataset's synapses (VL-13).

## What does running it on MVS tell us about the fly?

Nothing biological. The emulated MVS 3.8j system reproduces the fingerprints
the x86-64 builds give, which shows the code computes the same numbers
there. The science checks were measured on x86-64 only (CAN-02, CAN-06,
VL-05).

## What is the fitted input term, and is the 10% agreement partly built in?

The subcircuit keeps every connection among its 501 neurons with unchanged
weights, and adds a table of per-neuron input, one row per sampled sugar
rate, standing in for the drive its missing neurons supplied. Each row is
built from the full network's own measured activity at that rate, and the
whole table is scaled by one constant fitted on the calibration rates 20, 80
and 160 Hz (D-193, D-200, D-205).

So partly, yes. The constant never saw the validation rates at which the
10% agreement is tested, 40, 60, 120 and 200 Hz, but the table's rows do
carry the full network's activity at those rates (VL-74, D-165). The
agreement shows that one input term lets 501 neurons stand in for the full
network there, not that the subcircuit matches it unaided (CAN-07).

## Were the acceptance criteria changed after the results?

Yes, two of them. ACC-3 no longer tests 10 Hz, and ACC-4 no longer tests
magnitude. Both changes and the failing numbers are recorded in the
specification (CAN-15, D-202, D-340, D-341).

At 40 Hz, ACC-3's margin is smaller than the reference's own standard error,
and a campaign re-measured with new seeds is estimated to pass 52 to 60% of
the time (CAN-07, VL-114).

## How close is it to Shiu et al.'s model?

Close in shape, not in magnitude. Compared with their model of the female
FlyWire connectome, re-run from their published code, FlyBatch's model on
the annotated MaleCNS network rises with sugar in the same shape but fires
more at low rates: 3.67 Hz at 10 Hz where the reference is silent, and
14.35 Hz against 4.73 Hz at 40 Hz. No single synaptic weight removes that
gap (CAN-08, VL-103, VL-112).

## Does determinism mean the results are correct?

No. Identical fingerprints show that the platforms agree with each other,
not that any of them computes the right thing (VL-05).

They do not even show identical internal state. Until a GCCMVS
code-generation fault was found and worked around, every +0.0 in the MVS
kernel was a tiny subnormal, in every MVS run made before the fix, and no
fingerprint changed, because the fingerprint covers spikes, not membrane
values (CAN-14, D-420, VL-121, VL-125).

## Why emulated? Why not IBM Z hardware?

FlyBatch has not run on IBM Z hardware, and the project does not have IBM Z
access yet: every s390x and MVS result comes from QEMU and Hercules on one
laptop (CAN-03, VL-139). The project has not used any hosted s390x or IBM Z
service (VL-139).

MVS 3.8j under Hercules is the reference system because it is stricter than
z/OS: no IEEE floating point, 24-bit addressing and a 1970s COBOL compiler,
so passing there de-risks a later port (D-01, D-02).

## Did it run on z/OS or under IBM CICS?

No. The z/OS row of the determinism matrix is empty (VL-139). The
transaction is written in real EXEC CICS but runs on x86-64 Windows under
Raincode's CICS-compatible runtime, not under IBM CICS, and its menu-screen
program has never executed for lack of a licence (CAN-09).

On the emulated MVS lab, a request typed on a 3270 session under INTERCOMM,
a transaction monitor that is not CICS, starts the batch job and then shows
its result. The screen shows the run it started only when the request
differs from the last one run (CAN-11, VL-144).

## Is z/OS running under Hercules involved anywhere?

No. The only mainframe operating system FlyBatch has run on is MVS 3.8j, in
the TK5 distribution under Hercules (D-02, VL-139).

## How fast is it on MVS?

Under Hercules 4.9.1 on an Intel Core i7-13650HX laptop, one standard
1000 ms request on the shipped network used 161 s of emulated CPU, inside the
project's 10-minute budget. That is one emulator measurement and says
nothing about IBM Z performance (CAN-05, VL-106, VL-04).

## Why C89 and COBOL?

The engine had to build with GCCMVS and its strictly C89 library on MVS, and
the same source everywhere else, so it is C89 with `long long` and nothing
newer. The batch job is driven by COBOL because that is how such jobs are
built on MVS, and one driver source is kept in the part of the language both
the 1970s MVT compiler and Enterprise COBOL accept (D-19, D-17).

That driver compiles and runs under MVT COBOL on MVS 3.8j, and is checked by
a GnuCOBOL proxy, not by Enterprise COBOL itself (VL-02).

## Why do the arithmetic in software?

System/370 has no IEEE binary floating point, only hexadecimal floating
point, so FlyBatch does every binary64 operation in software with Berkeley
SoftFloat, in a fixed order, and ships its constants as bit patterns. That
is what lets an MVS answer be compared bit for bit with an x86-64 one (D-04,
D-06).

## Does it run on macOS or arm64?

Untested. It has been run on x86-64 Windows with MinGW gcc 6.3.0, on Linux
x86-64 under WSL with gcc 15.2.0, on Linux s390x under QEMU and on MVS 3.8j
under Hercules (VL-140, VL-143). A result from another platform is welcome
through the replication-report issue form (D-589).

## Can I reproduce the results?

The C engine, the Python reference and the x86-64 test suite are public,
and `REPLICATING.md` lists what can be re-run and what each step proves. The
two network files the suite needs are distributed as release assets rather
than in git (D-545, D-626). The MVS results need your own TK5 and Hercules
setup and hours of emulated CPU, and the 3270 demonstration cannot be
reproduced from the repository at all (CAN-10).

## Was AI used to build it?

Yes. FlyBatch is built with an AI coding agent, Anthropic's Claude Code,
working from the specification: it drafts code, tests and documentation and
runs the builds and lab jobs, and the owner makes every decision, each
recorded with the alternatives offered (D-522). This FAQ was drafted by the
agent from the claims register and approved by the owner before it was
published (D-617, D-622). Commits carry the owner's name alone (D-478).

## What is the licence?

FlyBatch's own code is under the MIT licence (D-62). The data derived from
MaleCNS, the network files included, is under CC BY 4.0 with MaleCNS's
attribution (D-50, D-516).

The reference curve derived from FlyWire data, and the files that embed it,
are under CC BY-NC 4.0; the project's position is that the one synaptic
weight fitted to that curve does not carry those terms into the network
files, a position taken without legal advice (D-625). Third-party components
keep their own terms, listed in `THIRD_PARTY_NOTICES.md` (D-535).

## Why was it renamed?

To avoid confusion with Onfly, an unrelated travel and expense software
company (D-636, D-637). The program names, the message prefix and the
specification's file name keep the old name, because they are written into
the job control, the requirements and every recorded listing (D-638).

## Who is behind it?

A personal project by Mert Efe Şensoy. It is not an IBM product and has
no affiliation with IBM or with any organisation whose data, software or
tools it uses, none of which sponsors or endorses it (D-520, D-639).
