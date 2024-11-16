from type.expression import check_expression, check_call, check_left_value
import helper
import type.types as types
from type.definitions import VOID


def check_statement(scopes, term):
    action = term["action"]

    if action == "return":
        return_type = types.functions[scopes[0]["_function"]]["type"]
        value_type = VOID

        if "value" in term:
            check_expression(scopes, term["value"])
            value_type = term["value"]["types"]

        types.assert_same_type(return_type, value_type, term)

    elif action == "call":
        check_call(scopes, term)

    elif action == "def_var_local":
        if term["name"] in scopes[-1]:
            helper.raise_error(
                "Variable {} already exists in scope".format(term["name"]), term
            )

        scopes[-1][term["name"]] = term["type"]

    elif action == "var_set":
        var_type = check_left_value(scopes, term["left_value"])
        check_expression(scopes, term["value"])
        types.assert_same_type(var_type, term["value"]["types"], term["value"])

    elif action == "def_var_local_set":
        if term["name"] in scopes[-1]:
            helper.raise_error(
                "Variable {} already exists in scope".format(term["name"]), term
            )

        scopes[-1][term["name"]] = term["type"]
        check_expression(scopes, term["value"])
        types.assert_same_type(term["type"], term["value"]["types"], term["value"])

    elif action == "block":
        scopes.append({})
        for statement in term["statements"]:
            check_statement(scopes, statement)
        scopes.pop()

    elif action == "if_else":
        check_expression(scopes, term["condition"])
        check_statement(scopes, term["then_body"])
        check_statement(scopes, term["else_body"])

    elif action == "while":
        check_expression(scopes, term["condition"])
        check_statement(scopes, term["body"])
