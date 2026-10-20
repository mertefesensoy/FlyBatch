# -*- coding: utf-8 -*-
"""Run `make test`'s targets one sub-make at a time, and count what ran.

WHY THIS EXISTS (P-41 E1, D-549)

`make test` used to end with a fixed `@echo` saying that every listed check
"passed", whatever had been skipped on the way (P-44 S3).  A replicator
missing pandas got that sentence over a run that never touched pandas.  The
closing line is now counted, not asserted:

    ONFLY test: <p> PASS, <s> SKIP, <q> PENDING, <e> EXEMPT (...)

PASS counts TARGETS, measured: each target named on the command line is
made by its own sub-make, in order, and it is a PASS when that sub-make
exits 0 having printed no `ONFRES SKIP` line.  SKIP, PENDING and EXEMPT
count CHECKS: the marker lines `tools/onfres.py` prints, found anywhere in
a line of the sub-make's output.

A target that fails stops the run, as make itself would, and its status is
the runner's.  A target already made is passed to every later sub-make as
`-o <target>`, so that a phony prerequisite made earlier in the list (`req`
needs `eng`) is not run a second time and its markers are not counted
twice.  One made LATER still runs inside the earlier target's sub-make:
`shim` comes before `fp` in TESTS, so `fp` runs twice (D-549).

THE NO2C KIND (D-691)

With `NO2C=1` each SoftFloat 2c half left out prints `ONFRES NO2C
<target>/SOFT2C`.  Such a marker demotes a sub-make's target only when the
check name's prefix before `/` equals that target, so `fp`'s marker inside
`shim`'s sub-make leaves `shim` a PASS: its own comparison ran whole.  A
SKIP still demotes whatever sub-make prints it, and wins over NO2C.  The
NO2C count is of distinct check names, so `fp/SOFT2C` counts once though
it prints twice.  A run that saw any NO2C marker closes

    ONFLY test NO2C=1: <p> PASS, <s> SKIP, <q> PENDING, <e> EXEMPT, <n> NO2C

and never with a line matching `^ONFLY test: <n> PASS`, the form 11.8
reads; a run that saw none closes exactly as before.

Contract: `python tools/testrun.py MAKE TARGET...`.  Output: every byte the
sub-makes write, unchanged, then a per-target table, the checks that did
not run, and the closing line.  Exit status: 0 when every target's sub-make
exits 0, otherwise the first failing sub-make's status.  Variables given on
the outer make's command line reach the sub-makes through MAKEFLAGS, which
make exports to its recipes.
"""
import re
import subprocess
import sys

MARK = re.compile(r"\bONFRES (SKIP|EXEMPT|PENDING|NO2C) (\S+): ")
KINDS = ("SKIP", "PENDING", "EXEMPT", "NO2C")


def scan(line):
    """(kind, check) for a marker line, or None."""
    m = MARK.search(line)
    return (m.group(1), m.group(2)) if m else None


def closing(npass, nskip, npend, nexempt, nno2c=0):
    """The closing line: the one 11.8 reads, or with NO2C markers its
    NO2C=1 form, which 11.8's pattern does not match (D-691)."""
    if not nno2c:
        return ("ONFLY test: %d PASS, %d SKIP, %d PENDING, %d EXEMPT "
                "(PASS counts targets; SKIP, PENDING and EXEMPT count "
                "checks; D-548, D-549)" % (npass, nskip, npend, nexempt))
    return ("ONFLY test NO2C=1: %d PASS, %d SKIP, %d PENDING, %d EXEMPT, "
            "%d NO2C (SoftFloat 2c not built: not the full suite; PASS "
            "counts targets; SKIP, PENDING, EXEMPT and NO2C count checks; "
            "D-548, D-549, D-691)"
            % (npass, nskip, npend, nexempt, nno2c))


def verdict(target, marks):
    """PASS, SKIP or NO2C for a target whose sub-make exited 0."""
    if any(k == "SKIP" for k, _ in marks):
        return "SKIP"
    if any(k == "NO2C" and c.split("/")[0] == target for k, c in marks):
        return "NO2C"
    return "PASS"


def make_one(make, target, done, sink):
    """Make one target; relay its output; return (status, markers)."""
    cmd = [make, "--no-print-directory"]
    for t in done:
        cmd += ["-o", t]
    cmd.append(target)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    marks = []
    for raw in iter(p.stdout.readline, b""):
        sink.write(raw)
        sink.flush()
        hit = scan(raw.decode("utf-8", "replace"))
        if hit:
            marks.append(hit)
    p.stdout.close()
    return p.wait(), marks


def report(rows, marks, say):
    say("ONFLY test: per target")
    for target, verdict, counts in rows:
        extra = ", ".join("%d %s" % (n, k) for k, n in counts if n)
        say("  %-6s %-10s %s" % (verdict, target, extra))
    if marks:
        say("ONFLY test: checks that did not run")
        listed = set()
        for kind, check in marks:
            # A NO2C marker can print in two sub-makes (`fp` inside
            # `shim`'s); it is listed, like it is counted, once.
            if kind == "NO2C" and check in listed:
                continue
            listed.add(check)
            say("  %-7s %s" % (kind, check))


def main(argv):
    if len(argv) < 3:
        sys.stderr.write("usage: testrun.py MAKE TARGET...\n")
        return 2
    make, targets = argv[1], argv[2:]
    sink = getattr(sys.stdout, "buffer", sys.stdout)

    def say(text):
        sink.write((text + "\n").encode("utf-8"))
        sink.flush()

    done, rows, allmarks = [], [], []
    npass = 0
    for target in targets:
        status, marks = make_one(make, target, done, sink)
        allmarks += marks
        counts = [(k, sum(1 for m in marks if m[0] == k)) for k in KINDS]
        if status != 0:
            rows.append((target, "FAIL", counts))
            report(rows, allmarks, say)
            say("ONFLY test: FAILED %s (exit %d); later targets not run"
                % (target, status))
            return status
        kind = verdict(target, marks)
        rows.append((target, kind, counts))
        if kind == "PASS":
            npass += 1
        done.append(target)

    report(rows, allmarks, say)
    total = dict((k, sum(1 for m in allmarks if m[0] == k))
                 for k in ("SKIP", "PENDING", "EXEMPT"))
    nno2c = len(set(c for k, c in allmarks if k == "NO2C"))
    say(closing(npass, total["SKIP"], total["PENDING"], total["EXEMPT"],
                nno2c))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
