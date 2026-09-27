# FlyBatch terminal demonstration recorded with VHS (SRS D-631, D-643).
# Run from the repository root on Windows, after `mingw32-make eng` with
# `srext` staged, and with vhs, ttyd and ffmpeg on PATH:
#     vhs tools/demo/demo.tape
# It runs the same tools/demo/demo.sh as the asciinema recording, so the two
# differ only in the recorder and the platform (here MinGW gcc 6.3.0).
# VHS starts PowerShell, not bash: Windows resolves a bare "bash" to WSL's
# launcher in System32 before any PATH entry (found in D-631's trial), so
# PowerShell calls Git's bash.exe by its full path.
Output "docs/media/demo-windows.gif"
Set Shell "pwsh"
Set FontSize 18
Set Width 1150
Set Height 780
Set Padding 18
Set Theme "Monokai Vivid"
Set TypingSpeed 20ms
Hide
Sleep 4s
Type "& 'C:\Program Files\Git\bin\bash.exe' -c 'PY=python bash tools/demo/demo.sh'"
Enter
Sleep 500ms
Show
Sleep 62s
