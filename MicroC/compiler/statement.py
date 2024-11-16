import json
import sys
from expression import *
from helper import *

def gen_statement(stmt, dict):
    code = "\t# Ligne {}\n".format(stmt["start_line"])

    if stmt["action"] == "print":
        code += gen_exp(stmt["value"], dict)
        code += "\tpopq %rsi\n"
        code += gen_call("print", dict)
    
    elif stmt["action"] == "read":
        var_pointer = get_var_pointer(stmt["name"], dict)
        code += gen_call("read", dict)
        code += "\tmovq %rax, {}\n".format(var_pointer)

    elif stmt["action"] == "def_var_local_set":
        dict["_acc"] -= 8
        dict[stmt["name"]] = dict["_acc"]
        code += gen_exp(stmt["value"], dict)
        code += "\tpopq {}(%rbp)\n\tsubq $8, %rsp\n".format(dict[stmt["name"]])
        grow_offset(dict, 8)

    elif stmt["action"] == "def_var_local":
        dict["_acc"] -= 8
        dict[stmt["name"]] = dict["_acc"]
        code += "\tsubq $8, %rsp\n"
        grow_offset(dict, 8)

    elif stmt["action"] == "var_set":
        var_pointer = get_var_pointer(stmt["name"], dict)
        code += gen_exp(stmt["value"], dict)
        code += "\tpopq {}\n".format(var_pointer)

    elif stmt["action"] == "return":
        code += gen_exp(stmt["value"], dict)
        code += '''\tpopq %rax
    movq %rbp, %rsp
    popq %rbp
    ret
'''

    elif stmt["action"] == "call":
        code += gen_exp(stmt["value"], dict)
        code += "\tpopq %rax\n"
        code += gen_call(stmt["name"], dict)

    return code
