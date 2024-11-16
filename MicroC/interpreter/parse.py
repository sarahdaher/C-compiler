from obj import *

def parse_expr(e):
    if e["type"] == "cst":
        expr = Expr(EXPR_CST)
        expr.value = e["value"]
        return expr

    if e["type"] == "add":
        expr = Expr(EXPR_ADD)
        expr.left = parse_expr(e["left"])
        expr.right = parse_expr(e["right"])
        return expr

    if e["type"] == "sub":
        expr = Expr(EXPR_SUB)
        expr.left = parse_expr(e["left"])
        expr.right = parse_expr(e["right"])
        return expr

    if e["type"] == "mul":
        expr = Expr(EXPR_MUL)
        expr.left = parse_expr(e["left"])
        expr.right = parse_expr(e["right"])
        return expr

    if e["type"] == "div":
        expr = Expr(EXPR_DIV)
        expr.left = parse_expr(e["left"])
        expr.right = parse_expr(e["right"])
        return expr

    if e["type"] == "mod":
        expr = Expr(EXPR_MOD)
        expr.left = parse_expr(e["left"])
        expr.right = parse_expr(e["right"])
        return expr

    if e["type"] == "var_get":
        expr = Expr(EXPR_VAR_GET)
        expr.name = e["name"]
        return expr 

    if e["type"] == "call":
        expr = Expr(EXPR_CALL)
        expr.name = e["name"]
        expr.value = parse_expr(e["value"])
        return expr

def parse_body(body):
    statements = []

    for s in body:
        if s["action"] == "print":
            stmt = Statement(ACTION_PRINT)
            stmt.value = parse_expr(s["value"])
            statements.append(stmt)

        elif s["action"] == "return":
            stmt = Statement(ACTION_RETURN)
            stmt.value = parse_expr(s["value"])
            statements.append(stmt)

        elif s["action"] == "def_var_local":
            stmt = Statement(ACTION_DEF_VAR)
            stmt.name = s["name"]
            statements.append(stmt)

        elif s["action"] == "var_set":
            stmt = Statement(ACTION_VAR_SET)
            stmt.name = s["name"]
            stmt.value = parse_expr(s["value"])
            statements.append(stmt)

        elif s["action"] == "call":
            stmt = Statement(ACTION_CALL)
            stmt.name = s["name"]
            stmt.value = parse_expr(s["value"])
            statements.append(stmt)

        elif s["action"] == "read":
            stmt = Statement(ACTION_READ)
            stmt.name = s["name"]
            statements.append(stmt)

        elif s["action"] == "def_var_local_set":
            stmt = Statement(ACTION_DEF_VAR)
            stmt.name = s["name"]
            statements.append(stmt)
            stmt = Statement(ACTION_VAR_SET)
            stmt.name = s["name"]
            stmt.value = parse_expr(s["value"])
            statements.append(stmt)

    return statements

def parse_json(json):
    functions = {}
    global_vars = {}

    for f in json:
        if f["action"] == "def_fun":
            functions[f["name"]] = Function(f["name"], f["arg"], parse_body(f["body"]))

        elif f["action"] == "def_var_global":
            global_vars[f["name"]] = None
    
    return {
        "functions": functions,
        "vars": global_vars
    }
