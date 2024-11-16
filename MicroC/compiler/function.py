from statement import *

def gen_function(function):
    instructions = ""
    dict = {"_offset": 8, "_acc": -8, function["arg"]: -8}
    for inst in function["body"]:
        instructions += gen_statement(inst, dict)
    return '''{}:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rax
{}
'''.format(function["name"], instructions)
