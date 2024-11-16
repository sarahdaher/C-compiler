type ppos = Lexing.position * Lexing.position

type program = global_def list

and global_def =
  | DefVarGlobal of string * ppos
  | DefFun of string * string * stmt list * ppos

and stmt =
  | Print of exp * ppos
  | Read of string * ppos
  | Return of exp * ppos
  | Call of string * exp * ppos
  | DefVarLocal of string * ppos
  | VarSet of string * exp * ppos
  | DefVarLocalSet of string * exp * ppos

and exp =
  | Cst of int * ppos
  | Add of exp * exp * ppos
  | Sub of exp * exp * ppos
  | Mul of exp * exp * ppos
  | Div of exp * exp * ppos
  | Mod of exp * exp * ppos
  | CallExp of string * exp * ppos
  | VarGet of string * ppos

val toJSON : program -> Yojson.t
