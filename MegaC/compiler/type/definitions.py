INT = {"type": "int"}
CHAR = {"type": "char"}
VOID = {"type": "void"}
POINTER = {"type": "pointer"}


def sizeof(t):
    if t == "void_pointer":
        return 8

    if type(t) != dict:
        return -1

    kind = t["type"]

    if kind == "int":
        return 4
    if kind == "char":
        return 1
    if kind in ["pointer", "tab"]:
        return 8
    if kind == "void":
        return 0

    return -1


def sizeof_tab(t):
    acc = 1

    while t["type"] == "tab":
        acc *= t["size"]
        t = t["sub_type"]

    acc *= sizeof(t)
    return acc
