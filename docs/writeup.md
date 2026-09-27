# The same answer from a laptop and from emulated MVS 3.8j

*Simulating a fruit fly circuit in C89 with software floating point: how the
byte comparison was built, the compiler fault it found, and what it does not
prove (CAN-02, CAN-14).*

FlyBatch, called ONFLY until 2026-09-27, is a personal open-source project.
It has not run on IBM Z hardware, and the project does not have IBM Z access
yet: everything below that happens on MVS or s390x happens under an
emulator, Hercules or QEMU, on one x86-64 laptop (CAN-03, VL-139, D-637).
Every paragraph cites the rows of the project's specification,
`docs/ONFLY-SRS.md`, that evidence it (D-622).

## The question

If a fruit fly tastes sugar at a given rate for a given time, what do its
feeding motor neurons do? FlyBatch answers that with a model: the
sugar-to-feeding circuit of the male fly, a 501-neuron subcircuit taken from
the MaleCNS v1.0 connectome, run with the leaky integrate-and-fire model
Shiu et al. published in 2024, in a portable C89 engine with a COBOL batch
driver (CAN-01).

A request names a sugar rate, a duration and a random seed. The answer gives,
for each of the two MN9 motor neurons, its spike count and its first-spike
latency in microseconds, a return code, and a CRC-32 fingerprint of all of
it. The fingerprint is built from integers only, so an ASCII machine and an
EBCDIC machine compute the same one (IR-COM-05, D-261).

## Why a 1970s operating system

The project's direction is a fly model served the way transaction
workloads are served. Before asking for access to real IBM Z hardware, it
set itself a harder target it could build in a lab: MVS 3.8j, a 1970s IBM
operating system, in the TK5 distribution, under the Hercules emulator
(D-01, D-02, D-23).

MVS 3.8j is stricter than anything modern. Its System/370 architecture has
no IEEE floating point, only hexadecimal. A program gets a few megabytes of
24-bit address space. The C compiler, GCCMVS, is a GCC 3.2.3 port with a
strictly C89 library, and the COBOL compiler predates the `END-IF` statement.
The lab is stricter than z/OS, so passing there de-risks a later port
(D-01, D-116, VL-15).

## The model, and what was cut

Each neuron is a leaky integrate-and-fire unit whose synaptic input decays
exponentially, with the parameters of Shiu et al.'s published code: a 0.1 ms
timestep, a 1.8 ms synaptic delay and a 2.2 ms refractory period. The one
free parameter, the weight of a single synapse, was calibrated for MaleCNS
to 0.2969 mV (D-66, D-71, D-211).

The full annotated MaleCNS network has 184,099 neurons and holds 39.0% of
the dataset's synapses. It is simulated in full, but only on the laptop.
What runs on every platform is the 501 neurons most active in the feeding
response, with one fitted input term standing in for the drive of the
neurons left out (VL-13, D-205). That subcircuit keeps within 10% of the
full network's MN9 rate at 40, 60, 120 and 200 Hz, on x86-64 (CAN-07).

## Designing for the same bits everywhere

A fingerprint only means something if every platform computes the same
bits, so the design starts from that, not from speed. Every binary64
operation in the engine goes through one small float layer, in an order the
specification fixes: never reordered, never fused into a multiply-add
(D-04, D-05).

Three rules keep the platforms from disagreeing where they easily could. No
target converts decimal text into a float: every constant is computed once
on the laptop and shipped as a 64-bit pattern. Stimulus draws use integers
only: a xorshift32 generator and a rejection rule that makes the draw
exactly uniform. And synaptic values below a tiny threshold are set to
exactly zero, so no platform ever does subnormal arithmetic, where hardware
modes differ most (FR-PRP-06, NR-12, NR-08, D-32).

Where a platform has no IEEE hardware, the float layer is Berkeley SoftFloat,
IEEE 754 done in software. Where it has, a native backend is allowed only
after it passes the TestFloat vectors and matches the software backend on
every golden request (D-04, D-07).

## Getting it onto MVS

The first surprise was the compiler. SoftFloat's current release needs
64-bit integer arithmetic, and GCCMVS could not do it: addition ended in an
internal compiler error, and multiplication produced assembler the
assembler rejected. The fallback, SoftFloat's older Release 2c, needs only
32-bit integers, and it passed its tests on MVS (VL-15, D-119).

The COBOL driver turns 80-column control cards into request records and,
after the engine has run, prints the report. It is one source, written in
the part of the language that both the 1970s MVT compiler and modern
Enterprise COBOL accept, and it is checked by a GnuCOBOL proxy, not by
Enterprise COBOL itself (D-17, D-161, VL-02).

The pieces run as a three-step batch job: driver, engine, driver. The job
that runs the demonstration, BUZZ, ran end to end with return code 0 and
printed the five shipped-network golden fingerprints. One standard 1000 ms
request used 161 s of emulated CPU under Hercules 4.9.1 on the laptop,
inside the 10-minute budget, which is an emulator figure and says nothing
about IBM Z (CAN-13, CAN-05, VL-104, VL-106).

## Nineteen requests, eight rows

The golden suite is 19 requests: silence, the validation rates, the largest
seed and rate, the shortest and longest durations, seed zero, a reserved and
an unknown stimulus, an out-of-range rate, and five requests on the shipped
network. All 19 give identical fingerprints and response records on x86-64
(a Python reference and three C floating-point builds) and on Linux s390x
under QEMU (CAN-02, VL-137).

On MVS 3.8j under Hercules with GCCMVS, the fingerprints are identical and
the response records match byte for byte, apart from one text field MVS
stores in EBCDIC. A second MVS compiler, JCC, reproduces all 19 the same way.
The z/OS row is empty (CAN-02, VL-91, VL-138, VL-139).

## A stream off an emulated card punch

The engine can also report while it runs: spikes and membrane values in
chunks of timesteps, as text. On MVS the job writes that stream to an
emulated card punch that the host reads while the job is still running, and
for the five shipped-network requests the stream is byte-identical to the
laptop's once line endings are normalised (CAN-12, VL-135, D-414).

## The +0.0 that was not zero

Comparing those two streams line by line, 19,909 lines, found what no
fingerprint had. Every +0.0 in the MVS kernel was a tiny subnormal, near
1e-318. The cause was GCCMVS: a no-argument function that returned a
two-word structure came back with the wrong bytes, while the same structure
returned from a function with two arguments was right (CAN-14, D-420,
VL-122).

No fingerprint had moved. The fingerprint covers spikes, not membrane
values, and a value near 1e-318 is swamped by every normal-sized value it
meets and never comes near the firing threshold. The record calls that luck,
not protection (VL-121, VL-125).

The fix was to stop calling that function and build the zero another way,
after which the engine's own float self-test ran on MVS for the first time
and matched the laptop's line for line. The fault itself is worked around,
not fully characterised: there is no minimal reproducer yet (D-420, VL-126,
VL-127).

## What the agreement proves, and what it does not

Identical fingerprints show that the platforms agree with each other. They
do not show that any of them is right, and the stream episode shows they do
not even imply identical internal state (VL-05, VL-118).

The science was measured on the laptop only. There, sugar at 40, 60, 120 and
200 Hz made the MN9 neurons fire in all 30 seeds at every rate, and zero
sugar produced zero spikes in all 501 neurons (CAN-06).

Compared with Shiu et al.'s model of the female FlyWire connectome, re-run
from their published code, the model on MaleCNS rises with sugar in the
same shape but fires more at low rates: 3.67 Hz at 10 Hz where the reference
is silent, and 14.35 Hz against 4.73 Hz at 40 Hz. No single synaptic weight
removes that gap, so the agreement shows consistency of shape, not identity
(CAN-08, VL-112).

Two acceptance criteria were changed after the results were seen: ACC-3 no
longer tests 10 Hz, and ACC-4 no longer tests magnitude. Both changes and
the failing numbers are in the specification (CAN-15, D-202, D-340, D-341).
The 10% agreement is partly built in, too: the fitted input term's rows
carry the full network's activity at the very rates it is tested at, and
only its one scaling constant was fitted elsewhere (D-193, D-200, VL-74).

## How it was built

FlyBatch is built with an AI coding agent, Anthropic's Claude Code, working
from a requirements specification. The agent drafts code, tests and
documents and runs the builds and the emulated-lab jobs; the owner makes
every decision, and each is recorded with the alternatives offered. This
article was drafted by the agent from the project's claims register and
approved by the owner (D-522, D-617, D-622).

## Try it

The engine, the Python reference and the x86-64 test suite are public under
the MIT licence, and `REPLICATING.md` lists what can be re-run and what each
step proves. The two network files are distributed as release assets. The
MVS rows need your own TK5 and Hercules and hours of emulated CPU, and the
3270 demonstration cannot be reproduced from the repository at all (CAN-10,
D-62, D-545).

The code and the full record are at
https://github.com/mertefesensoy/FlyBatch. Replication reports from other
platforms and compilers are the most useful thing anyone can send (D-589).
