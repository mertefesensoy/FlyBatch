# -*- coding: utf-8 -*-
"""D-635 (P-41 item 22): the G0 inventory shows the home directory as ~.

WHY THIS TEST EXISTS
--------------------
`data/g0/inventory.json` is a committed record, and `tools/g0.py` wrote
into it whatever the host's paths were: the interpreter it ran under, the
COBOL compiler it found, the virtual environment it probed.  On the owner's
host every one of those sits under the user's home directory, so the
record published a personal folder layout that says nothing about Gate
G0.  D-635 keeps the record as it stands, as evidence, and masks the home
directory as `~` in what `g0.py` writes from now on.

WHAT IT CHECKS
--------------
`tilde()` masks the home directory in either slash form and at any depth
of a nested record, and leaves every other path alone; `merge()` masks the
section it writes and leaves the sections already in the file untouched,
because those are the evidence D-635 keeps.

usage:  python tests/test_g0.py
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import g0      # noqa: E402
import onfres  # noqa: E402

HOME = os.path.expanduser("~")


class Tilde(unittest.TestCase):

    def test_the_home_directory_becomes_a_tilde(self):
        exe = os.path.join(HOME, "venv", "python.exe")
        self.assertEqual(g0.tilde(exe),
                         "~" + exe[len(HOME):])

    def test_the_forward_slash_spelling_is_masked_too(self):
        exe = HOME.replace("\\", "/") + "/venv/python.exe"
        self.assertEqual(g0.tilde(exe), "~/venv/python.exe")

    def test_inside_a_command_line(self):
        cmd = os.path.join(HOME, "python.exe") + " --version"
        self.assertEqual(g0.tilde(cmd), "~" + os.sep + "python.exe --version")

    def test_a_nested_record_is_masked_throughout(self):
        exe = os.path.join(HOME, "p.exe")
        rec = {"tools": {"python": {"command": exe, "rc": 0}},
               "list": [exe, 3]}
        got = g0.tilde(rec)
        self.assertEqual(got["tools"]["python"]["command"], "~" + os.sep
                         + "p.exe")
        self.assertEqual(got["tools"]["python"]["rc"], 0)
        self.assertEqual(got["list"], ["~" + os.sep + "p.exe", 3])

    def test_other_paths_are_left_alone(self):
        for s in ("C:\\MinGW\\bin\\gcc.exe", "/usr/bin/gcc", "gcc 6.3.0"):
            self.assertEqual(g0.tilde(s), s)


class Merge(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="test_g0_")
        self.path = os.path.join(self.dir, "inventory.json")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_the_new_section_is_masked_and_the_old_one_kept(self):
        exe = os.path.join(HOME, "python.exe")
        io.open(self.path, "w", encoding="utf-8").write(
            json.dumps({"old": {"python": exe}}))
        g0.merge("x86", {"python": exe}, path=self.path)
        doc = json.loads(io.open(self.path, encoding="utf-8").read())
        self.assertEqual(doc["x86"]["python"], "~" + os.sep + "python.exe")
        self.assertEqual(doc["old"]["python"], exe,
                         "merge() rewrote evidence recorded before D-635")


if __name__ == "__main__":
    # D-555: skips are reported through onfres so that make test counts them.
    sys.exit(onfres.unittest_main("test_g0"))
