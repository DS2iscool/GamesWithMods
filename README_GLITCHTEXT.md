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

No external dependencies — just the Python standard library (`random`).

## Installation

Nothing to install — just Python 3 (standard library only, no `pip`
packages needed).

```bash
git clone https://github.com/yourusername/glitchtext-hell.git
cd glitchtext-hell
python3 glitchtext_hell.py
```

**Windows, out of the box:** double-click `run_glitchtext.bat` — it
finds and runs `glitchtext_hell.py` for you and keeps the console
window open afterward so you can read the output (requires Python 3
installed and on your `PATH`).

**macOS/Linux, out of the box:** the script starts with a
`#!/usr/bin/env python3` shebang, so after cloning you can do:

```bash
chmod +x glitchtext_hell.py
./glitchtext_hell.py
```

and it runs directly without typing `python3` first.

## Usage

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

Running the file directly (`python3 glitchtext_hell.py`) prints a demo
of all four functions.

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
