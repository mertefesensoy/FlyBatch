#!/usr/bin/env bash
# FlyBatch terminal demonstration (SRS D-628, D-631, D-643): one golden
# request, G-16, on the shipped network, through three floating-point builds
# of the engine.  Every line of output is the real output of the command
# shown; nothing is typed into the recording that the shell does not run.
#
# Run from the repository root, after `make eng` and with `srext` staged:
#     PY=python3 bash tools/demo/demo.sh
# `make demo-linux` records it with asciinema and draws it with agg;
# `mingw32-make demo-windows` records it with VHS (tools/demo/demo.tape).
PY=${PY:-python3}
NETF=data/networks/onfnet-malecns-v1.0-srext.bin
mkdir -p build/demo
printf 'SUGR 0040 1000 000000001\n' > build/demo/g16.cards

say() {
    printf '\033[1;32m$\033[0m '
    s="$1"
    for ((i = 0; i < ${#s}; i++)); do printf '%s' "${s:i:1}"; sleep 0.025; done
    printf '\n'
    sleep 0.4
}
run() { say "$1"; eval "$1"; sleep 1.6; }
note() { printf '\033[2m# %s\033[0m\n' "$1"; sleep 1.2; }

clear
note "FlyBatch: one golden request, three floating-point builds"
run "cat build/demo/g16.cards"
note "sugar at 40 Hz for 1000 ms, seed 1: golden request G-16"
run "$PY tools/mkreq.py build/demo/g16.cards build/demo/g16.req"
run "./build/onflyeng_nat.exe RUN $NETF build/demo/g16.req build/demo/g16.rsp"
note "the same request with IEEE 754 done in software"
run "./build/onflyeng_soft.exe RUN $NETF build/demo/g16.req build/demo/g16.rsp | grep -E 'BACKEND|FP='"
run "./build/onflyeng_2c.exe RUN $NETF build/demo/g16.req build/demo/g16.rsp | grep -E 'BACKEND|FP='"
note "the fingerprint the specification records for G-16"
run "grep -o 'G-16 .BAF81D91.' docs/ONFLY-SRS.md | head -1"
sleep 2
