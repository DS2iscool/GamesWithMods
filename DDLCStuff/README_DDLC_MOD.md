# ddlc-qol-mod

An unofficial, loose-`.rpy` quality-of-life / cheat mod for
**Doki Doki Literature Club** (tested against v1.1.1), built entirely
by reverse-engineering the shipped `.rpa`/`.rpyc` files — no source
leak, no repacking required.

## What it does

- **Shift+M** opens an in-game cheat panel:
  - Max out each character's affection/poem-appeal trackers
    (`n_appeal`, `s_appeal`, `y_appeal`, `m_appeal`, and their
    `*_poemappeal` counterparts)
  - Mark all poems as read/delivered
  - Toggle the game's `persistent.anticheat` flag
  - Print every label in the loaded script to the console (so you can
    `renpy.jump()` anywhere by name, without guessing)
- **Shift+O** — forces Ren'Py's built-in dev console on, regardless of
  the game's shipped `developer` define
- **Shift+D** — Ren'Py's built-in dev menu (also force-enabled)
- **Custom music swap** — drop `.ogg` files into a `bgm_custom/`
  folder, named to match the game's internal track keys (`t1`, `t6`,
  `m1`, etc.), and the mod reroutes the corresponding track to your
  file automatically. No music is bundled — you supply your own.

## Installation

1. Copy `zzz_mods.rpy` into your DDLC install's `game/` folder, next
   to `script.rpyc`:
   ```
   DDLC-1.1.1-pc/game/zzz_mods.rpy
   ```
2. Launch the game normally. Ren'Py auto-compiles loose `.rpy` files
   on startup — no repacking of `scripts.rpa` needed, and nothing in
   the original archive is modified.
3. In-game, press **Shift+M** for the cheat panel or **Shift+O** for
   the console.

## How it was built

The mod was developed by unpacking `scripts.rpa` (Ren'Py's `RPA-3.0`
archive format — a header line with a hex index offset + XOR key,
followed by a zlib+pickle index) and decompiling the non-narrative
`.rpyc` files (`definitions.rpyc`, `cgs.rpyc`, etc.) to find the real
variable names Ren'Py uses internally — `n_appeal`, `poemsread`,
`persistent.playthrough`, and so on — rather than guessing at them.

## Intentional omissions

Two things were left out on purpose:

1. **No gallery-unlock cheat for `persistent.yuri_kill`.** That
   variable specifically gates the game's graphic self-harm CG
   sequence (confirmed via `cgs.rpyc`'s image-unlock thresholds). This
   mod does not touch it, and won't add a one-click unlock for it.
2. **No bundled music.** The swap mechanism is real and functional,
   but no actual audio files are included — only use tracks you have
   the rights to.

## Files

| File | Purpose |
|---|---|
| `zzz_mods.rpy` | The mod itself — drop into `game/` |

## Notes on `persistent.anticheat`

Investigated out of curiosity: the game sets this to a random 6-digit
number at four story checkpoints (`persistent.anticheat =
renpy.random.randint(100000, 999999)`) and reads it into a local
variable, but — across every script file checked — it's never actually
compared against anything or used to branch on. Functionally inert as
far as static analysis can tell. The mod's toggle button is included
mostly as a curiosity, not a real cheat.

## Disclaimer

This is a fan-made, unofficial modification for personal/offline use
with a copy of the game you own. It doesn't modify, repack, or
redistribute any of Team Salvato's original files — it's a
standalone `.rpy` file that runs alongside them.

## License

MIT, for this mod file. DDLC itself is © Team Salvato, all rights
reserved — this repo does not include or redistribute any of their
assets or script content.
