open Yojson

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

let pos ((s, e) : ppos) =
  [
    ("start_line", `Int s.pos_lnum);
    ("start_char", `Int (s.pos_cnum - s.pos_bol));
    ("end_line", `Int e.pos_lnum);
    ("end_char", `Int (e.pos_cnum - e.pos_bol));
  ]

let rec toJSON_exp exp =
  match exp with
  | Cst (cst, p) ->
      `Assoc ([ ("type", `String "cst"); ("value", `Int cst) ] @ pos p)
  | Add (left, right, p) ->
      `Assoc
        ([
           ("type", `String "add");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Sub (left, right, p) ->
      `Assoc
        ([
           ("type", `String "sub");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Mul (left, right, p) ->
      `Assoc
        ([
           ("type", `String "mul");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Div (left, right, p) ->
      `Assoc
        ([
           ("type", `String "div");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Mod (left, right, p) ->
      `Assoc
        ([
           ("type", `String "mod");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | CallExp (name, value, p) ->
      `Assoc
        ([
           ("type", `String "call");
           ("name", `String name);
           ("value", toJSON_exp value);
         ]
        @ pos p)
  | VarGet (name, p) ->
      `Assoc ([ ("type", `String "var_get"); ("name", `String name) ] @ pos p)

let toJSON_stmt stmt =
  match stmt with
  | Print (value, p) ->
      `Assoc
        ([ ("action", `String "print"); ("value", toJSON_exp value) ] @ pos p)
  | Read (name, p) ->
      `Assoc ([ ("action", `String "read"); ("name", `String name) ] @ pos p)
  | Return (value, p) ->
      `Assoc
        ([ ("action", `String "return"); ("value", toJSON_exp value) ] @ pos p)
  | Call (name, value, p) ->
      `Assoc
        ([
           ("action", `String "call");
           ("name", `String name);
           ("value", toJSON_exp value);
         ]
        @ pos p)
  | DefVarLocal (name, p) ->
      `Assoc
        ([ ("action", `String "def_var_local"); ("name", `String name) ] @ pos p)
  | VarSet (name, value, p) ->
      `Assoc
        ([
           ("action", `String "var_set");
           ("name", `String name);
           ("value", toJSON_exp value);
         ]
        @ pos p)
  | DefVarLocalSet (name, value, p) ->
      `Assoc
        ([
           ("action", `String "def_var_local_set");
           ("name", `String name);
           ("value", toJSON_exp value);
         ]
        @ pos p)

let toJSON_global_def global_def =
  match global_def with
  | DefVarGlobal (name, p) ->
      `Assoc
        ([ ("action", `String "def_var_global"); ("name", `String name) ]
        @ pos p)
  | DefFun (name, arg, body, p) ->
      `Assoc
        ([
           ("action", `String "def_fun");
           ("name", `String name);
           ("arg", `String arg);
           ("body", `List (List.map toJSON_stmt body));
         ]
        @ pos p)

let toJSON p = `List (List.map toJSON_global_def p)
