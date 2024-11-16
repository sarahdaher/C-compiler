import json
import sys
from function import *

def read(filename):
    with open(filename) as f:
        term = json.load(f)
        return term

def write(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

skeleton = '''\t.data
.out_int:
    .string "%d\\n"
.in_int:
    .string "%d"
{variables}
    .text
print:
    subq $8, %rsp
    leaq .out_int(%rip), %rdi
    movq $0, %rax
    call printf
    addq $8, %rsp
    ret

read:
    subq $8, %rsp
    leaq (%rsp), %rsi 
    leaq .in_int(%rip), %rdi 
    movq $0, %rax 
    call scanf
    movq (%rsp), %rax
    addq $8, %rsp
    ret

    .globl main
{functions}\t.section .note.GNU-stack
'''

def compile(term):
    functions = ""
    var_global = ""

    for definition in term:
        if definition["action"] == "def_fun":
            functions += gen_function(definition)
        if definition["action"] == "def_var_global":
            var_global += ".{}: .quad 0x0\n".format(definition["name"])
            
    return skeleton.format(variables=var_global,functions=functions)

filename = sys.argv[-1]
term = read(sys.argv[-1])
assembler = compile(term)
filename_s = filename[:-4] + "s" # file.json => file.s
write(filename_s, assembler)
