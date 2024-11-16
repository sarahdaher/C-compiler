from generator import *
from type.definitions import *


def grow_acc(env, growth):
    scope = env["scopes"][-1]
    scope["_acc"] -= growth
    return scope["_acc"]


def get_acc(env):
    return env["scopes"][-1]["_acc"]


def add_offset(offset):
    if offset != 0:
        sub(POINTER, REG_SP, cst(16 - offset))


def remove_offset(offset):
    if offset != 0:
        add(POINTER, REG_SP, cst(16 - offset))


def raise_error(message, term):
    print(
        "{} at line {}, column {}".format(
            message, term["start_line"], term["start_char"]
        )
    )
    exit(16)


def get_var_pointer(name, env, term):
    for i in range(len(env["scopes"]) - 1, -1, -1):
        scope = env["scopes"][i]
        if name in scope:
            return address(REG_BP, scope[name])

    if name in env["global_vars"]:
        return label_address(name)

    raise_error("Internal error: Variable {} not found".format(name), term)


def grow_offset(env, size):
    scope = env["scopes"][-1]
    scope["_offset"] = (scope["_offset"] + size) % 16


def get_offset(env):
    scope = env["scopes"][-1]
    return scope["_offset"]
