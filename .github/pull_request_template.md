## What this changes

<!-- One or two sentences. Link the issue or proposal it answers. -->

## Requirement IDs touched

<!-- FR-, IR-, NR-, SR-, ACC-, NFR- IDs, and any D- or VL-rows it relies on. -->

## Tests run

<!-- The exact commands, the closing `ONFLY test:` line, and the platform,
     compiler and version, and float backend they ran on. -->

## What this does not prove

<!-- For example: "run on x86-64 Linux gcc 13 only; not run under MinGW,
     on s390x or on MVS". -->

## Checklist

- [ ] Nothing under `third_party/` is edited, and nothing under `generated/`
      is edited by hand.
- [ ] `make test-nonet` (or `test`) passes with `ONFLY_NOSKIP=1`.
- [ ] A change to code, tests, the build, CI or a recorded result carries an
      implementation doc from `docs/implementations/_TEMPLATE.md`; a wording
      or link fix says here what was checked instead (SRS D-685).
- [ ] If AI tools helped with this change, it says so here, and I can
      explain every line (SRS D-686).
- [ ] I contribute this under the terms in `CONTRIBUTING.md`.
