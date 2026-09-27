# Notice: the Shiu reference curve

`mn9-reference.csv` in this directory is the MN9 firing-rate curve FlyBatch
calibrates and validates against (SRS SR-CAL-04, D-164). It was produced on
2026-09-12 by `reference/shiu/rerun.py`, which re-runs the Figure 1D protocol
of Shiu et al. (2024) with their published MIT code (`model.py`, `utils.py`)
on FlyWire connectome files from snapshot 630. Those FlyWire files are not in
this repository; their digests are in `MANIFEST.json` beside this file.

FlyWire's guidelines (https://flywire.ai/guidelines) state that its public
release data is under CC BY-NC 4.0, a non-commercial licence. That page names
release v783 and does not name snapshot 630 explicitly.

**Licence: CC BY-NC 4.0 (SRS D-625, 2026-09-27).** This directory, and the
other files that embed the curve's values, are offered under CC BY-NC 4.0,
https://creativecommons.org/licenses/by-nc/4.0/, the licence FlyWire's
guidelines give its data, with FlyWire's attribution; the text is
`LICENSES/CC-BY-NC-4.0.txt`. The MIT licence in the repository's `LICENSE` is
not claimed for this directory. FlyBatch's position is that the synaptic weight
fitted to the curve, a single number, is not adapted material of FlyWire's
data, so the network files stay under CC BY 4.0; that position was taken
without legal advice. `THIRD_PARTY_NOTICES.md`,
section 6, lists every path this affects and the papers FlyWire asks users to
cite. This notice is not legal advice.
