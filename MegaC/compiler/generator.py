from type.definitions import *
import config


CST = 0
REG = 1
ADDRESS = 2
LABEL_ADDRESS = 3

REG_A = {"type": REG, 1: "%al", 2: "%ax", 4: "%eax", 8: "%rax"}
REG_B = {"type": REG, 1: "%bl", 2: "%bx", 4: "%ebx", 8: "%rbx"}
REG_C = {"type": REG, 1: "%cl", 2: "%cx", 4: "%ecx", 8: "%rcx"}
REG_D = {"type": REG, 1: "%dl", 2: "%dx", 4: "%edx", 8: "%rdx"}
REG_DI = {"type": REG, 1: "%dil", 2: "%di", 4: "%edi", 8: "%rdi"}
REG_SI = {"type": REG, 1: "%sil", 2: "%si", 4: "%esi", 8: "%rsi"}
REG_SP = {"type": REG, 1: "%spl", 2: "%sp", 4: "%esp", 8: "%rsp"}
REG_BP = {"type": REG, 1: "%bpl", 2: "%bp", 4: "%ebp", 8: "%rbp"}
REG_8 = {"type": REG, 1: "%r8b", 2: "%r8w", 4: "%r8d", 8: "%r8"}
REG_9 = {"type": REG, 1: "%r9b", 2: "%r9w", 4: "%r9d", 8: "%r9"}
REG_10 = {"type": REG, 1: "%r10b", 2: "%r10w", 4: "%r10d", 8: "%r10"}
REG_11 = {"type": REG, 1: "%r11b", 2: "%r11w", 4: "%r11d", 8: "%r11"}
REG_12 = {"type": REG, 1: "%r12b", 2: "%r12w", 4: "%r12d", 8: "%r12"}
REG_13 = {"type": REG, 1: "%r13b", 2: "%r13w", 4: "%r13d", 8: "%r13"}
REG_14 = {"type": REG, 1: "%r14b", 2: "%r14w", 4: "%r14d", 8: "%r14"}
REG_15 = {"type": REG, 1: "%r15b", 2: "%r15w", 4: "%r15d", 8: "%r15"}


def cst(cst):
    return {"type": CST, "value": cst}


def address(reg, offset):
    return {"type": ADDRESS, "offset": offset, "reg": reg}


def label_address(label):
    return {"type": LABEL_ADDRESS, "label": label}


CST_ZERO = cst(0)

PUSH = 0
MOV = 1
POP = 2
ADD = 3
SUB = 4
IMUL = 5
IDIV = 6
CQTO = 7
AND = 8
CALL = 9
LEAVE = 10
RET = 11
CMOV = 12
JMP = 13
CJMP = 14
CMP = 15
LEA = 16
CDQ = 17
MOVSX = 18
COMMENT = 99


LABEL = 0
DATA_SECTION = 1
TEXT_SECTION = 2
VARIABLE = 3
GNU_SECTION = 4
GLOBL = 5


code = []


def s(size):
    if size == 8:
        return "q"
    if size == 4:
        return "l"
    if size == 2:
        return "w"
    if size == 1:
        return "b"
    return None


def push_instruction(ins):
    global code

    if config.OPTIMIZE_INS and len(code[-1]) >= 2:
        last_ins = get_last_instruction()
        if last_ins[0] in [RET, JMP]:
            return

    code[-1].append(ins)


def get_last_instruction():
    global code
    return code[-1][-1]


def pop_instruction():
    global code
    return code[-1].pop()


def mov(type, src, dst):
    if config.OPTIMIZE_INS:
        stored_ins = []
        last_ins = pop_instruction()

        while last_ins[0] == MOV:
            if (
                last_ins[1] == type
                and last_ins[3] == src
                and not (last_ins[2]["type"] == ADDRESS and dst["type"] == ADDRESS)
                and not (
                    last_ins[2]["type"] == ADDRESS and dst["type"] == LABEL_ADDRESS
                )
                and not (
                    last_ins[2]["type"] == LABEL_ADDRESS and dst["type"] == ADDRESS
                )
            ):
                break
            else:
                stored_ins.append(last_ins)
                last_ins = pop_instruction()

        if last_ins[0] == MOV:
            push_instruction([MOV, type, last_ins[2], dst])
            for stored_i in reversed(stored_ins):
                push_instruction(stored_i)
        else:
            push_instruction(last_ins)
            for stored_i in reversed(stored_ins):
                push_instruction(stored_i)
            push_instruction([MOV, type, src, dst])

    else:
        push_instruction([MOV, type, src, dst])


def push(type, value):
    push_instruction([PUSH, type, value])


def pop(type, place):
    if config.OPTIMIZE_INS:
        stored_ins = []
        last_ins = pop_instruction()

        while last_ins[0] == MOV:
            stored_ins.append(last_ins)
            last_ins = pop_instruction()

        if last_ins[0] == PUSH and last_ins[1] == type:
            if last_ins[2] != place:
                mov(type, last_ins[2], place)
            for stored_i in reversed(stored_ins):
                push_instruction(stored_i)
        else:
            push_instruction(last_ins)
            for stored_i in reversed(stored_ins):
                push_instruction(stored_i)
            push_instruction([POP, type, place])
    else:
        push_instruction([POP, type, place])


# dst = dst + value
def add(type, dst, value):
    if value == CST_ZERO:
        return

    last_ins = pop_instruction()

    if (
        config.OPTIMIZE_INS
        and last_ins[0] == ADD
        and last_ins[1] == type
        and last_ins[3]["type"] == CST
        and value["type"] == CST
        and last_ins[2] == dst
    ):
        push_instruction([ADD, type, dst, cst(value["value"] + last_ins[3]["value"])])
    else:
        push_instruction(last_ins)
        push_instruction([ADD, type, dst, value])


# dst = dst - value
def sub(type, dst, value):
    if value == CST_ZERO:
        return

    last_ins = pop_instruction()

    if (
        config.OPTIMIZE_INS
        and last_ins[0] == SUB
        and last_ins[1] == type
        and last_ins[3]["type"] == CST
        and value["type"] == CST
        and last_ins[2] == dst
    ):
        push_instruction([SUB, type, dst, cst(value["value"] + last_ins[3]["value"])])
    else:
        push_instruction(last_ins)
        push_instruction([SUB, type, dst, value])


# %rdx:%rax = %rax * value
def mul(type, value):
    push_instruction([IMUL, type, value])


# %rax = %rax / value
# %rdx = %rax % value
def div(type, value):
    if type == INT:
        push_instruction([CDQ])
    push_instruction([IDIV, type, value])


# dst = dst & value
def andi(type, dst, value):
    push_instruction([AND, type, dst, value])


def call(label):
    push_instruction([CALL, label])


def ret():
    push_instruction([RET])


def label(label):
    global code
    code.append([LABEL, label])


def comment(comment):
    last_ins = pop_instruction()

    if last_ins[0] != COMMENT:
        push_instruction(last_ins)

    push_instruction([COMMENT, comment])


def data_section():
    global code
    code.append([DATA_SECTION])


def text_section():
    global code
    code.append([TEXT_SECTION])


def global_label(label):
    global code
    code.append([GLOBL, label])


def gnu_section():
    global code
    code.append([GNU_SECTION])


def lea(src, dst):
    push_instruction([LEA, src, dst])


def var(label, value):
    global code
    code.append([VARIABLE, label, value])


def var_string(label, value):
    var(label, '.string "{}"'.format(value))


def var_zero(label, size):
    var(label, ".zero {}".format(size))


def var_quad(label, value):
    var(label, ".quad {}".format(value))


def cmp(type, operand1, operand2):
    push_instruction([CMP, type, operand1, operand2])


def cmov(type, condition, src, dst):
    push_instruction([CMOV, type, condition, src, dst])


def cjump(condition, label):
    push_instruction([CJMP, condition, label])


def jump(label):
    push_instruction([JMP, label])


def leave():
    push_instruction([LEAVE])


def movsx(src_type, src, dst_type, dst):
    push_instruction([MOVSX, src_type, src, dst_type, dst])


def change_label(instructions, old_label, new_label):
    for ins in instructions:
        if ins[0] == JMP and ins[1] == old_label:
            ins[1] = new_label
        elif ins[0] == CJMP and ins[2] == old_label:
            ins[2] = new_label


def optimize_label(i, label, instructions):
    for ins in instructions:
        if ins[0] != COMMENT:
            return

    global code
    code_len = len(code)
    j = i + 1

    while j < code_len and code[j][0] != LABEL:
        j += 1

    if j < code_len:
        for part in code:
            if part[0] == LABEL:
                change_label(part[2:], label, code[j][1])

        del code[i]


def optimize_labels():
    global code

    for i, part in enumerate(code):
        if part[0] == LABEL:
            optimize_label(i, part[1], part[2:])


string = ""


def write(code):
    global string
    string += code


def new_line():
    write("\n")


def write_instruction(ins):
    write(f"\t{ins}\n")


def v(value, size):
    type = value["type"]

    if type == CST:
        return "${}".format(value["value"])

    if type == REG:
        return value[size]

    if type == ADDRESS:
        if value["offset"] == 0:
            return "({})".format(v(value["reg"], 8))
        return "{}({})".format(value["offset"], v(value["reg"], 8))

    if type == LABEL_ADDRESS:
        return ".{}(%rip)".format(value["label"])


def generate_label(label, instructions):
    write("\n{}:\n".format(label))

    for i in instructions:
        kind = i[0]
        size_l = None
        size = None

        if len(i) >= 2:
            size = sizeof(i[1])
            size_l = s(size)

        if kind == PUSH:
            if size == 4:
                size = 8
            if size == 1:
                size = 2
            size_l = s(size)
            write_instruction("push{} {}".format(size_l, v(i[2], size)))
        elif kind == MOV:
            write_instruction(
                "mov{} {}, {}".format(size_l, v(i[2], size), v(i[3], size))
            )
        elif kind == POP:
            if size == 4:
                size = 8
            if size == 1:
                size = 2
            size_l = s(size)
            write_instruction("pop{} {}".format(size_l, v(i[2], size)))
        elif kind == ADD:
            write_instruction(
                "add{} {}, {}".format(size_l, v(i[3], size), v(i[2], size))
            )
        elif kind == SUB:
            write_instruction(
                "sub{} {}, {}".format(size_l, v(i[3], size), v(i[2], size))
            )
        elif kind == IMUL:
            write_instruction("imul{} {}".format(size_l, v(i[2], size)))
        elif kind == IDIV:
            write_instruction("idiv{} {}".format(size_l, v(i[2], size)))
        elif kind == CQTO:
            write_instruction("cqto")
        elif kind == AND:
            write_instruction(
                "and{} {}, {}".format(size_l, v(i[3], size), v(i[2], size))
            )
        elif kind == CALL:
            write_instruction("call {}".format(i[1]))
        elif kind == LEAVE:
            write_instruction("leave")
        elif kind == RET:
            write_instruction("ret")
        elif kind == CMOV:
            if size == 1:
                size = 2
            size_l = s(size)
            write_instruction(
                "cmov{}{} {}, {}".format(i[2], size_l, v(i[3], size), v(i[4], size))
            )
        elif kind == JMP:
            write_instruction("jmp {}".format(i[1]))
        elif kind == CJMP:
            write_instruction("j{} {}".format(i[1], i[2]))
        elif kind == CMP:
            write_instruction(
                "cmp{} {}, {}".format(size_l, v(i[2], size), v(i[3], size))
            )
        elif kind == LEA:
            write_instruction("leaq {}, {}".format(v(i[1], 8), v(i[2], 8)))
        elif kind == CDQ:
            write_instruction("cdq")
        elif kind == MOVSX:
            size2 = sizeof(i[3])
            size2_l = s(size2)
            if size == size2:
                write_instruction("mov{}", size_l, v(i[2], size), v(i[4], size))
            elif size > size2:
                write_instruction("pushq {}".format(v(i[2], size)))
                write_instruction("mov{} (%rsp), {}".format(size2_l, v(i[4], size2)))
                write_instruction("addq $8, %rsp")
            else:
                write_instruction("movsx {}, {}".format(v(i[2], size), v(i[4], size2)))
        elif kind == COMMENT:
            write_instruction("# {}".format(i[1]))


def generate_code():
    if config.OPTIMIZE_INS:
        optimize_labels()

    global code

    for part in code:
        kind = part[0]

        if kind == LABEL:
            generate_label(part[1], part[2:])
        elif kind == DATA_SECTION:
            new_line()
            write_instruction(".data")
        elif kind == TEXT_SECTION:
            new_line()
            write_instruction(".text")
        elif kind == VARIABLE:
            write(".{}: {}\n".format(part[1], part[2]))
        elif kind == GNU_SECTION:
            write_instruction(".section .note.GNU-stack")
        elif kind == GLOBL:
            write_instruction(".globl {}".format(part[1]))

    return string
