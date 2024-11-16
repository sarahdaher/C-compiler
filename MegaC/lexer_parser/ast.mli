type ppos = Lexing.position * Lexing.position

type program = global_def list
and types = Int | Void | Char | Pointer of types | TabType of types * int
and arg = types * string * ppos

and global_def =
  | DefVarGlobal of types * string * ppos
  | DefFun of types * string * arg list * stmt * ppos

and stmt =
  | Return of exp option * ppos
  | Call of string * exp list * ppos
  | DefVarLocal of types * string * ppos
  | VarSet of left_value * exp * ppos
  | DefVarLocalSet of types * string * exp * ppos
  | Block of stmt list * ppos
  | IfElse of exp * stmt * stmt * ppos
  | While of exp * stmt * ppos
  | Break of ppos
  | Continue of ppos

and left_value = Var of string * ppos | Deref of exp * ppos

and exp =
  | Integer of int * ppos
  | Char of char * ppos
  | Str of string * ppos
  | Add of exp * exp * ppos
  | Sub of exp * exp * ppos
  | Mul of exp * exp * ppos
  | Div of exp * exp * ppos
  | Mod of exp * exp * ppos
  | Equal of exp * exp * ppos
  | NonEqual of exp * exp * ppos
  | Less of exp * exp * ppos
  | LessEqual of exp * exp * ppos
  | Greater of exp * exp * ppos
  | GreaterEqual of exp * exp * ppos
  | And of exp * exp * ppos
  | Or of exp * exp * ppos
  | Not of exp * ppos
  | CallExp of string * exp list * ppos
  | Tab of exp list * ppos
  | Val of left_value * ppos
  | Ref of left_value * ppos
  | Sizeof of types * ppos

val toJSON : program -> Yojson.t
