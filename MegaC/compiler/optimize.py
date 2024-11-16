from type.definitions import INT, CHAR, sizeof
from math import floor, ceil


def check_both_side_are_constant(term):
    left = term["left"]
    right = term["right"]
    optimize_exp(left)
    optimize_exp(right)

    if left["type"] == "integer" and right["type"] == "integer":
        return True

    if left["type"] == "char" and right["type"] == "char":
        return True

    return False


def constant_term(term, value):
    types = term["types"]

    if types == INT:
        term["type"] = "integer"
    elif types == CHAR:
        term["type"] = "char"

    if value == True:
        value = 1
    elif value == False:
        value = 0

    term["value"] = value


def optimize_left_value(term):
    type = term["type"]

    if type == "dereference":
        optimize_exp(term["address"])


def optimize_exp(term):
    type = term["type"]

    if type == "add" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] + term["right"]["value"])

    elif type == "sub" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] - term["right"]["value"])

    elif type == "mul" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] * term["right"]["value"])

    elif type == "div" and check_both_side_are_constant(term):
        left = term["left"]["value"]
        right = term["right"]["value"]
        v = left / right
        if v >= 0:
            v = floor(v)
        else:
            v = ceil(v)
        constant_term(term, v)

    elif type == "mod" and check_both_side_are_constant(term):
        left = term["left"]["value"]
        right = abs(term["right"]["value"])
        v = left % right
        if left < 0:
            v -= right
        constant_term(term, v)

    elif type == "equal" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] == term["right"]["value"])

    elif type == "non_equal" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] != term["right"]["value"])

    elif type == "less" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] < term["right"]["value"])

    elif type == "less_equal" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] <= term["right"]["value"])

    elif type == "greater" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] > term["right"]["value"])

    elif type == "greater_equal" and check_both_side_are_constant(term):
        constant_term(term, term["left"]["value"] >= term["right"]["value"])

    elif type == "and" and check_both_side_are_constant(term):
        constant_term(
            term, bool(term["left"]["value"]) and bool(term["right"]["value"])
        )

    elif type == "or" and check_both_side_are_constant(term):
        constant_term(term, bool(term["left"]["value"]) or bool(term["right"]["value"]))

    elif type == "not":
        optimize_exp(term["value"])
        if term["value"]["type"] == "integer":
            constant_term(term, not bool(term["value"]["value"]))
            term["type"] = "integer"
        elif term["value"]["type"] == "char":
            constant_term(term, not bool(term["value"]["value"]))
            term["type"] = "char"

    elif type == "sizeof":
        term["value"] = sizeof(term["typee"])
        term["types"] = INT

    elif type == "val":
        optimize_left_value(term["left_value"])

    elif type in ["convert_to_pointer", "convert_to_int"]:
        optimize_exp(term["value"])
        if term["value"]["type"] in ["integer", "char"]:
            term["type"] = term["value"]["type"]
            term["value"] = term["value"]["value"]

    elif type == "tab":
        for element in term["elements"]:
            optimize_exp(element)


def optimize_stmt(term):
    action = term["action"]

    if action == "return":
        if "value" in term:
            optimize_exp(term["value"])
    elif action == "call":
        for arg in term["args"]:
            optimize_exp(arg)
    elif action == "var_set":
        optimize_left_value(term["left_value"])
        optimize_exp(term["value"])
    elif action == "def_var_local_set":
        optimize_exp(term["value"])
    elif action == "block":
        for stmt in term["statements"]:
            optimize_stmt(stmt)
    elif action == "if_else":
        optimize_exp(term["condition"])
        optimize_stmt(term["then_body"])
        optimize_stmt(term["else_body"])
    elif action == "while":
        optimize_exp(term["condition"])
        optimize_stmt(term["body"])


def optimize_ast(term):
    for definition in term:
        if definition["action"] == "def_fun":
            optimize_stmt(definition["body"])
