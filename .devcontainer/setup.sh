#!/bin/sh
# FlyBatch dev container setup (SRS D-678).  Run once when a Codespace or a
# local dev container is created, and by the `devcontainer` CI job, so the
# job checks exactly what a newcomer gets.
#
# 1. The pinned Python packages, from requirements.txt only.
# 2. The two distributed networks, `srext` and `path`, from the release
#    named by NETWORKS_TAG in .github/workflows/ci.yml (the line the
#    `golden` job reads, moved at each release), checked against that
#    release's SHA256SUMS and placed by tools/fixtures.py, so `make quick`
#    works as well as `make test-nonet`.  FLYBATCH_NO_NETWORKS=1 skips this.
#
# Nothing is built here.  Every engine build contains Berkeley SoftFloat
# Release 2c, whose terms are in THIRD_PARTY_NOTICES.md, section 3; read
# them before the first `make`.  `make test-no2c` never compiles it.
set -eu

python -m pip install -r requirements.txt

if [ "${FLYBATCH_NO_NETWORKS:-}" = "1" ]; then
    echo "setup: networks skipped (FLYBATCH_NO_NETWORKS=1)"
    exit 0
fi

tag=$(sed -n 's/^ *NETWORKS_TAG: *//p' .github/workflows/ci.yml | head -n 1)
if [ -z "$tag" ]; then
    echo "setup: no NETWORKS_TAG in .github/workflows/ci.yml" >&2
    exit 1
fi

nets="${TMPDIR:-/tmp}/flybatch-nets"
mkdir -p "$nets"
base="https://github.com/mertefesensoy/FlyBatch/releases/download/$tag"
for f in onfnet-malecns-v1.0-srext.bin onfnet-malecns-v1.0-path.bin \
         SHA256SUMS NETWORKS-NOTICE.md; do
    curl -fsSL -o "$nets/$f" "$base/$f"
done
(cd "$nets" && sha256sum -c SHA256SUMS)
python tools/fixtures.py --from "$nets"
python tools/fixtures.py --check

cat <<'EOF'

setup: done.  On this Linux x86-64 container:
  make ONFPLAT=x86l PYTHON=python test-no2c    never compiles SoftFloat 2c
  make ONFPLAT=x86l PYTHON=python quick        the 19 golden fingerprints
  make ONFPLAT=x86l PYTHON=python test-nonet   what CI runs
Add ONFLY_NOSKIP=1 before `make` so a missing file fails instead of skipping.
EOF
