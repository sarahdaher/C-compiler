import statement
from generator import *
from expression import ARG_REGS, NB_REGS
from type.definitions import *


def get_args_size(args):
    size = 0

    for arg in args:
        size += sizeof(arg["type"])

    return size


def compile(term, global_vars):
    all_args_size = get_args_size(term["args"])  # Taille de tous les arguments
    # Taille des arguments de 1 à NB_REGS
    after_call_args_size = get_args_size(term["args"][:NB_REGS])

    label(term["name"])
    # On sauvegarde le %rbp de la fonction qui a appelé la fonction
    push(POINTER, REG_BP)
    # On actualise %rbp au bas de la pile
    mov(POINTER, REG_SP, REG_BP)
    # On laisse de la place pour les arguments 1 à NB_REGS
    sub(POINTER, REG_SP, cst(after_call_args_size))

    env = {
        "tab": False,  # Drapeau pour savoir si on manipule des expressions de type tab
        "val_depth": 0,  # Niveau de récursion dans une expression de type val
        "loop_starts": [],  # Labels pour le début des boucles
        "loop_ends": [],  # Labels pour la fin des boucles
        "scopes": [  # Pile des scopes pour les variables locales
            {
                "_acc": -after_call_args_size,  # La prochaine place pour une variable se trouve après les arguments
                "_offset": after_call_args_size % 16,
            }
        ],
        "global_vars": global_vars,
        "name": term["name"],
        "label": 0,  # Prochain indice pour le label à générer
    }

    local_vars = env["scopes"][0]
    pos_after_call = 0  # Position pour les arguments de 1 à NB_REGS
    pos_before_call = (
        all_args_size - after_call_args_size + 16
    )  # Position pour les arguments de NB_REGS+1 à n

    for i, arg in enumerate(term["args"]):
        type = arg["type"]
        size = sizeof(type)

        if i < NB_REGS:
            # On actualise la position
            pos_after_call -= size
            local_vars[arg["name"]] = pos_after_call
            mov(type, ARG_REGS[i], address(REG_BP, pos_after_call))
        else:
            # On actualise la position
            pos_before_call -= size
            local_vars[arg["name"]] = pos_before_call

    statement.compile(term["body"], env)
    # Pour les fonctions qui n'ont pas de return, on retourne ici
    leave()
    ret()
