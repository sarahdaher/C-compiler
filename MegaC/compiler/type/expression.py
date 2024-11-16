import type.types as types
import helper
from type.definitions import *


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
    "and",
    "or",
]


def convert_to(term, t):
    if type(term) != dict:
        return

    term["types"] = t

    if "value" in term:
        convert_to(term["value"], t)
    if "left" in term:
        convert_to(term["left"], t)
    if "right" in term:
        convert_to(term["right"], t)


def check_left_value(scopes, term):
    type = term["type"]

    if type == "variable":
        t = types.get_variable_type(scopes, term)
        term["types"] = t
        return t

    if type == "dereference":
        check_expression(scopes, term["address"])
        sub_type = term["address"]["types"]

        if sub_type["type"] not in ["pointer", "tab"]:
            helper.raise_error("Can't dereference a non pointer variable", term)

        term["types"] = sub_type["sub_type"]
        return sub_type["sub_type"]


def check_call(scopes, term):
    name = term["name"]
    args = term["args"]

    if name in types.functions:
        expected_args = types.functions[name]["args"]

        if len(args) != len(expected_args):
            helper.raise_error(
                "Function {} expects {} arguments but provided {}".format(
                    name, len(expected_args), len(args)
                ),
                term,
            )

        for i in range(len(expected_args)):
            check_expression(scopes, args[i])
            types.assert_same_type(args[i]["types"], expected_args[i], args[i])

        term["types"] = types.functions[name]["type"]

    else:
        helper.raise_error("Function {} does not exists".format(name), term)


def check_sub(scopes, term):
    left = term["left"]
    right = term["right"]
    check_expression(scopes, left)
    check_expression(scopes, right)

    if left["types"]["type"] == "pointer" and right["types"]["type"] == "pointer":
        types.assert_same_type(left["types"], right["types"], term)
        term["types"] = left["types"]
        term["left"] = {"type": "convert_to_int", "value": term.copy(), "types": INT}
        term["type"] = "div"
        term["right"] = {
            "type": "integer",
            "value": sizeof(left["types"]["sub_type"]),
            "types": INT,
        }
        term["types"] = INT
        return

    check_add(scopes, term)


def check_add(scopes, term):
    left = term["left"]
    right = term["right"]
    check_expression(scopes, left)
    check_expression(scopes, right)
    types.assert_number(right)
    left_type = left["types"]

    if left_type["type"] in ["pointer", "tab"]:
        if left_type["type"] == "pointer":
            size = sizeof(left_type["sub_type"])
        else:
            size = sizeof_tab(left_type["sub_type"])

        term["right"] = right = {
            "type": "convert_to_pointer",
            "value": {
                "type": "mul",
                "left": right,
                "right": {
                    "type": "integer",
                    "types": right["types"],
                    "value": size,
                },
                "types": right["types"],
            },
            "types": left["types"],
        }
    else:
        types.assert_number(left)

    types.assert_same_type(left["types"], right["types"], term)
    term["types"] = left["types"]


def check_binop(scopes, term):
    type = term["type"]

    if type == "sub":
        check_sub(scopes, term)
        return

    if type == "add":
        check_add(scopes, term)
        return

    left = term["left"]
    right = term["right"]
    check_expression(scopes, left)
    check_expression(scopes, right)
    types.assert_number(left)
    types.assert_number(right)
    types.assert_same_type(left["types"], right["types"], term)
    term["types"] = left["types"]


def check_expression(scopes, term):
    type = term["type"]

    if type == "integer":
        term["types"] = INT

    elif type == "char":
        term["types"] = CHAR

    elif type in BINOP:
        check_binop(scopes, term)

    elif type == "not":
        check_expression(scopes, term["value"])
        term["types"] = term["value"]["types"]

    elif type == "val":
        term["types"] = check_left_value(scopes, term["left_value"])

    elif type == "call":
        check_call(scopes, term)

    elif type == "reference":
        subtype = check_left_value(scopes, term["left_value"])
        term["types"] = {"type": "pointer", "sub_type": subtype}

    elif type == "sizeof":
        term["types"] = INT

    elif type == "string":
        term["types"] = {"type": "pointer", "sub_type": CHAR}
        index = len(types.strings)
        types.strings.append(term["value"])
        term["value"] = index

    elif type == "tab":
        t = "all"

        for element in term["elements"]:
            check_expression(scopes, element)
            types.assert_same_type(element["types"], t, element)
            t = element["types"]

        term["types"] = {"type": "pointer", "sub_type": t}
