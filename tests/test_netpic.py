# -*- coding: utf-8 -*-
"""D-628: the picture of the shipped subcircuit says what it shows.

WHY THIS TEST EXISTS
--------------------
`tools/netpic.py` draws the 501-neuron `srext` subcircuit from its soma
coordinates for the README and the site.  A picture is the easiest place for
a claim to drift: a count typed into a caption, an imputed position drawn as
if it were measured, or the MaleCNS attribution that CC BY 4.0 and P-41 7.1
rule 10 require being left off because it spoils the look.  So the numbers
the picture prints are taken from the data, and this test holds them to it.

WHAT IT CHECKS
--------------
The attribution line names MaleCNS v1.0, its four creators, CC BY 4.0 and
the modification, and it is drawn INSIDE the figure, not only in a caption
beside it.  The role counts come from the geometry file (14 stimulus, 2
readout, 19 imputed).  Excitatory and inhibitory connections are counted
from the weights' signs, and on the shipped network they come to all 10,783
of its edges.  Two renders of the same input are byte-identical, so the
committed PNG can be regenerated and checked (FR-PRP-09's spirit).

It runs in the `netpic` target, before the picture is drawn, and not in
`make test`: matplotlib is in `requirements-live.txt`, not in the
`requirements.txt` a replicator installs for the suite.

usage:  python tests/test_netpic.py
"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "layout"))

import onfres  # noqa: E402

try:
    import matplotlib  # noqa: E402,F401
except ImportError:
    onfres.skip("test_netpic/matplotlib", "matplotlib is not installed; it "
                "is in requirements-live.txt, not requirements.txt")
    raise SystemExit(0)

import netpic   # noqa: E402

SREXT = os.path.join(ROOT, "data", "networks",
                     "onfnet-malecns-v1.0-srext.bin")


def synthetic_spec(doc):
    """A spec shaped like layout/netread.py's, with three known edges."""
    n = len(doc["neurons"])
    rowptr = [0] * (n + 1)
    target, weight = [], []
    edges = {0: [(1, 0.5), (2, -0.25)], 3: [(4, 1.0)]}
    for i in range(n):
        for t, w in edges.get(i, []):
            target.append(t)
            weight.append(w)
        rowptr[i + 1] = len(target)
    stim = [r["index"] for r in doc["neurons"] if r["role"] == "stimulus"]
    read = [r["index"] for r in doc["neurons"] if r["role"] == "readout"]
    return {"n": n, "rowptr": rowptr, "target": target, "weight": weight,
            "stim": stim, "readout": read, "e": len(target)}


class Attribution(unittest.TestCase):

    def test_names_the_dataset_its_creators_licence_and_change(self):
        a = netpic.attribution()
        for want in ("MaleCNS v1.0", "HHMI Janelia", "MRC LMB",
                     "University of Cambridge", "Google Research",
                     "CC BY 4.0", "modified by FlyBatch"):
            self.assertIn(want, a)

    def test_is_drawn_inside_the_figure(self):
        doc, cloud = netpic.load_geometry()
        fig = netpic.figure(doc, cloud, synthetic_spec(doc))
        texts = [t.get_text() for t in fig.texts]
        self.assertIn(netpic.attribution(), texts)


class Counts(unittest.TestCase):

    def test_roles_come_from_the_geometry(self):
        doc, _ = netpic.load_geometry()
        c = netpic.counts(doc)
        self.assertEqual((c["neurons"], c["stimulus"], c["readout"],
                          c["imputed"]), (501, 14, 2, 19))

    def test_edge_signs_are_counted_from_the_weights(self):
        doc, _ = netpic.load_geometry()
        self.assertEqual(netpic.edge_counts(synthetic_spec(doc)), (2, 1))

    @unittest.skipUnless(os.path.exists(SREXT), "srext is not staged")
    def test_the_shipped_network_accounts_for_every_edge(self):
        import netread
        spec = netread.read(SREXT)
        exc, inh = netpic.edge_counts(spec)
        self.assertEqual(exc + inh, spec["e"])
        self.assertEqual(spec["e"], 10783)


class Deterministic(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="test_netpic_")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_two_renders_are_byte_identical(self):
        doc, cloud = netpic.load_geometry()
        spec = synthetic_spec(doc)
        a = os.path.join(self.dir, "a.png")
        b = os.path.join(self.dir, "b.png")
        netpic.render(a, doc, cloud, spec)
        netpic.render(b, doc, cloud, spec)
        with open(a, "rb") as fa, open(b, "rb") as fb:
            self.assertEqual(fa.read(), fb.read())


if __name__ == "__main__":
    # D-555: skips are reported through onfres so that make test counts them.
    sys.exit(onfres.unittest_main("test_netpic"))
