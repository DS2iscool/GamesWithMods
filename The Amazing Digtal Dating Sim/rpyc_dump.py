import struct, zlib, pickle, sys, io

def read_slot(path, slot=1):
    with open(path, 'rb') as f:
        header = f.read(10)
        assert header == b"RENPY RPC2", header
        while True:
            s = struct.unpack("III", f.read(12))
            if s[0] == slot:
                f.seek(s[1])
                data = f.read(s[2])
                return zlib.decompress(data)
            if s[0] == 0:
                return None

class Stub:
    """Generic stand-in for any renpy.* class encountered during unpickling."""
    def __init__(self, qualname):
        self._qualname = qualname
    def __setstate__(self, state):
        if isinstance(state, dict):
            self.__dict__.update(state)
        elif isinstance(state, tuple) and len(state) == 2:
            d, extra = state
            if isinstance(d, dict):
                self.__dict__.update(d)
            if isinstance(extra, dict):
                self.__dict__.update(extra)
            else:
                self._extra = extra
        else:
            self._raw_state = state
    def __repr__(self):
        return f"<{self._qualname}>"

class FakeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        qualname = f"{module}.{name}"
        # PyExpr behaves like str
        if name == "PyExpr":
            class PyExprStub(str):
                def __new__(cls, s, *args, **kwargs):
                    return str.__new__(cls, s)
                def __setstate__(self, state):
                    pass
            return PyExprStub
        if name in ("Sentinel",):
            return Stub
        if name in ("RevertableDict", "RollbackDict"):
            return dict
        if name in ("RevertableList", "RollbackList"):
            return list
        if name in ("RevertableSet", "RollbackSet"):
            return set
        if name in ("RevertableObject",):
            return Stub
        if qualname not in _class_cache:
            def __new__(cls, *args, **kwargs):
                obj = object.__new__(cls)
                obj._qualname = qualname
                obj._init_args = args
                return obj
            def __init__(self, *args, **kwargs):
                pass
            cls = type(name, (Stub,), {"__new__": __new__, "__init__": __init__})
            _class_cache[qualname] = cls
        return _class_cache[qualname]

_class_cache = {}

def load(path):
    data = read_slot(path, 1)
    if data is None:
        return None
    return FakeUnpickler(io.BytesIO(data)).load()

if __name__ == "__main__":
    result = load(sys.argv[1])
    print(type(result))
    print(result)
