# tadds-rpyc-extractor

A small, dependency-free Python tool that reads compiled Ren'Py
`.rpyc` script files and pulls out the readable dialogue — without
needing the `renpy` package installed or network access to fetch
`unrpyc`. Built and tested against **TADDS** (a Ren'Py fangame), but
the core parser (`rpyc_dump.py`) works on any Ren'Py 6/7-era `.rpyc`
file, since it targets the documented `RENPY RPC2` container format
directly.

## How it works

Ren'Py's `.rpyc` files are a `RENPY RPC2`-tagged container: a short
header of `(slot, offset, length)` records, followed by zlib-compressed
pickled data. Slot 1 holds a pickled `(metadata, statement_list)` tuple
— the compiled Abstract Syntax Tree (AST) of the script.

Normally you'd need Ren'Py's own `renpy.ast` module installed to
unpickle that (the pickled objects reference classes like
`renpy.ast.Say`, `renpy.ast.Menu`, etc.). This tool sidesteps that by
installing a custom `Unpickler.find_class` that fabricates a generic
`Stub` class for *any* `renpy.*` class it's asked for, capturing
whatever state gets set via `__setstate__` into a plain `__dict__`.
The result is a tree of `Stub` objects you can walk with normal
Python — no engine required.

`extract_dialogue.py` walks that tree looking for `Say` and `Menu`
nodes and prints them as a readable transcript.

## Files

| File | Purpose |
|---|---|
| `rpyc_dump.py` | Core `.rpyc` parser: reads the RPC2 container, decompresses/unpickles slot 1, returns `(metadata, statements)` |
| `extract_dialogue.py` | Walks the parsed AST and prints `Say`/`Menu` dialogue as plain text |

## Usage

```bash
python3 extract_dialogue.py path/to/script.rpyc > transcript.txt
```

Or use `rpyc_dump.py` directly for custom analysis:

```python
from rpyc_dump import load, Stub

meta, stmts = load("script.rpyc")
print(meta)   # {'version': ..., 'key': ..., ...}

# walk the tree yourself, e.g. to find a specific node type:
def find(obj, qualname, out, seen=None):
    if seen is None: seen = set()
    if isinstance(obj, Stub):
        if id(obj) in seen: return
        seen.add(id(obj))
        if obj._qualname == qualname:
            out.append(obj)
        for v in vars(obj).values():
            find(v, qualname, out, seen)
    elif isinstance(obj, (list, tuple)):
        for i in obj: find(i, qualname, out, seen)
    elif isinstance(obj, dict):
        for v in obj.values(): find(v, qualname, out, seen)

labels = []
find(stmts, "renpy.ast.Label", labels)
print([vars(l).get("name") for l in labels])
```

## Output format

```
=== label some_label ===
character_name: Dialogue line text goes here.
-- MENU --
  * First choice text
  * Second choice text
```

## Known limitations

- Only reads slot 1 (the main statement list). Some `.rpyc` variants
  store additional data in slot 2; not currently extracted.
- `PyExpr` (Ren'Py's string-with-source-location type) is stubbed to
  behave like a plain `str` — line/file provenance is discarded.
- Ren'Py-internal mutable-tracking container types (`RevertableDict`,
  `RevertableList`, `RevertableSet`) are mapped to plain `dict`/`list`/
  `set` so pickle's `SETITEMS`/`APPEND` opcodes work — this loses the
  revert-on-rollback behavior, which doesn't matter for static analysis.
- Circular references (common in Ren'Py ASTs — e.g. parent pointers)
  are handled via an `id()`-based `seen` set during traversal.
- Screen-language (`SL2`) content — `screen` statements, ATL animation
  blocks — isn't dialogue and isn't extracted by `extract_dialogue.py`,
  though `rpyc_dump.py` will happily parse it if you write your own
  walker (see `renpy.sl2.slast.*` and `renpy.atl.*` qualnames).

## A note on copyright

This tool just reads a file format — what you do with its output is
on you. Only run it against files you have the right to inspect (your
own projects, fan content you're modding, games whose license permits
it, etc.), and don't redistribute another creator's full script text
without permission.

## License

MIT.

## NOTE: Will put game in folder. Coming soon...
