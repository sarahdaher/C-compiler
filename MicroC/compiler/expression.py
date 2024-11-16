from helper import *


def gen_call_exp(name, arg, dict):
    code = gen_exp(arg, dict)
    code += "\tpopq %rax\n"
    code += gen_call(name, dict)
    code += "\tpushq %rax\n"
    return code


BINOP = ["add", "sub", "mul", "div", "mod"]

BINOP_CODE = {
    "add": """\tpopq %rax
    popq %rbx
    addq %rax, %rbx
    pushq %rbx
""",
    "sub": """\tpopq %rax
    popq %rbx
    subq %rax, %rbx
    pushq %rbx
""",
    "mul": """\tpopq %rax
    popq %rbx
    imulq %rax, %rbx
    pushq %rbx
""",
    "div": """\tpopq %rbx
    popq %rax
    cqto
    idivq %rbx
    pushq %rax
""",
    "mod": """\tpopq %rbx
    popq %rax
    movq $0, %rdx
    idivq %rbx
    pushq %rdx
""",
}


def gen_exp(exp, dict):
    if exp["type"] == "cst":
        return "\tpushq ${}\n".format(exp["value"])

    if exp["type"] == "var_get":
        var_pointer = get_var_pointer(exp["name"], dict)
        return "\tpushq {}\n".format(var_pointer)

    if exp["type"] == "call":
        return gen_call_exp(exp["name"], exp["value"], dict)

    if exp["type"] in BINOP:
        code = gen_exp(exp["left"], dict) + gen_exp(exp["right"], dict)
        code += BINOP_CODE[exp["type"]]
        return code
