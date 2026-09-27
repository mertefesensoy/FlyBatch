# -*- coding: utf-8 -*-
"""Draw the shipped 501-neuron subcircuit as a still picture (D-628).

WHY THIS EXISTS
---------------
The README and the site need one image that shows what FlyBatch simulates:
the `srext` subcircuit, where its neurons sit in the fly's nervous system and
how densely they are wired.  The live view (`tools/liveview.py`) already
draws the somata over time from a running engine; this draws the network
itself, still, with its connections, and needs no engine at all.

It reuses the live view's geometry and projection, so the two pictures put
every neuron in the same place, and `layout/netread.py`, the verified Python
decode of the network file, so the connections drawn are the file's own.

WHAT IT DRAWS
-------------
* Every connection of the network as a faint line, coloured by the sign of
  its weight: excitatory warm, inhibitory cool.
* Each of the 501 somata.  The 19 imputed positions (D-384) are hollow
  rings, never dots; the 14 sugar-sensing stimulus neurons are triangles and
  the 2 MN9 readout neurons stars, so colour is never the only encoding.
* A faint backdrop of MaleCNS somata, every 7th, from `data/geom/`.
* The counts, taken from the data, and the attribution line that CC BY 4.0
  and P-41 7.1 rule 10 require, drawn inside the image.

LIMITS
------
Positions are somata, not neurites, and the projection is prep/geom.py's
measurement.  A picture of connections says nothing about activity; the
live view shows that.

Run:
    python tools/netpic.py                       writes docs/media/srext-network.png
    python tools/netpic.py --out <path> [--net <network file>]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "layout"))

from liveview import load_geometry, project     # noqa: E402

NET = os.path.join(ROOT, "data", "networks", "onfnet-malecns-v1.0-srext.bin")
OUT = os.path.join(ROOT, "docs", "media", "srext-network.png")

BG = "#0b0d12"
INK = "#d6deee"
MUTED = "#8a96ad"
EXC = "#ff9f43"
INH = "#7b8cff"
STIM = "#4cc9f0"
READ = "#f72585"


def attribution():
    """The line P-41 7.1 rule 10 requires on a MaleCNS-derived image."""
    return ("Data: MaleCNS v1.0 (HHMI Janelia, MRC LMB, University of "
            "Cambridge, Google Research), CC BY 4.0, modified by FlyBatch.")


def counts(doc):
    rows = doc["neurons"]
    return {"neurons": len(rows),
            "stimulus": sum(1 for r in rows if r["role"] == "stimulus"),
            "readout": sum(1 for r in rows if r["role"] == "readout"),
            "imputed": sum(1 for r in rows if r["placed"])}


def edge_counts(spec):
    """(excitatory, inhibitory) connections, from the weights' signs."""
    exc = sum(1 for w in spec["weight"] if w > 0)
    inh = sum(1 for w in spec["weight"] if w < 0)
    return exc, inh


def figure(doc, cloud, spec):
    """The picture as a matplotlib Figure; nothing is written."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.lines import Line2D

    rows = sorted(doc["neurons"], key=lambda r: r["index"])
    if len(rows) != spec["n"]:
        raise SystemExit("the geometry lists %d neurons, the network %d"
                         % (len(rows), spec["n"]))
    gx, gy = project(doc, [(r["x"], r["y"], r["z"]) for r in rows])
    c = counts(doc)
    exc, inh = edge_counts(spec)

    fig = plt.figure(figsize=(16, 10), dpi=100, facecolor=BG)
    ax = fig.add_axes([0.02, 0.07, 0.62, 0.80])
    ax.set_facecolor(BG)
    ax.set_axis_off()
    ax.set_aspect("equal")

    if cloud:
        cx, cy = project(doc, cloud)
        ax.scatter(cx, cy, s=0.8, c="#1b2233", linewidths=0, zorder=1)

    segs = {1: [], -1: []}
    rp, tg, wt = spec["rowptr"], spec["target"], spec["weight"]
    for i in range(spec["n"]):
        for k in range(rp[i], rp[i + 1]):
            if wt[k] != 0:
                segs[1 if wt[k] > 0 else -1].append(
                    [(gx[i], gy[i]), (gx[tg[k]], gy[tg[k]])])
    ax.add_collection(LineCollection(segs[-1], colors=INH, linewidths=0.35,
                                     alpha=0.10, zorder=2))
    ax.add_collection(LineCollection(segs[1], colors=EXC, linewidths=0.35,
                                     alpha=0.10, zorder=3))

    inter = [r["index"] for r in rows
             if r["role"] not in ("stimulus", "readout") and not r["placed"]]
    placed = [r["index"] for r in rows
              if r["role"] not in ("stimulus", "readout") and r["placed"]]
    stim = [r["index"] for r in rows if r["role"] == "stimulus"]
    read = [r["index"] for r in rows if r["role"] == "readout"]
    ax.scatter([gx[i] for i in inter], [gy[i] for i in inter], s=10,
               c="#c9d4ea", linewidths=0, zorder=4)
    ax.scatter([gx[i] for i in placed], [gy[i] for i in placed], s=34,
               facecolors="none", edgecolors="#6b7a99", linewidths=0.9,
               zorder=4)
    ax.scatter([gx[i] for i in stim], [gy[i] for i in stim], s=90,
               marker="^", facecolors="none", edgecolors=STIM,
               linewidths=1.4, zorder=5)
    ax.scatter([gx[i] for i in read], [gy[i] for i in read], s=260,
               marker="*", c=READ, linewidths=0, zorder=6)

    fig.text(0.03, 0.935, "FlyBatch", color=INK, fontsize=30,
             fontweight="bold")
    fig.text(0.03, 0.895, "The sugar-to-feeding subcircuit of the male fruit "
             "fly: %d neurons and %s connections from the MaleCNS v1.0 "
             "connectome" % (c["neurons"], "{:,}".format(spec["e"])),
             color=MUTED, fontsize=13)

    handles = [
        Line2D([], [], marker="*", linestyle="none", markersize=15,
               markerfacecolor=READ, markeredgecolor="none",
               label="MN9 feeding motor neuron (%d)" % c["readout"]),
        Line2D([], [], marker="^", linestyle="none", markersize=10,
               markerfacecolor="none", markeredgecolor=STIM,
               label="sugar-sensing stimulus neuron (%d)" % c["stimulus"]),
        Line2D([], [], marker="o", linestyle="none", markersize=5,
               markerfacecolor="#c9d4ea", markeredgecolor="none",
               label="interneuron, measured soma"),
        Line2D([], [], marker="o", linestyle="none", markersize=7,
               markerfacecolor="none", markeredgecolor="#6b7a99",
               label="interneuron, soma imputed (%d)" % len(placed)),
        Line2D([], [], color=EXC, linewidth=2,
               label="excitatory connection (%s)" % "{:,}".format(exc)),
        Line2D([], [], color=INH, linewidth=2,
               label="inhibitory connection (%s)" % "{:,}".format(inh)),
        Line2D([], [], marker="o", linestyle="none", markersize=3,
               markerfacecolor="#3a4660", markeredgecolor="none",
               label="other MaleCNS somata, every 7th"),
    ]
    leg = fig.legend(handles=handles, loc="upper left",
                     bbox_to_anchor=(0.665, 0.80), frameon=False,
                     fontsize=12.5, labelspacing=1.1, handletextpad=0.8)
    for t in leg.get_texts():
        t.set_color(INK)

    notes = ("Soma positions, not neurites. %d of %d positions are\n"
             "imputed (D-384), the %d sugar-sensing neurons among them:\n"
             "their cell bodies lie outside the imaged volume, so they\n"
             "are drawn where their axons end. The projection is the one\n"
             "prep/geom.py measured. Connections are straight lines\n"
             "between somata; they show wiring, not activity."
             % (c["imputed"], c["neurons"], c["stimulus"]))
    fig.text(0.667, 0.32, notes, color=MUTED, fontsize=10.5,
             linespacing=1.5, va="top")
    fig.text(0.03, 0.035, attribution(), color=MUTED, fontsize=10.5)
    return fig


def render(path, doc, cloud, spec):
    """Write the picture as a PNG with no timestamp or version metadata, so
    the same input gives the same bytes."""
    import matplotlib.pyplot as plt
    fig = figure(doc, cloud, spec)
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor(),
                metadata={"Software": None})
    plt.close(fig)
    return path


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--net", default=NET)
    a = ap.parse_args(argv)
    import netread
    spec = netread.read(a.net)
    doc, cloud = load_geometry()
    render(a.out, doc, cloud, spec)
    exc, inh = edge_counts(spec)
    print("netpic: wrote %s (%d neurons, %d connections: %d excitatory, "
          "%d inhibitory)" % (a.out.replace("\\", "/"), spec["n"], spec["e"],
                              exc, inh))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
