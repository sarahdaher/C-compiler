import helper
from generator import *
from type.definitions import *

ARG_REGS = [
    REG_A,
    REG_B,
    REG_C,
    REG_D,
    REG_SI,
    REG_DI,
    REG_8,
    REG_9,
    REG_10,
    REG_11,
    REG_12,
    REG_13,
    REG_14,
    REG_15,
]
NB_REGS = len(ARG_REGS)


def _push(env, t, val):
    size = sizeof(t)
    if size == 4:
        size = 8
    if size == 1:
        size = 2

    helper.grow_offset(env, size)
    push(t, val)


def _pop(env, t, val):
    size = sizeof(t)
    if size == 4:
        size = 8
    if size == 1:
        size = 2

    helper.grow_offset(env, -size)
    pop(t, val)


def new_label(env):
    label = "{}_{}".format(env["name"], env["label"])
    env["label"] += 1
    return label


def get_real_function_name(name):
    if name == "malloc":
        return "_malloc"
    if name == "printf":
        return "_printf"
    if name == "scanf":
        return "_scanf"
    if name == "scanf":
        return "_scanf"
    return name


def compile_call(name, args, env):
    # Calcul de la place que l'on doit allouer pour les arguments qui sont
    # stockés dans la pile (de l'argument numéro NB_REGS+1 à n)
    range_on_stack = 0
    for arg in args[NB_REGS:]:
        range_on_stack += sizeof(arg["types"])

    # On doit ajouter l'offset après avoir ajouté la place pour les arguments
    sub_to_rsp = range_on_stack
    helper.grow_offset(env, range_on_stack)

    # Si l'offset à ajouter est nul, on ne fait rien
    if helper.get_offset(env) != 0:
        sub_to_rsp += 16 - helper.get_offset(env)

    # On soustrait l'offset de rsp
    sub(POINTER, REG_SP, cst(sub_to_rsp))

    # On ajoute d'abord les arguments de NB_REGS+1 à n. Pour cela on commence à
    # %rsp+range_on_stack puis on descend
    pos = range_on_stack
    nb_args = len(args)

    for arg in args[NB_REGS:]:
        compile(arg, env)
        # On descend le pointeur vers le prochain argument
        pos -= sizeof(arg["types"])
        _pop(env, arg["types"], REG_A)
        mov(arg["types"], REG_A, address(REG_SP, pos))

    # On compile tous les arguments de 1 à NB_REGS pour ne pas avoir des
    # conflits avec les registres
    for arg in args[:NB_REGS]:
        compile(arg, env)

    # Ensuite, on les met dans les registres
    for i in range(min(NB_REGS, nb_args) - 1, -1, -1):
        arg = args[i]
        _pop(env, arg["types"], ARG_REGS[i])

    call(get_real_function_name(name))

    # On ajoute la plage pour les arguments + l'offset à %rsp
    add(POINTER, REG_SP, cst(sub_to_rsp))

    # On actualise l'offset dans l'environnment
    helper.grow_offset(env, -range_on_stack)


def compile_left_value(env, term):
    type = term["type"]

    if type == "variable":
        var_pointer = helper.get_var_pointer(term["name"], env, term)
        lea(var_pointer, REG_A)

    elif type == "dereference":
        compile(term["address"], env)
        _pop(env, term["address"]["types"], REG_A)


BINOP = [
    "add",
    "sub",
    "mul",
    "div",
    "mod",
    "equal",
    "non_equal",
    "less",
    "less_equal",
    "greater",
    "greater_equal",
]


def compile(term, env):
    type = term["type"]
    types = term["types"]

    if type == "integer":
        _push(env, types, cst(term["value"]))

    elif type == "char":
        _push(env, types, cst(ord(term["value"])))

    elif type == "val":
        env["tab"] = False
        env["val_depth"] += 1
        compile_left_value(env, term["left_value"])
        env["val_depth"] -= 1

        if types["type"] == "tab" and env["tab"] and env["val_depth"] > 0:
            _push(env, term["types"], REG_A)
        else:
            _push(env, term["types"], address(REG_A, 0))
            env["tab"] = True

    elif type == "call":
        compile_call(term["name"], term["args"], env)
        _push(env, types, REG_A)

    elif type in BINOP:
        compile(term["left"], env)
        compile(term["right"], env)

        if type == "add":
            _pop(env, types, REG_A)
            _pop(env, types, REG_B)
            add(types, REG_B, REG_A)
            _push(env, types, REG_B)

        elif type == "sub":
            _pop(env, types, REG_A)
            _pop(env, types, REG_B)
            sub(types, REG_B, REG_A)
            _push(env, types, REG_B)

        elif type == "mul":
            _pop(env, types, REG_A)
            _pop(env, types, REG_B)
            mul(types, REG_B)
            _push(env, types, REG_A)

        elif type == "div":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            div(types, REG_B)
            _push(env, types, REG_A)

        elif type == "mod":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            div(types, REG_B)
            _push(env, types, REG_D)

        elif type == "equal":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_A, REG_B)
            mov(types, cst(1), REG_A)
            cmov(types, "e", REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "ne", REG_A, REG_B)
            _push(env, types, REG_B)

        elif type == "non_equal":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "e", REG_A, REG_B)
            mov(types, cst(1), REG_A)
            cmov(types, "ne", REG_A, REG_B)
            _push(env, types, REG_B)

        elif type == "less":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_B, REG_A)
            mov(types, cst(1), REG_A)
            cmov(types, "l", REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "nl", REG_A, REG_B)
            _push(env, types, REG_B)

        elif type == "less_equal":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_B, REG_A)
            mov(types, cst(1), REG_A)
            cmov(types, "le", REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "nle", REG_A, REG_B)
            _push(env, types, REG_B)

        elif type == "greater":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_B, REG_A)
            mov(types, cst(1), REG_A)
            cmov(types, "g", REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "ng", REG_A, REG_B)
            _push(env, types, REG_B)

        elif type == "greater_equal":
            _pop(env, types, REG_B)
            _pop(env, types, REG_A)
            cmp(types, REG_B, REG_A)
            mov(types, cst(1), REG_A)
            cmov(types, "ge", REG_A, REG_B)
            mov(types, cst(0), REG_A)
            cmov(types, "nge", REG_A, REG_B)
            _push(env, types, REG_B)

    elif type == "and":
        compile(term["left"], env)
        _pop(env, types, REG_A)
        cmp(types, cst(0), REG_A)
        zero = new_label(env)
        cjump("z", zero)

        # Test de l'expression de droite
        compile(term["right"], env)
        _pop(env, types, REG_A)
        cmp(types, cst(0), REG_A)
        cjump("z", zero)

        # Expression vraie
        mov(types, cst(1), REG_B)
        end = new_label(env)
        jump(end)

        # Expression fausse
        label(zero)
        mov(types, cst(0), REG_B)

        # Fin
        label(end)
        _push(env, types, REG_B)

    elif type == "or":
        compile(term["left"], env)
        _pop(env, types, REG_A)
        cmp(types, cst(0), REG_A)
        one = new_label(env)
        cjump("nz", one)

        # Test de l'expression de droite
        compile(term["right"], env)
        _pop(env, types, REG_A)
        cmp(types, cst(0), REG_A)
        cjump("nz", one)

        # Expression fausse
        mov(types, cst(0), REG_B)
        end = new_label(env)
        jump(end)

        # Expression fausse
        label(one)
        mov(types, cst(1), REG_B)

        # Fin
        label(end)
        _push(env, types, REG_B)

    elif type == "not":
        compile(term["value"], env)
        _pop(env, types, REG_A)
        mov(types, cst(0), REG_B)
        mov(types, cst(1), REG_D)
        cmp(types, cst(0), REG_A)
        cmov(types, "z", REG_D, REG_A)
        cmov(types, "nz", REG_B, REG_A)
        _push(env, types, REG_A)

    elif type == "reference":
        left_value = term["left_value"]

        if left_value["type"] == "variable":
            var_pointer = helper.get_var_pointer(term["left_value"]["name"], env, term)
            lea(var_pointer, REG_A)
            _push(env, POINTER, REG_A)
        elif left_value["type"] == "dereference":
            compile(term["left_value"]["address"], env)

    elif type == "sizeof":
        _push(env, INT, cst(sizeof_tab(term["typee"])))

    elif type == "convert_to_pointer":
        compile(term["value"], env)
        _pop(env, term["value"]["types"], REG_A)
        movsx(term["value"]["types"], REG_A, POINTER, REG_A)
        _push(env, POINTER, REG_A)

    elif type == "convert_to_int":
        compile(term["value"], env)
        _pop(env, term["value"]["types"], REG_A)
        movsx(term["value"]["types"], REG_A, INT, REG_A)
        _push(env, POINTER, REG_A)

    elif type == "string":
        lea(label_address("_S{}".format(term["value"])), REG_A)
        _push(env, POINTER, REG_A)

    elif type == "tab":
        for elem in reversed(term["elements"]):
            compile(elem, env)
