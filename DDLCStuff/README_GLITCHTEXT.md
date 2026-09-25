# glitchtext-hell
 
A tiny, dependency-free Python toolkit for generating "corrupted" text —
inspired by the `glitchtext()` function found in *Doki Doki Literature
Club*'s engine code, escalated with [Zalgo text](https://en.wikipedia.org/wiki/Combining_character)
(stacked Unicode combining marks) for maximum chaos.
 
```
--- FULL HELL ---
ť̯̣̒̇̈̍̆̍£̧͉͙̃͒e̯̯̮̊̎̒̓̅͏̾ǫ̸̯̞̯͇̮͚̼͎̪̫̂̃̏̇̑̔͒͞͞ͅż̮͕͍̋̍́̉̎̎̋̐̈́̿͘͘͞ͅͅę̦...
```
 
## Features
 
- **`glitchtext(length)`** — the original algorithm: picks `length`
  random characters from a fixed pool of accented Latin-1 /
  Latin Extended-A characters. No source text needed.
- **`zalgo(text, intensity)`** — wraps every character of real text in
  randomly stacked combining marks (above, through, and below the line).
- **`hellglitch(text, corruption, intensity)`** — the full combo: first
  randomly swaps some letters for glitch-pool noise, then zalgos the
  result.
- **`demon_scream(length, intensity)`** — pure noise, no input text,
  maximum stacking.
- **Interactive menu** — run the script directly and type your own
  text in, no code editing required.
No external dependencies — just the Python standard library (`random`).
 
## Installation
 
Three ways to run it, pick whichever fits:
 
### Option A — Just run the `.exe` (Windows, no setup)
 
A pre-built `glitchtext_hell.exe` is included right in this repo — no
Python required. Download/clone the repo and double-click
`glitchtext_hell.exe`. That's it.
 
### Option B — Run the Python file directly (any OS)
 
Requires Python 3, nothing else.
 
```bash
git clone https://github.com/yourusername/glitchtext-hell.git
cd glitchtext-hell
python3 glitchtext_hell.py
```
 
**Windows, out of the box:** double-click `run_glitchtext.bat` — it
finds and runs `glitchtext_hell.py` for you, no terminal typing needed
(requires Python 3 installed and on your `PATH`).
 
**macOS/Linux, out of the box:** the script starts with a
`#!/usr/bin/env python3` shebang, so after cloning you can do:
 
```bash
chmod +x glitchtext_hell.py
./glitchtext_hell.py
```
 
and it runs directly without typing `python3` first.
 
### Option C — Rebuild the `.exe` yourself
 
If you change the source and want to regenerate `glitchtext_hell.exe`:
 
1. Make sure Python 3 is installed.
2. Double-click `build_exe.bat` in this repo.
3. It installs [PyInstaller](https://pyinstaller.org/) and compiles
   the script into `dist\glitchtext_hell.exe` — copy that over the
   one in the repo root to update it.
`build_exe.bat` just runs these two commands, if you'd rather do it
by hand:
 
```bat
python -m pip install --upgrade pyinstaller
python -m PyInstaller --onefile --console --name glitchtext_hell glitchtext_hell.py
```
 
### Option D — Import it as a module
 
See [Usage](#usage) below — works the same regardless of how you got
the file onto your machine.
 
## Usage
 
Running the script directly (`python3 glitchtext_hell.py`, the `.bat`,
or the built `.exe`) drops you into an interactive menu:
 
```
==================================================
   GLITCHTEXT HELL
==================================================
1) glitchtext   - random noise, no input text
2) zalgo        - stack combining marks on YOUR text
3) hellglitch   - corrupt + zalgo YOUR text (full hell)
4) demon_scream - pure noise, maximally stacked
5) quit
 
Pick a mode (1-5): 3
Text to send to hell: everything is fine
Corruption 0.0-1.0 (try 0.3-0.9) [0.5]: 0.85
Intensity (try 4-16) [10]: 16
 
ť̯̣̒̇̈̍̆̍£̧͉͙̃͒e̯̯̮̊̎̒̓̅͏̾ǫ̸̯̞̯͇̮͚̼͎̪̫̂̃̏̇̑̔͒͞͞ͅż̮͕͍̋̍́̉̎̎̋̐̈́̿͘͘͞ͅͅę̦...
 
Go again? (Y/n):
```
 
Just press Enter at any prompt to accept the shown default. It loops
until you choose "quit" or answer "n" to "Go again?".
 
You can also skip the menu entirely and call the functions from your
own code:
 
```python
from glitchtext_hell import glitchtext, zalgo, hellglitch, demon_scream
 
glitchtext(20)
# ûŽÚòÆĉÖ¾ŐçĀÎľěŦŉµÆßśĽŃù
 
zalgo("just a normal sentence", intensity=6)
# j̖̲͏̺ü̊s̈̊̋̏̈ṱ̮̱̮̑̉̄̑̒̅͛ ̟̝͔͚͗͂͊͌a̛̗̐̉̋...
 
hellglitch("everything is fine", corruption=0.85, intensity=16)
# nearly unreadable — high corruption + heavy zalgo stacking
 
demon_scream(length=25, intensity=18)
# pure noise, no source text at all
```
 
## API
 
| Function | Args | Description |
|---|---|---|
| `glitchtext(length)` | `length: int` | Random glitch-pool string of given length |
| `zalgo(text, intensity=8)` | `text: str`, `intensity: int` | Stacks combining marks on each character of `text` |
| `hellglitch(text, corruption=0.5, intensity=10)` | `text: str`, `corruption: float (0–1)`, `intensity: int` | Corrupts a fraction of characters, then zalgos the result |
| `demon_scream(length=40, intensity=14)` | `length: int`, `intensity: int` | Pure noise + zalgo, no input text |
 
`intensity` roughly controls how many combining marks pile onto each
character — keep it under ~10 for something still legible, push past
15 for something that breaks most renderers' line height.
 
## Files
 
| File | Purpose |
|---|---|
| `glitchtext_hell.py` | The tool itself — functions + interactive menu |
| `glitchtext_hell.exe` | Pre-built standalone Windows executable — no Python needed |
| `run_glitchtext.bat` | Windows double-click launcher (runs via installed Python) |
| `build_exe.bat` | Windows double-click builder — regenerates `dist\glitchtext_hell.exe` |
 
## Notes
 
- Zalgo text can visually break terminals, chat clients, and some
  fonts/renderers — that's the point, but be considerate about where
  you paste heavily-stacked output.
- This is a fun/cosmetic text-effect toy, not intended for anything
  beyond that.
## Credit
 
The base `glitchtext()` concept is a reimplementation of a simple
effect used in Doki Doki Literature Club's Ren'Py source — this repo
just extends the idea; it doesn't include or redistribute any of that
game's original code or assets.
 
## License
 
MIT — do whatever you want with it.
 
