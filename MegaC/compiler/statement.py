from generator import *
import expression
from expression import new_label
import helper
import itertools


# faire tous les combinaisons possibles : exemple : [2,3] -> [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
def generate_combinations(lst):
    ranges = [range(x) for x in lst]
    combinations = list(itertools.product(*ranges))
    return combinations


def get_element_address(tup, size, pointer, tab_size, dim_list):
    dim_nb = len(dim_list)
    pos = pointer - tab_size
    tup = list(tup)

    for i in range(dim_nb - 1):
        subtab_size = size

        for j in range(i + 1, dim_nb):
            subtab_size *= dim_list[j]

        pos += tup[i] * subtab_size

    pos += size * tup[dim_nb - 1]
    return pos


def compile_while(term, env):
    label_start = new_label(env)
    label_end = new_label(env)
    scope = env["scopes"][-1]
    env["loop_starts"].append([label_start, scope])
    env["loop_ends"].append(label_end)

    label(label_start)
    expression.compile(term["condition"], env)
    expression._pop(env, term["condition"]["types"], REG_A)
    cmp(term["condition"]["types"], cst(0), REG_A)
    cjump("z", label_end)
    compile(term["body"], env)
    jump(label_start)
    label(label_end)

    env["loop_starts"].pop()
    env["loop_ends"].pop()


def compile_if_else(term, env):
    expression.compile(term["condition"], env)
    expression._pop(env, term["condition"]["types"], REG_A)
    cmp(term["condition"]["types"], cst(0), REG_A)

    label_else = new_label(env)
    label_endif = new_label(env)

    cjump("z", label_else)
    compile(term["then_body"], env)
    jump(label_endif)
    label(label_else)
    compile(term["else_body"], env)
    label(label_endif)


def get_left_value_name(left_value):
    while left_value["type"] == "dereference":
        left_value = left_value["left_value"]
    return left_value["name"]


def set_variable(term, env):
    expression.compile(term["value"], env)
    env["val_depth"] = 1
    expression.compile_left_value(env, term["left_value"])
    env["val_depth"] = 0
    expression._pop(env, term["value"]["types"], REG_B)
    mov(term["value"]["types"], REG_B, address(REG_A, 0))


def declare_new_variable(env, name, t):
    size = sizeof(t)
    acc = helper.grow_acc(env, size)
    env["scopes"][-1][name] = acc
    helper.grow_offset(env, size)
    sub(POINTER, REG_SP, cst(size))

    if t["type"] == "tab":
        tab_size = sizeof_tab(t)
        helper.grow_offset(env, tab_size)
        new_acc = helper.grow_acc(env, tab_size)
        sub(POINTER, REG_SP, cst(tab_size))
        lea(address(REG_BP, new_acc), REG_A)
        mov(POINTER, REG_A, address(REG_BP, acc))

    return acc


def get_dimensions(types):
    res = []
    while types["type"] == "tab":
        res.append(types["size"])
        types = types["sub_type"]
    return res, types


def compile(term, env):
    comment("Ligne {}".format(term["start_line"]))
    action = term["action"]

    if action == "def_var_local_set":
        pointer = declare_new_variable(env, term["name"], term["type"])

        if term["value"]["type"] == "tab":
            dim_list, root_type = get_dimensions(term["type"])
            size = sizeof(root_type)
            expression.compile(term["value"], env)
            comb = generate_combinations(dim_list)
            tab_size = sizeof_tab(term["type"])

            for tup in comb:
                pos = get_element_address(list(tup), size, pointer, tab_size, dim_list)
                expression._pop(env, root_type, REG_A)
                mov(root_type, REG_A, address(REG_BP, pos))
        else:
            expression.compile(term["value"], env)
            expression._pop(env, term["type"], REG_A)
            mov(term["type"], REG_A, address(REG_BP, pointer))

    elif action == "def_var_local":
        declare_new_variable(env, term["name"], term["type"])

    elif action == "var_set":
        set_variable(term, env)

    elif action == "return":
        if "value" in term:
            expression.compile(term["value"], env)
            expression._pop(env, term["value"]["types"], REG_A)
        leave()
        ret()

    elif action == "call":
        expression.compile_call(term["name"], term["args"], env)

    elif action == "if_else":
        compile_if_else(term, env)

    elif action == "block":
        last_scope = env["scopes"][-1]
        new_scope = {"_acc": last_scope["_acc"], "_offset": last_scope["_offset"]}
        env["scopes"].append(new_scope)

        for s in term["statements"]:
            compile(s, env)

        add(POINTER, REG_SP, cst(last_scope["_acc"] - new_scope["_acc"]))
        env["scopes"].pop()

    elif action == "while":
        compile_while(term, env)

    elif action == "break":
        [_, loop_scope] = env["loop_starts"][-1]
        end = env["loop_ends"][-1]
        current_scope = env["scopes"][-1]
        add(POINTER, REG_SP, cst(loop_scope["_acc"] - current_scope["_acc"]))
        jump(end)

    elif action == "continue":
        [label, loop_scope] = env["loop_starts"][-1]
        current_scope = env["scopes"][-1]
        add(POINTER, REG_SP, cst(loop_scope["_acc"] - current_scope["_acc"]))
        jump(label)
