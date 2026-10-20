# -*- coding: utf-8 -*-
"""The test-result plumbing of P-44's group 1: `tools/onfres.py`,
`tools/lastln.py` and `tools/testrun.py` (D-546, D-548, D-549).

WHY THESE THREE ARE TESTED BEFORE ANYTHING USES THEM

Each one exists because the build used to report less than it knew.

`lastln.py` replaces `prog | tail -1` in four Makefile recipes.  In a
pipeline the recipe's status is tail's, so for the two of those recipes
that `make test` runs, the test program's own exit status never reached
make (P-44 S1).  The property that matters is therefore the status, and it
is pinned here with programs that exit 0 and 3.

`onfres.py` is the one way a check says it did not run.  Before it, 18
files printed skip lines in four spellings (P-44 S4), so no strict mode
could be added in one place.  What is pinned: the line format the runner
counts, that `ONFLY_NOSKIP=1` turns a skip into a failure, that D-548's
exempt checks stay exempt under it, and that every exemption cites a
decision row that really exists in the SRS.

`testrun.py` produces `make test`'s closing line.  Its PASS is a target
whose own sub-make exited 0 having printed no SKIP line (D-549), so what is
pinned is that a failing target stops the run with its status, that a
skipped target is not counted as a PASS, and that a target already made is
passed to later sub-makes with `-o` rather than run twice.

`NO2C=1` (P-52, D-690 to D-692) builds and compares the engine on SOFT3E
and NATIVE only, for a contributor who does not accept Berkeley SoftFloat
2c's terms.  Each 2c half it leaves out prints an `ONFRES NO2C` marker
(D-691).  What is pinned: the marker's form and its two-condition strict
rule; that the runner demotes only the target a marker names and closes
in a form 11.8 cannot mistake for the full suite; and, from make's own dry
runs, that the switch removes every 2c command and changes nothing else.

Run:

    python tests/test_onfres.py [MAKE]

MAKE is the make program to drive the runner's end-to-end case with; the
Makefile passes "$(MAKE)".  Without it the end-to-end case is reported
through onfres itself, which is exactly the path it tests.
"""
import io
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import onfres                          # noqa: E402
import testrun                         # noqa: E402

LASTLN = os.path.join(ROOT, "tools", "lastln.py")
SRS = os.path.join(ROOT, "docs", "ONFLY-SRS.md")

ok = bad = 0


def check(label, cond, detail=""):
    global ok, bad
    # The details quote demo marker lines, and `make test`'s runner counts
    # any `ONFRES SKIP ...` it sees, so the first full run through it
    # counted this file's demo skips as real ones.  Break the token in
    # anything printed: "ONFRES_SKIP" is not a marker.
    detail = str(detail).replace("ONFRES ", "ONFRES_")
    if cond:
        ok += 1
        print("  ok   %-52s %s" % (label, detail))
    else:
        bad += 1
        print("  FAIL %-52s %s" % (label, detail))


# --- onfres: the line format and the strict mode ---------------------------

def t_onfres():
    lax, strict = {}, {"ONFLY_NOSKIP": "1"}

    text, fatal = onfres.skipline("demo/check", "no widget", env=lax)
    check("a skip line has the counted form",
          text == "ONFRES SKIP demo/check: no widget", repr(text))
    check("a skip is not fatal without ONFLY_NOSKIP", fatal is False)

    text, fatal = onfres.skipline("demo/check", "no widget", env=strict)
    check("ONFLY_NOSKIP=1 makes a skip fatal", fatal is True)
    check("the fatal skip still prints as SKIP",
          text.startswith("ONFRES SKIP demo/check: "), repr(text))

    other = {"ONFLY_NOSKIP": "0"}
    check("only the value 1 turns strict mode on",
          onfres.skipline("demo/check", "x", env=other)[1] is False)

    name = sorted(onfres.EXEMPT)[0]
    text, fatal = onfres.skipline(name, "absent here", env=strict)
    check("an exempt check prints as EXEMPT with its D-row",
          text == "ONFRES EXEMPT %s: absent here [%s]"
          % (name, onfres.EXEMPT[name]), repr(text))
    check("an exempt check is not fatal even under ONFLY_NOSKIP=1",
          fatal is False)

    text = onfres.pendingline("demo/rec", "recording absent")
    check("a pending line has the counted form",
          text == "ONFRES PENDING demo/rec: recording absent", repr(text))

    # skip() prints, and exits 1 only when the skip is fatal.
    buf = io.StringIO()
    kind = onfres.skip("demo/check", "no widget", out=buf, env=lax)
    check("skip() returns SKIP and prints one line when lax",
          kind == "SKIP" and buf.getvalue()
          == "ONFRES SKIP demo/check: no widget\n", repr(buf.getvalue()))
    buf = io.StringIO()
    try:
        onfres.skip("demo/check", "no widget", out=buf, env=strict)
        code = None
    except SystemExit as exc:
        code = exc.code
    check("skip() exits 1 under ONFLY_NOSKIP=1", code == 1, "code=%r" % code)
    check("and says why before it exits",
          "ONFLY_NOSKIP=1" in buf.getvalue() and "D-548" in buf.getvalue(),
          repr(buf.getvalue()[-80:]))
    buf = io.StringIO()
    kind = onfres.skip(name, "absent here", out=buf, env=strict)
    check("skip() of an exempt check returns EXEMPT under strict mode",
          kind == "EXEMPT")
    buf = io.StringIO()
    onfres.skip("demo/check", "no widget", out=buf, env=lax, indent="  ")
    check("skip() indents the marker when asked, and the runner still "
          "finds it", buf.getvalue() == "  ONFRES SKIP demo/check: no "
          "widget\n" and testrun.scan(buf.getvalue()) is not None,
          repr(buf.getvalue()))

    # Every exemption must cite a decision the owner actually made.
    rows = set(re.findall(r"^\| (D-\d+) \|",
                          io.open(SRS, encoding="utf-8").read(), re.M))
    for check_id, drow in sorted(onfres.EXEMPT.items()):
        check("exemption %s cites a real A.1 row" % check_id,
              drow in rows, drow)
    # D-575 removed D-548's eng/TE-08: ONFLYENG exposes FR-LOD-04's limit
    # since D-567, so TE-08 runs through the program and cannot be exempt.
    check("the table holds D-548's four remaining checks and D-555's",
          len(onfres.EXEMPT) == 5, "%d entries" % len(onfres.EXEMPT))
    check("eng/TE-08 is no longer exempt (D-575)",
          "eng/TE-08" not in onfres.EXEMPT, "")


# --- D-691: the NO2C marker and its two-condition strict rule --------------

def t_no2c():
    halves = sorted(getattr(onfres, "NO2C_HALVES", ()))
    check("onfres declares the nine 2c halves NO2C=1 may leave out",
          len(halves) == 9
          and all(h.endswith("/SOFT2C") for h in halves), halves)
    if not hasattr(onfres, "no2cline") or not halves:
        check("onfres has no2cline() and no2c() (D-691)", False)
        return
    rows = set(re.findall(r"^\| (D-\d+) \|",
                          io.open(SRS, encoding="utf-8").read(), re.M))
    check("the NO2C marker cites D-691, a real A.1 row",
          onfres.NO2C_ROW == "D-691" and onfres.NO2C_ROW in rows,
          onfres.NO2C_ROW)
    name = halves[0]
    text, fatal = onfres.no2cline(name, "why", env={})
    check("a NO2C line has the counted form",
          text == "ONFRES NO2C %s: why [D-691]" % name, repr(text))
    check("a NO2C marker is not fatal without ONFLY_NOSKIP",
          fatal is False)
    cases = [
        ("declared, NO2C=1, strict: let through", name,
         {"NO2C": "1", "ONFLY_NOSKIP": "1"}, False),
        ("undeclared, NO2C=1, strict: fails", "demo/SOFT2C",
         {"NO2C": "1", "ONFLY_NOSKIP": "1"}, True),
        ("declared, NO2C unset, strict: fails", name,
         {"ONFLY_NOSKIP": "1"}, True),
        ("declared, NO2C=yes, strict: fails (only 1)", name,
         {"NO2C": "yes", "ONFLY_NOSKIP": "1"}, True),
    ]
    for label, check_id, env, want in cases:
        got = onfres.no2cline(check_id, "why", env=env)[1]
        check("NO2C rule: " + label, got is want, "fatal=%r" % got)

    buf = io.StringIO()
    kind = onfres.no2c(name, "why", out=buf,
                       env={"NO2C": "1", "ONFLY_NOSKIP": "1"})
    check("no2c() prints one line and returns NO2C when let through",
          kind == "NO2C" and buf.getvalue() == text + "\n",
          repr(buf.getvalue()))
    buf = io.StringIO()
    try:
        onfres.no2c(name, "why", out=buf, env={"ONFLY_NOSKIP": "1"})
        code = None
    except SystemExit as exc:
        code = exc.code
    check("no2c() exits 1 when strict mode fails it, citing D-691",
          code == 1 and "D-691" in buf.getvalue(), "code=%r" % code)

    # The Makefile prints the marker from a recipe line, so the CLI is
    # what a NO2C=1 run actually executes.
    env = dict(os.environ)
    for k in ("NO2C", "ONFLY_NOSKIP"):
        env.pop(k, None)
    tool = os.path.join(ROOT, "tools", "onfres.py")

    def cli(args, extra):
        e = dict(env)
        e.update(extra)
        p = subprocess.run([sys.executable, tool] + args, env=e,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.returncode, p.stdout.decode("utf-8", "replace")

    rc, out = cli(["no2c", name], {"NO2C": "1", "ONFLY_NOSKIP": "1"})
    check("`onfres.py no2c CHECK` prints the marker and exits 0",
          rc == 0 and out.splitlines()[:1] == [onfres.no2cline(
              name, onfres.NO2C_REASON, env={})[0]], "rc=%d %r" % (rc, out))
    rc, _ = cli(["no2c", name], {"ONFLY_NOSKIP": "1"})
    check("and exits 1 when strict mode is on and NO2C=1 is not",
          rc == 1, "rc=%d" % rc)
    rc, _ = cli(["bogus"], {})
    check("and exits 2 on a usage error", rc == 2, "rc=%d" % rc)


# --- onfres.unittest_main: unittest's own skips are counted too ------------

def t_unittest():
    # D-555: a unittest skip used to reach the build output only as
    # "OK (skipped=1)", which neither a grep nor the runner could count.
    import types
    import unittest
    mod = types.ModuleType("onfres_fake")

    class Plain(unittest.TestCase):
        def test_runs(self):
            pass

        def test_skips(self):
            self.skipTest("no gadget")

    class Whole(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            raise unittest.SkipTest("no dataset")

        def test_never(self):
            pass

    mod.Plain, mod.Whole = Plain, Whole
    sys.modules["onfres_fake"] = mod
    try:
        out, err = io.StringIO(), io.StringIO()
        rc = onfres.unittest_main("fake", module="onfres_fake", out=out,
                                  stream=err, env={})
        lines = out.getvalue().splitlines()
        check("a method skip is reported as a counted SKIP line",
              "ONFRES SKIP fake/Plain.test_skips: no gadget" in lines,
              repr(lines))
        check("a class-level skip is reported under the class name",
              "ONFRES SKIP fake/Whole: no dataset" in lines, repr(lines))
        check("skips alone do not fail a lax run", rc == 0, "rc=%d" % rc)
        rc = onfres.unittest_main("fake", module="onfres_fake",
                                  out=io.StringIO(), stream=io.StringIO(),
                                  env={"ONFLY_NOSKIP": "1"})
        check("ONFLY_NOSKIP=1 fails a run with an unexempt skip",
              rc == 1, "rc=%d" % rc)
    finally:
        del sys.modules["onfres_fake"]


# --- lastln: the exit status survives --------------------------------------

def run_lastln(code, lines):
    prog = ("import sys\n"
            "for i in range(%d): print('line %%d' %% i)\n"
            "sys.exit(%d)\n" % (lines, code))
    fd, path = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    try:
        io.open(path, "w", encoding="utf-8").write(prog)
        p = subprocess.run([sys.executable, LASTLN, sys.executable, path],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        os.remove(path)
    return (p.returncode, p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def t_lastln():
    rc, out, _ = run_lastln(0, 30)
    check("lastln passes status 0 through", rc == 0, "rc=%d" % rc)
    check("and prints only the last line, as tail -1 did",
          out.splitlines() == ["line 29"], repr(out[:60]))

    rc, out, err = run_lastln(3, 30)
    check("lastln passes a nonzero status through", rc == 3, "rc=%d" % rc)
    got = out.splitlines()
    check("and prints the last 20 lines so the failure is readable",
          got == ["line %d" % i for i in range(10, 30)],
          "%d lines" % len(got))
    check("and names the status on stderr", "exited 3" in err, repr(err))

    rc, out, _ = run_lastln(0, 0)
    check("a program with no output prints nothing and passes",
          rc == 0 and out == "", "rc=%d out=%r" % (rc, out))

    # The Makefile names programs as `build/tstxxx.exe`: relative, with a
    # forward slash.  Windows process creation did not find that spelling
    # when the first unmasked run tried it, so lastln resolves a program
    # path that exists before running it.
    import lastln
    d = tempfile.mkdtemp(prefix="onfly_ll_")
    here = os.getcwd()
    try:
        os.mkdir(os.path.join(d, "build"))
        io.open(os.path.join(d, "build", "prog.exe"), "wb").write(b"")
        os.chdir(d)
        got = lastln.resolve("build/prog.exe")
        check("a relative build/ path resolves to the file itself",
              os.path.isabs(got) and os.path.samefile(
                  got, os.path.join(d, "build", "prog.exe")), got)
        check("a name that is not a path is left for PATH to find",
              lastln.resolve("gcc") == "gcc")
    finally:
        os.chdir(here)
        os.remove(os.path.join(d, "build", "prog.exe"))
        os.rmdir(os.path.join(d, "build"))
        os.rmdir(d)


# --- testrun: counting, stopping and not repeating -------------------------

def t_testrun_scan():
    check("scan finds a SKIP marker mid-line",
          testrun.scan("  ok   label   ONFRES SKIP a/b: why")
          == ("SKIP", "a/b"))
    check("scan finds an EXEMPT marker",
          testrun.scan("ONFRES EXEMPT c/d: why [D-132]") == ("EXEMPT", "c/d"))
    check("scan finds a PENDING marker",
          testrun.scan("ONFRES PENDING e/f: why") == ("PENDING", "e/f"))
    check("scan ignores an ordinary line",
          testrun.scan("  ok   TE-01 bad magic") is None)
    check("scan ignores the word SKIP without the prefix",
          testrun.scan("test_x: SKIP - pandas absent") is None)

    line = testrun.closing(3, 1, 0, 2)
    check("the closing line carries all four counts",
          line == "ONFLY test: 3 PASS, 1 SKIP, 0 PENDING, 2 EXEMPT "
                  "(PASS counts targets; SKIP, PENDING and EXEMPT count "
                  "checks; D-548, D-549)", repr(line))
    check("and matches the form 11.8 reads", COUNTED.match(line) is not None)

    # D-691.
    check("scan finds a NO2C marker",
          testrun.scan("ONFRES NO2C fp/SOFT2C: why [D-691]")
          == ("NO2C", "fp/SOFT2C"))
    try:
        same = testrun.closing(3, 1, 0, 2, 0) == line
        line = testrun.closing(1, 0, 0, 2, 3)
    except TypeError as exc:
        same, line = False, "TypeError: %s" % exc
    check("no NO2C marker leaves the closing line byte for byte", same)
    check("NO2C markers give the closing line its own form",
          line == "ONFLY test NO2C=1: 1 PASS, 0 SKIP, 0 PENDING, 2 EXEMPT, "
                  "3 NO2C (SoftFloat 2c not built: not the full suite; "
                  "PASS counts targets; SKIP, PENDING, EXEMPT and NO2C "
                  "count checks; D-548, D-549, D-691)", repr(line))
    check("which 11.8's pattern does not match",
          COUNTED.match(line) is None, repr(line[:24]))


#: The counted closing line that 11.8 reads (D-548, D-549).  A NO2C=1 run
#: must never print a line of this form (D-691).
COUNTED = re.compile(r"^ONFLY test: \d+ PASS", re.M)

MAKEFILE = """\
.PHONY: good exempt skipper later bad needsgood twoc needstwoc
twoc:
\t@echo "ONFRES NO2C twoc/SOFT2C: not built [D-691]"
needstwoc: twoc
\t@echo needstwoc-ran
good:
\t@echo good-ran
exempt:
\t@echo "ONFRES EXEMPT %(ex)s: absent [x]"
skipper:
\t@echo "ONFRES SKIP demo/skip: no widget"
needsgood: good
\t@echo needsgood-ran
bad:
\t@echo bad-ran
\t@exit 5
later:
\t@echo later-ran
"""


def t_testrun_make(make):
    if not make:
        # Reported through onfres itself: the one path this case would test.
        text, fatal = onfres.skipline(
            "onfres/runner-end-to-end", "no MAKE program given on the "
            "command line")
        print("  " + text)
        if fatal:
            check("runner end to end (strict mode requires a MAKE)", False)
        return
    d = tempfile.mkdtemp(prefix="onfly_tr_")
    try:
        io.open(os.path.join(d, "Makefile"), "w", encoding="utf-8",
                newline="\n").write(MAKEFILE % {"ex": sorted(onfres.EXEMPT)[0]})
        env = dict(os.environ)
        env.pop("MAKEFLAGS", None)
        env.pop("MAKELEVEL", None)
        env.pop("ONFLY_NOSKIP", None)
        env.pop("NO2C", None)

        def drive(targets):
            p = subprocess.run([sys.executable,
                                os.path.join(ROOT, "tools", "testrun.py"),
                                make] + targets, cwd=d, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return p.returncode, p.stdout.decode("utf-8", "replace")

        rc, out = drive(["good", "exempt", "skipper", "needsgood"])
        last = out.rstrip().splitlines()[-1]
        check("a clean run exits 0", rc == 0, "rc=%d" % rc)
        check("PASS counts targets, a skipped target is not a PASS",
              last.startswith("ONFLY test: 3 PASS, 1 SKIP, 0 PENDING, "
                              "1 EXEMPT"), repr(last))
        runs = [ln.strip() for ln in out.splitlines()]
        check("a target already made is not run again (-o)",
              runs.count("good-ran") == 1 and "needsgood-ran" in runs,
              "good-ran x%d" % runs.count("good-ran"))

        # The recipe exits 5, and make reports any failed recipe as its
        # own status 2; the runner must hand on make's status, not 0.
        rc, out = drive(["good", "bad", "later"])
        check("a failing target stops the run with make's status",
              rc == 2, "rc=%d" % rc)
        check("nothing after the failure runs", "later-ran" not in out)
        check("and the failure is named",
              "FAILED bad" in out, repr(out.rstrip().splitlines()[-1]))

        # D-691.  The dependent target is named FIRST, as TESTS names
        # `shim` before `fp`: in the other order it would get `-o twoc`,
        # the marker would never print in its sub-make, and this case
        # would prove nothing about prerequisites.
        rc, out = drive(["needstwoc", "twoc"])
        last = out.rstrip().splitlines()[-1]
        verdict = dict(
            (m.group(2), m.group(1)) for m in re.finditer(
                r"^  (\w+)\s+(needstwoc|twoc)\b", out, re.M))
        check("a NO2C run exits 0", rc == 0, "rc=%d" % rc)
        check("the marker printed in both sub-makes",
              out.count("ONFRES NO2C twoc/SOFT2C") == 2,
              "x%d" % out.count("ONFRES NO2C twoc/SOFT2C"))
        check("it demotes only the target it names",
              verdict == {"needstwoc": "PASS", "twoc": "NO2C"}, verdict)
        check("it is counted once, and the line names the switch",
              last.startswith("ONFLY test NO2C=1: 1 PASS, 0 SKIP, "
                              "0 PENDING, 0 EXEMPT, 1 NO2C ("), repr(last))
        check("no line of a NO2C run has 11.8's counted form",
              COUNTED.search(out) is None, "")
    finally:
        for name in os.listdir(d):
            os.remove(os.path.join(d, name))
        os.rmdir(d)


def make_list(name):
    """The words of a `NAME = ...` assignment in the Makefile, joined
    across backslash continuations."""
    text = io.open(os.path.join(ROOT, "Makefile"), encoding="utf-8").read()
    m = re.search(r"^%s\s*=\s*((?:.*\\\n)*.*)$" % name, text, re.M)
    return m.group(1).replace("\\\n", " ").split() if m else None


def t_makefile():
    # P-41 E9: test-nonet is the subset of `test` that needs no network,
    # fixed by the group 2 measurement of P-44.  Pinned here so that the
    # two lists cannot drift apart: every NONET target is a TESTS target,
    # in the same order, and none of the targets that measurement showed
    # needing a network is in it.
    tests, nonet = make_list("TESTS"), make_list("NONET")
    check("the Makefile defines TESTS and NONET",
          bool(tests) and bool(nonet),
          "TESTS %s, NONET %s" % (len(tests or []), len(nonet or [])))
    if not tests or not nonet:
        return
    check("NONET is TESTS' targets in TESTS' order",
          nonet == [t for t in tests if t in nonet]
          and set(nonet) <= set(tests), " ".join(nonet))
    needs = {"mvsrun", "names", "req", "golden", "prep"}
    check("NONET holds none of the targets that need a network",
          not (set(nonet) & needs), sorted(set(nonet) & needs))
    check("NONET is the 23 targets measured network-free",
          len(nonet) == 23, "%d" % len(nonet))

    # D-679, D-692: FREE2C is the subset of NONET that never had a Berkeley
    # SoftFloat 2c half.  D-679 named it NO2C; D-692 gave that name to the
    # switch, because a command-line NO2C=1 overrides any assignment of it.
    # It is pinned by reading the Makefile, not by a list written here: no
    # FREE2C target, and no target or variable it depends on, may name the
    # 2c sources, flags or derivation.  `shim` is the case that shows why
    # the walk goes through prerequisites: its own recipe never names 2c,
    # but it depends on `fp`, which builds a 2c test program.
    free = make_list("FREE2C")
    check("the Makefile defines FREE2C (D-692)", bool(free), repr(free))
    check("and no longer assigns NO2C, the switch's name (D-692)",
          make_list("NO2C") is None, repr(make_list("NO2C")))
    if not free:
        return
    check("FREE2C is NONET's targets in NONET's order",
          free == [t for t in nonet if t in free]
          and set(free) <= set(nonet), " ".join(free))
    text = io.open(os.path.join(ROOT, "Makefile"), encoding="utf-8").read()
    touched = [t for t in free if uses_2c(text, t, set())]
    check("no FREE2C target compiles SoftFloat 2c, directly or through a "
          "prerequisite", not touched, touched)
    check("the walk finds 2c where it is: shim through fp, and c2c",
          uses_2c(text, "shim", set()) and uses_2c(text, "c2c", set()))
    left = [t for t in nonet if t not in free
            and not uses_2c(text, t, set())]
    check("every NONET target free of 2c is in FREE2C", not left, left)
    # The dry-run walk below cannot run a target whose recipe names
    # $(MAKE): GNU make executes such a line even under -n.  `onfres` is
    # the one such target in TESTS, and the walk leaves it out.
    runs = [t for t in tests if t != "onfres" and any(
        "$(MAKE)" in r for _, r in rules(text, t))]
    check("no TESTS recipe but onfres's names $(MAKE)", not runs, runs)


# A recipe with a conditional inside it, as D-690's nine are written.  The
# walk must read BOTH branches: the 2c lines sit in the `else` one.
FIXTURE = """\
both: dep
\t@echo plain
ifeq ($(NO2C),1)
\t@echo none
else
\t$(CC) $(SF2CFLAGS) -o x_2c.exe x.c
endif
\t@echo after
# a comment among the recipe lines
\t@echo last
dep:
\t@echo dep
"""


def t_walk_fixture():
    body = " ".join(r for _, r in rules(FIXTURE, "both"))
    check("the text walk reads both branches of a recipe conditional",
          uses_2c(FIXTURE, "both", set()), repr(body[:60]))
    check("and the recipe lines after it, past a comment",
          "after" in body and "last" in body and "dep" not in body,
          repr(body[-40:]))


# The marks of SoftFloat 2c in the Makefile: its flags and sources
# (SF2CFLAGS, SF2CSRC, SF2CINC), its name map (generated/onf2cnm.h), its
# derivation (softfloat/derive2c.py into softfloat/c2c) and its upstream
# directory.  C2CFLAGS is not one: it is the plain C89 flag set.
TWO_C = re.compile(r"SF2C|onf2c|derive2c|SoftFloat-2c|softfloat/c2c")


#: Lines GNU make reads among a rule's recipe lines without ending the
#: recipe: blank lines, comments, and conditional directives (D-690 puts
#: a recipe's 2c lines in the `else` branch of an `ifeq`).
BETWEEN = re.compile(r"^(\s*$|#|(ifeq|ifneq|ifdef|ifndef)\b|else\b|endif\b)")


def rules(text, name):
    """(prerequisite words, recipe text) for every rule whose target is
    NAME.  A recipe is the tab-indented lines after the rule line, with
    lines continued by a backslash, read through BETWEEN lines and BOTH
    branches of a conditional, until any other line."""
    out = []
    lines = text.split("\n")
    head = re.compile(r"^%s\s*:(?!=)(.*)$" % re.escape(name))
    i = 0
    while i < len(lines):
        m = head.match(lines[i])
        if not m:
            i += 1
            continue
        pre = m.group(1)
        while pre.endswith("\\") and i + 1 < len(lines):
            i += 1
            pre = pre[:-1] + " " + lines[i]
        body = []
        i += 1
        while i < len(lines):
            line = lines[i]
            if line.startswith("\t") or (body and body[-1].endswith("\\")):
                body.append(line)
            elif not BETWEEN.match(line):
                break
            i += 1
        out.append((pre.split(), "\n".join(body)))
    return out


def uses_2c(text, name, seen):
    """True if target NAME, or anything it depends on, names SoftFloat 2c.
    A `$(VAR)` prerequisite is expanded through make_list; every word is
    then checked against TWO_C and followed as a target in its own right."""
    if name in seen:
        return False
    seen.add(name)
    for prereqs, recipe in rules(text, name):
        if TWO_C.search(recipe):
            return True
        for word in prereqs:
            v = re.match(r"^\$\((\w+)\)$", word)
            words = (make_list(v.group(1)) or []) if v else [word]
            for w in words:
                if TWO_C.search(w) or uses_2c(text, w, seen):
                    return True
    return False


# --- D-690, D-691: what NO2C=1 makes make do, read from make itself --------
#
# The text walk above parses the Makefile; this asks make.  Each TESTS
# target is dry-run (`make -n -B`) with and without NO2C=1, and the two
# command lists are compared.  It is the main proof of P-52: the switch
# removes every 2c command, prints a marker for each 2c half, and leaves
# every SOFT3E and NATIVE command exactly as the full build has it.

#: P-52 S1: the TESTS targets whose dry run names SoftFloat 2c.  Fixed
#: here, so that a target which gains a 2c half fails this walk until it
#: is handled.  `shim` reaches 2c only through `fp`.
TEN = ("c04mvs", "tt02", "c2c", "shim", "fp", "kernel", "syn", "eng",
       "req", "golden")

#: The two of them that are 2c and nothing else: under NO2C=1 they run
#: their marker and nothing more, not even their prerequisites.
WHOLE = ("c04mvs", "c2c")

#: 2c in an EXPANDED command: its sources, flags, name map and vectors and
#: their generators, its derivation, the backend's adapter and programs.
TWO_C_RUN = re.compile(r"softfloat/c2c|SoftFloat-2c|derive2c|gen2c|onf2c"
                       r"|ONF_FP_SOFT2C|onffp2\.c|_2c\.exe|tstc2c|tst2c"
                       r"|obj2c")
TWO_C_EXE = re.compile(r"\S*_2c\.exe")
MARKER = re.compile(r"tools/onfres\.py no2c (\S+)")


def commands(text):
    """A dry run's commands: backslash continuations joined and runs of
    whitespace collapsed, since dropping one argument moves make's line
    split."""
    out, cur = [], ""
    for line in text.splitlines():
        if line.endswith("\\"):
            cur += line[:-1] + " "
            continue
        cmd = " ".join((cur + line).split())
        cur = ""
        if cmd:
            out.append(cmd)
    if cur.strip():
        out.append(" ".join(cur.split()))
    return out


def dry(make, target, *assign):
    """(status, output) of `make -n -B TARGET` in this checkout.

    MAKEFLAGS, MAKELEVEL and NO2C are removed, so an outer NO2C=1 run
    cannot make the "full" side NO2C too; ONFPLAT, PYTHON and CC are passed
    on the command line when the outer run set them.  TFPREREQ= keeps the
    TestFloat build, whose recipe names $(MAKE), out of the dry run (it is
    SoftFloat 3e's, not 2c's).  ONFLY_DRYRUN stops a nested test_onfres
    from walking again, should a recipe ever run it.
    """
    env = dict(os.environ)
    for k in ("MAKEFLAGS", "MAKELEVEL", "MFLAGS", "NO2C", "ONFLY_NOSKIP"):
        env.pop(k, None)
    env["ONFLY_DRYRUN"] = "1"
    cmd = [make, "-n", "-B", "--no-print-directory", "TFPREREQ="]
    cmd += ["%s=%s" % (k, os.environ[k]) for k in ("ONFPLAT", "PYTHON", "CC")
            if k in os.environ]
    p = subprocess.run(cmd + list(assign) + [target], cwd=ROOT, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def runs_make(text, name, seen):
    """True if target NAME, or anything it depends on, has a recipe that
    names $(MAKE), which GNU make executes even under -n."""
    if name in seen:
        return False
    seen.add(name)
    for prereqs, recipe in rules(text, name):
        if "$(MAKE)" in recipe:
            return True
        if any(runs_make(text, w, seen) for w in prereqs):
            return True
    return False


def expect_no2c(full):
    """The full dry run's commands as NO2C=1 must give them: a 2c build or
    run is gone, and a comparator keeps its other programs."""
    out = []
    for c in full:
        s = " ".join(TWO_C_EXE.sub("", c).split())
        if TWO_C_RUN.search(s):
            continue
        if s != c and ".exe" not in s:
            continue
        out.append(s)
    return out


def t_dryrun(make):
    why = None
    if os.environ.get("ONFLY_DRYRUN") == "1":
        why = "run inside one of this walk's own dry runs"
    elif not make:
        why = "no MAKE program given on the command line"
    if why:
        text, fatal = onfres.skipline("onfres/no2c-dry-run", why)
        print("  " + text)
        if fatal:
            check("NO2C dry-run walk (strict mode requires a MAKE)", False)
        return
    halves = set(getattr(onfres, "NO2C_HALVES", ()))
    tests = [t for t in make_list("TESTS") or [] if t != "onfres"]
    named, leaks, drift, same, marks_bad, seen = [], [], [], [], [], set()
    for t in tests:
        rc1, out1 = dry(make, t)
        rc2, out2 = dry(make, t, "NO2C=1")
        if rc1 or rc2:
            check("dry run of %s exits 0 both ways" % t, False,
                  "rc=%d,%d %r" % (rc1, rc2, out2[-120:]))
            continue
        full, sw = commands(out1), commands(out2)
        if any(TWO_C_RUN.search(c) for c in full):
            named.append(t)
        if any(TWO_C_RUN.search(c) for c in sw):
            leaks.append(t)
        marks = [m.group(1) for c in sw for m in MARKER.finditer(c)]
        seen.update(marks)
        want = [] if t in WHOLE else expect_no2c(full)
        if [c for c in sw if not MARKER.search(c)] != want:
            drift.append(t)
        if t not in TEN and sw == full:
            same.append(t)
        own = "%s/SOFT2C" % t
        if (bool(marks) != (t in TEN) or not set(marks) <= halves
                or (own in marks) != (own in halves)):
            marks_bad.append((t, marks))
    check("without NO2C=1, exactly P-52's ten targets name 2c",
          named == [t for t in tests if t in TEN] and len(named) == 10,
          named)
    check("with NO2C=1, no TESTS target names 2c", not leaks, leaks)
    check("with NO2C=1, every other command is the full build's, less "
          "its 2c programs; c04mvs and c2c run only their marker",
          not drift, drift)
    check("the %d targets free of 2c dry-run identically both ways"
          % (len(tests) - 10), len(same) == len(tests) - 10, len(same))
    check("each target with a 2c half prints its declared NO2C marker",
          not marks_bad, marks_bad)
    check("the markers printed are exactly onfres's nine halves",
          seen == halves and len(seen) == 9, sorted(seen))
    # D-694: under NO2C=1 no target at all names 2c, not only the test
    # targets; `tf2`, which is 2c and nothing else, refuses instead.  The
    # targets whose recipes, or whose prerequisites' recipes, name $(MAKE)
    # cannot be dry-run and are pinned, so a new one is noticed.
    text = io.open(os.path.join(ROOT, "Makefile"), encoding="utf-8").read()
    every = sorted(set(re.findall(r"^([a-z][\w-]*)\s*:(?!=)", text, re.M)))
    calls = [n for n in every if runs_make(text, n, set())]
    check("the targets that run make are the seven expected",
          calls == ["all", "onfres", "quick", "test", "test-no2c",
                    "test-nonet", "testfloat"], calls)
    others, refused = [], None
    for n in every:
        if n in calls or n in tests:
            continue
        rc, out = dry(make, n, "NO2C=1")
        if n == "tf2":
            refused = rc != 0 and "D-694" in out
        elif rc or any(TWO_C_RUN.search(c) for c in commands(out)):
            others.append(n)
    check("with NO2C=1, no other Makefile target names 2c (D-694)",
          not others, others)
    check("and tf2, which is 2c and nothing else, refuses (D-694)",
          refused is True, "refused=%r" % refused)
    rc, out = dry(make, "layout", "NO2C=yes")
    check("NO2C=yes stops make before anything is built",
          rc != 0 and "NO2C is 'yes'" in out, "rc=%d %r" % (rc, out[-90:]))
    rc0, zero = dry(make, "fp", "NO2C=0")
    rc1, full = dry(make, "fp")
    check("NO2C=0 is the full build", rc0 == 0 and zero == full,
          "rc=%d" % rc0)


def main(argv):
    make = argv[1] if len(argv) > 1 else None
    t_onfres()
    t_no2c()
    t_makefile()
    t_walk_fixture()
    t_dryrun(make)
    t_unittest()
    t_lastln()
    t_testrun_scan()
    t_testrun_make(make)
    print("test_onfres: %d passed, %d failed" % (ok, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
