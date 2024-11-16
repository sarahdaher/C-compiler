from generator import *
from type.definitions import *
import config


def generate():
    data_section()
    var_string("_out_int", "%d\\n")
    var_string("_in_char", "%c")
    var_string("_in_str", "%s")
    var_string("_in_int", "%d")
    var_string("_bad_align", "Alignement is not correct!\\n")

    text_section()

    if config.CHECK_ALIGN:
        label("_check_align_1")
        push(POINTER, REG_A)
        mov(POINTER, REG_SP, REG_A)
        andi(POINTER, REG_A, cst(15))
        cmp(POINTER, cst(0), REG_A)
        cjump("ne", "_check_align_2")
        pop(POINTER, REG_A)
        ret()
        label("_check_align_2")
        mov(POINTER, cst(16), REG_B)
        sub(POINTER, REG_B, REG_A)
        sub(POINTER, REG_SP, REG_B)
        lea(label_address("_bad_align"), REG_DI)
        mov(POINTER, cst(0), REG_A)
        call("printf")
        mov(POINTER, cst(64), REG_DI)
        call("exit")

    label("print_int")
    sub(POINTER, REG_SP, cst(8))
    if config.CHECK_ALIGN:
        call("_check_align_1")
    lea(label_address("_out_int"), REG_DI)
    mov(INT, REG_A, REG_SI)
    mov(POINTER, cst(0), REG_A)
    call("printf")
    add(POINTER, REG_SP, cst(8))
    ret()

    label("read_int")
    sub(POINTER, REG_SP, cst(8))
    if config.CHECK_ALIGN:
        call("_check_align_1")
    lea(address(REG_SP, 0), REG_SI)
    lea(label_address("_in_int"), REG_DI)
    mov(POINTER, cst(0), REG_A)
    call("scanf")
    mov(POINTER, address(REG_SP, 0), REG_A)
    add(POINTER, REG_SP, cst(8))
    ret()

    label("_malloc")
    sub(POINTER, REG_SP, cst(8))
    if config.CHECK_ALIGN:
        call("_check_align_1")
    mov(INT, REG_A, REG_DI)
    call("malloc")
    add(POINTER, REG_SP, cst(8))
    ret()

    label("_printf")
    sub(POINTER, REG_SP, cst(8))
    if config.CHECK_ALIGN:
        call("_check_align_1")
    mov(POINTER, REG_A, REG_DI)
    mov(POINTER, REG_B, REG_SI)
    mov(POINTER, cst(0), REG_A)
    call("printf")
    add(POINTER, REG_SP, cst(8))
    ret()

    label("_scanf")
    sub(POINTER, REG_SP, cst(8))
    if config.CHECK_ALIGN:
        call("_check_align_1")
    mov(POINTER, REG_A, REG_DI)
    mov(POINTER, REG_B, REG_SI)
    mov(POINTER, cst(0), REG_A)
    call("scanf")
    add(POINTER, REG_SP, cst(8))
    ret()

    global_label("main")
    gnu_section()
