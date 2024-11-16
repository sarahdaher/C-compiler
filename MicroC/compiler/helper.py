def add_offset(offset):
    if offset != 0:
        return "\tsubq ${}, %rsp\n".format(16 - offset)
    return ""

def remove_offset(offset):
    if offset != 0:
        return "\taddq ${}, %rsp\n".format(16 - offset)
    return ""

def get_var_pointer(name, dict):
    if name in dict:
        return "{}(%rbp)".format(dict[name])
    return ".{}(%rip)".format(name)

def grow_offset(dict, size):
    dict["_offset"] = (dict["_offset"] + size) % 16

def gen_call(name, dict):
    code = add_offset(dict["_offset"])
    code += "\tcall {}\n".format(name)
    code += remove_offset(dict["_offset"])
    return code
