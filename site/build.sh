#!/usr/bin/env bash
# Assemble FlyBatch's Pages site into one directory (SRS D-627, D-630).
#
# The page is hand-written in site/; its images are the repository's own
# docs/media and docs/diagrams files, copied in here rather than kept twice.
# Every local src= and href= in the page must exist in the output, or this
# exits 1, so a renamed image fails the deploy instead of breaking the page.
#
# usage:  bash site/build.sh <output directory>
set -eu
out=${1:?usage: bash site/build.sh <output directory>}
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")

rm -rf "$out"
mkdir -p "$out/media" "$out/diagrams"
cp "$here/index.html" "$here/style.css" "$out/"
for f in srext-network.png demo-linux.gif demo-windows.gif \
         mvs-report-g17.png mvs-3270-g17.png onfly-mvs-live.gif; do
    cp "$root/docs/media/$f" "$out/media/"
done
cp "$root"/docs/diagrams/*.svg "$out/diagrams/"
touch "$out/.nojekyll"

missing=0
for ref in $(grep -oE '(src|href)="[^"#:]+"' "$out/index.html" \
             | sed -E 's/^(src|href)="//; s/"$//' | sort -u); do
    if [ ! -e "$out/$ref" ]; then
        echo "site/build.sh: $ref is linked from index.html but not in $out"
        missing=1
    fi
done
[ "$missing" = 0 ] || exit 1
echo "site/build.sh: assembled $(find "$out" -type f | wc -l | tr -d ' ') files" \
     "into $out; every local link resolves"
