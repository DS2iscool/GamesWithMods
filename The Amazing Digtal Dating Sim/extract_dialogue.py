import sys, os
sys.path.insert(0, '/home/claude/rpa_work')
from rpyc_dump import load, Stub

def pyexpr_str(v):
    return str(v) if v is not None else None

def walk(obj, lines, label_stack, seen=None):
    if seen is None:
        seen = set()
    if isinstance(obj, Stub):
        oid = id(obj)
        if oid in seen:
            return
        seen.add(oid)
        q = obj._qualname
        d = vars(obj)
        if q == "renpy.ast.Label":
            name = d.get("name")
            lines.append(f"\n=== label {name} ===")
        elif q == "renpy.ast.Say":
            who = d.get("who")
            what = d.get("what")
            attrs = d.get("attributes")
            who_str = pyexpr_str(who) if who else ""
            if attrs:
                who_str += f" [{' '.join(str(a) for a in attrs)}]"
            lines.append(f"{who_str}: {pyexpr_str(what)}")
        elif q == "renpy.ast.Menu":
            items = d.get("items", [])
            lines.append("-- MENU --")
            for it in items:
                # items are tuples: (caption, condition, block) roughly
                if isinstance(it, (list, tuple)) and len(it) >= 1:
                    cap = it[0]
                    lines.append(f"  * {pyexpr_str(cap)}")
                    if len(it) >= 3:
                        walk(it[2], lines, label_stack, seen)
        # recurse into all attributes regardless
        for k, v in d.items():
            if k.startswith("_"):
                continue
            if k in ("who", "what", "attributes") and q == "renpy.ast.Say":
                continue
            if k == "items" and q == "renpy.ast.Menu":
                continue
            walk(v, lines, label_stack, seen)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            walk(item, lines, label_stack, seen)
    elif isinstance(obj, dict):
        for v in obj.values():
            walk(v, lines, label_stack, seen)

def extract(path):
    result = load(path)
    if result is None:
        return None
    meta, stmts = result
    lines = []
    walk(stmts, lines, [])
    return "\n".join(lines)

if __name__ == "__main__":
    src = sys.argv[1]
    out = extract(src)
    print(out)
