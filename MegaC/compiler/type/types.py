import helper
from type.statement import check_statement
from type.definitions import INT, CHAR, VOID

global_vars = {}
functions = {
    "print_int": {"type": VOID, "args": ["int_or_char"]},
    "read_int": {"type": INT, "args": []},
    "malloc": {"type": "void_pointer", "args": [INT]},
    "printf": {"type": VOID, "args": [{"type": "pointer", "sub_type": CHAR}, "all"]},
    "scanf": {
        "type": VOID,
        "args": [{"type": "pointer", "sub_type": CHAR}, "void_pointer"],
    },
}
strings = []


def get_variable_type(scopes, term):
    name = term["name"]

    for i in range(len(scopes) - 1, -1, -1):
        scope = scopes[i]
        if name in scope:
            return scope[name]

    if name in global_vars:
        return global_vars[name]

    helper.raise_error("Variable {} does not exists".format(name), term)


def assert_same_type(term1, term2, term):
    if term1 == "all" or term2 == "all":
        return

    if term1 == "int_or_char":
        if term2 not in [INT, CHAR]:
            helper.raise_error("Incompatible types", term)
        return

    if term2 == "int_or_char":
        if term1 not in [INT, CHAR]:
            helper.raise_error("Incompatible types", term)
        return

    if term1 == "void_pointer":
        if term2["type"] not in ["pointer", "tab"]:
            helper.raise_error("Incompatible types", term)
        return

    if term2 == "void_pointer":
        if term1["type"] not in ["pointer", "tab"]:
            helper.raise_error("Incompatible types", term)
        return

    if (term2["type"] == "tab" and term1["type"] == "pointer") or (
        term1["type"] == "tab" and term2["type"] == "pointer"
    ):
        assert_same_type(term1["sub_type"], term2["sub_type"], term)
        return

    if term1 != term2:
        helper.raise_error("Incompatible types", term)


def assert_number(term):
    if term["types"] not in [INT, CHAR]:
        helper.raise_error("Incompatible types", term)


def check_function(term):
    name = term["name"]

    if name in functions:
        helper.raise_error("Function {} already exists".format(name), term)

    function = {"type": term["type"], "args": []}
    functions[name] = function
    scope = {"_function": name}

    for arg in term["args"]:
        if arg["name"] in function["args"]:
            helper.raise_error("Another parameter has the same name", term)

        if arg["type"]["type"] == "void":
            helper.raise_error("A function parameter can't have type void", term)

        function["args"].append(arg["type"])
        scope[arg["name"]] = arg["type"]

    check_statement([scope], term["body"])


def check_types(term):
    for t in term:
        action = t["action"]

        if action == "def_var_global":
            if t["name"] in global_vars:
                helper.raise_error(
                    "Global variable {} already exists".format(t["name"]), t
                )

            global_vars[t["name"]] = t["type"]

        elif action == "def_fun":
            check_function(t)
