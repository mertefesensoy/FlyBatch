# -*- coding: utf-8 -*-
"""Hold the FAQ and the write-up to P-41's claims register (D-622).

WHY THIS EXISTS
---------------
P-41 3.1 makes one rule for every public sentence about what FlyBatch does
or has shown: it comes from the claims register, and every register entry
cites the D- or VL-row that evidences it.  `docs/FAQ.md` is reused as saved
replies and `docs/writeup.md` is what outreach links to, so a sentence that
drifts from the evidence there is repeated everywhere they are quoted.  Both
were drafted by the engineer (D-617), which makes a mechanical check more
important, not less.

WHAT IT CHECKS
--------------
1. Both files exist.
2. Every answer paragraph cites at least one evidence id: a register entry
   (CAN-nn), a decision (D-nnn) or a verification limit (VL-nnn).  A
   paragraph is a run of non-blank lines; headings, table rules and code
   blocks are not answer paragraphs.
3. Every cited id exists: CAN ids in P-41 Section 5.1, D-rows in the SRS's
   Appendix A.1, VL-rows in its Appendix D.
4. No phrase from P-41 Section 5.2, the MUST-NOT list, appears outside a
   heading.  A question may quote the phrase it answers ("Is this a brain
   upload?"); an answer may not use it, not even negated, so that a quoted
   fragment of an answer cannot say it either.  Matching ignores case,
   hyphens and runs of whitespace.

WHAT IT CANNOT DO
-----------------
It checks that each paragraph points at evidence, not that the evidence
says what the paragraph says.  That remains a reading, done when the owner
approves the text (D-617).

usage:  python tools/lint_reg.py [--self-test]
        exit 0 clean, 1 on a finding, 2 on an internal error
"""
import io
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = ("docs/FAQ.md", "docs/writeup.md")
SRS = "docs/ONFLY-SRS.md"
PLAN = "docs/plan/2026-09-24-open-source-launch.md"

ID_RE = re.compile(r"\b(CAN-\d+|D-\d+|VL-\d+)\b")

# P-41 Section 5.2, as phrases a sentence could actually contain.  Kept to
# the unambiguous ones: "z/OS" or "mainframe" alone are needed to say what
# FlyBatch has NOT done, so the list names the claims, not the words.
MUST_NOT = (
    "runs on IBM Z", "ran on IBM Z hardware and", "runs on a mainframe",
    "runs on z/OS", "runs on LinuxONE", "real s390x hardware result",
    "served as a CICS transaction", "runs on CICS", "CICS-ready",
    "slower than a mainframe", "MIPS equivalent",
    "reproduces Shiu", "matches the fly", "within 25% of the published model",
    "the whole fly brain", "whole brain", "the complete connectome",
    "all synapses", "pure-connectome",
    "criteria fixed in advance", "fixed in advance",
    "all criteria passed as originally written",
    "validated on MVS", "validated on the mainframe",
    "passes on every platform",
    "reproduce everything",
    "deterministic means correct",
    "robust under re-measurement",
    "world's first", "the first ever", "endorsed by IBM",
    "unmodified SoftFloat", "Enterprise COBOL-compatible",
    "brain upload", "uploading a fly brain", "brain emulation",
    "digital fly", "bit-identical on every", "IEEE arithmetic done by S/370",
)


def norm(text):
    return " ".join(text.replace("-", " ").lower().split())


def read(root, rel):
    try:
        with io.open(os.path.join(root, *rel.split("/")),
                     encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def known_ids(root):
    """Every id the texts may cite: (CAN set, D set, VL set)."""
    srs = read(root, SRS) or ""
    plan = read(root, PLAN) or ""
    can = set(re.findall(r"^\| (CAN-\d+) \|", plan, re.M))
    d = set(re.findall(r"^\| (D-\d+) \|", srs, re.M))
    vl = set(re.findall(r"^\| (VL-\d+) \|", srs, re.M))
    return can, d, vl


def paragraphs(text):
    """(first line number, paragraph text) for each answer paragraph."""
    out, cur, start, fence = [], [], 0, False
    lines = text.split("\n")
    rule = re.compile(r"^\|[-| :]+\|$")
    for n, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            if cur:
                out.append((start, " ".join(cur)))
                cur = []
            continue
        if fence or not s or s.startswith("#") or rule.match(s):
            if cur:
                out.append((start, " ".join(cur)))
                cur = []
            continue
        if s.startswith("|"):
            # A table: its header row (the one above the rule) holds column
            # names, not claims; every body row is checked on its own.
            if cur:
                out.append((start, " ".join(cur)))
                cur = []
            nxt = lines[n].strip() if n < len(lines) else ""
            if not rule.match(nxt):
                out.append((n, s))
            continue
        if not cur:
            start = n
        cur.append(s)
    if cur:
        out.append((start, " ".join(cur)))
    return out


def findings(root):
    can, d, vl = known_ids(root)
    banned = [(p, norm(p)) for p in MUST_NOT]
    out = []
    for rel in FILES:
        text = read(root, rel)
        if text is None:
            out.append("%s: missing" % rel)
            continue
        for line, para in paragraphs(text):
            ids = ID_RE.findall(para)
            if not ids:
                out.append("%s:%d: a paragraph cites no CAN, D or VL id: "
                           "%.60s" % (rel, line, para))
            for i in ids:
                pool = can if i.startswith("CAN-") else \
                    d if i.startswith("D-") else vl
                if i not in pool:
                    out.append("%s:%d: cites %s, which does not exist"
                               % (rel, line, i))
            flat = norm(para)
            for phrase, key in banned:
                if key in flat:
                    out.append("%s:%d: uses the P-41 5.2 phrase '%s'"
                               % (rel, line, phrase))
    return out


def self_test():
    checks = [0, 0]

    def check(name, ok):
        checks[0] += 1
        if not ok:
            checks[1] += 1
            print("lint_reg: self-test FAIL: %s" % name)

    def tree(faq, writeup="The engine is C89 (D-19).\n"):
        root = tempfile.mkdtemp(prefix="lint_reg_")
        os.makedirs(os.path.join(root, "docs", "plan"))
        with io.open(os.path.join(root, *SRS.split("/")), "w",
                     encoding="utf-8") as fh:
            fh.write("| D-19 | x |\n| D-205 | x |\n| VL-05 | x |\n")
        with io.open(os.path.join(root, *PLAN.split("/")), "w",
                     encoding="utf-8") as fh:
            fh.write("| CAN-01 | x |\n| CAN-15 | x |\n")
        for rel, text in (("docs/FAQ.md", faq), ("docs/writeup.md", writeup)):
            if text is not None:
                with io.open(os.path.join(root, *rel.split("/")), "w",
                             encoding="utf-8") as fh:
                    fh.write(text)
        return root

    good = ("# FAQ\n\n## Is this a brain upload?\n\nNo. It is a 501-neuron "
            "subcircuit (CAN-01, D-205).\n\n## Does agreement prove "
            "correctness?\n\nNo (VL-05).\n")
    cases = (
        ("a good pair passes", good, 0),
        ("a paragraph with no id", good + "\nThis sentence cites nothing.\n",
         1),
        ("an id that does not exist", good + "\nIt is fast (VL-999).\n", 1),
        ("a CAN id not in the register", good + "\nSee CAN-99.\n", 1),
        ("a MUST-NOT phrase in an answer", good.replace(
            "No. It is", "No, it is not whole-brain emulation. It is"), 1),
        ("the same phrase negated is still refused", good +
         "\nIt is not a digital fly (CAN-01).\n", 1),
        ("a MUST-NOT phrase in a heading is allowed", good +
         "\n## Is it a digital fly?\n\nNo (CAN-01).\n", 0),
        ("case and hyphens do not hide a phrase", good +
         "\nA Brain-Upload, in effect (CAN-01).\n", 1),
        ("the write-up is checked too", good, 0),
        ("a missing FAQ", None, 1),
        ("a table rule is not a paragraph", good +
         "\n| a | b |\n|---|---|\n| x (D-19) | y (D-19) |\n", 0),
        ("a code block is not a paragraph", good +
         "\n```\nmake test\n```\n", 0),
    )
    for name, faq, want in cases:
        root = tree(faq)
        try:
            got = findings(root)
            check(name, (len(got) == 0) if want == 0 else (len(got) >= want))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    root = tree(good, writeup="Clone it and reproduce everything.\n")
    try:
        check("a write-up paragraph with no id and a phrase",
              len(findings(root)) >= 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("lint_reg: self-test %d checks, %d failed" % tuple(checks))
    return 1 if checks[1] else 0


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    if argv:
        sys.stderr.write(__doc__.split("usage:")[1])
        return 2
    got = findings(ROOT)
    if not got:
        print("lint_reg: ok -- %s cite only ids that exist and use no "
              "P-41 5.2 phrase" % " and ".join(FILES))
        return 0
    print("lint_reg: %d finding(s). P-41 3.1: every public sentence comes "
          "from the claims register (D-622)." % len(got))
    for f in got:
        print("  " + f)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write("lint_reg: internal error: %s: %s\n"
                         % (type(exc).__name__, exc))
        sys.exit(2)
