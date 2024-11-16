import json
import sys
from generator import data_section, text_section, var_zero, var_string, var_quad
import generator
import function
import preamble
import type.types as types
import config
import optimize
from type.definitions import sizeof, sizeof_tab


def read(filename):
    with open(filename) as f:
        term = json.load(f)
        return term


def write(filename, text):
    with open(filename, "w") as f:
        f.write(text)


def declare_new_global_variable(term):
    size = sizeof(term["type"])

    if term["type"]["type"] == "tab":
        tab_size = sizeof_tab(term["type"])
        var_zero(term["name"] + "_", tab_size)
        var_quad(term["name"], ".{}_".format(term["name"]))
    else:
        var_zero(term["name"], size)


def compile(term):
    preamble.generate()
    global_vars = []

    data_section()
    for definition in term:
        if definition["action"] == "def_var_global":
            global_vars.append(definition["name"])
            declare_new_global_variable(definition)

    for i in range(len(types.strings)):
        var_string("_S{}".format(i), types.strings[i])

    text_section()
    for definition in term:
        if definition["action"] == "def_fun":
            function.compile(definition, global_vars)


# Import JSON
filename = sys.argv[-1]
term = read(sys.argv[-1])

# Check types
types.check_types(term)

# Optimize AST
if config.OPTIMIZE_AST:
    optimize.optimize_ast(term)

# Compile
compile(term)

# Write assembly
filename_s = filename[:-4] + "s"  # file.json => file.s
write(filename_s, generator.generate_code())
