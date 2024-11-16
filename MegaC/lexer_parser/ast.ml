open Yojson

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

let pos ((s, e) : ppos) =
  [
    ("start_line", `Int s.pos_lnum);
    ("start_char", `Int (s.pos_cnum - s.pos_bol));
    ("end_line", `Int e.pos_lnum);
    ("end_char", `Int (e.pos_cnum - e.pos_bol));
  ]

let rec toJSON_exp exp =
  match exp with
  | Integer (cst, p) ->
      `Assoc ([ ("type", `String "integer"); ("value", `Int cst) ] @ pos p)
  | Char (cst, p) ->
      `Assoc
        ([ ("type", `String "char"); ("value", `String (String.make 1 cst)) ]
        @ pos p)
  | Str (cst, p) ->
      `Assoc ([ ("type", `String "string"); ("value", `String cst) ] @ pos p)
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
           ("args", `List (List.map toJSON_exp value));
         ]
        @ pos p)
  | Val (left_value, p) ->
      `Assoc
        ([
           ("type", `String "val"); ("left_value", toJSON_left_value left_value);
         ]
        @ pos p)
  | Equal (left, right, p) ->
      `Assoc
        ([
           ("type", `String "equal");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | NonEqual (left, right, p) ->
      `Assoc
        ([
           ("type", `String "non_equal");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Less (left, right, p) ->
      `Assoc
        ([
           ("type", `String "less");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | LessEqual (left, right, p) ->
      `Assoc
        ([
           ("type", `String "less_equal");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Greater (left, right, p) ->
      `Assoc
        ([
           ("type", `String "greater");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | GreaterEqual (left, right, p) ->
      `Assoc
        ([
           ("type", `String "greater_equal");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | And (left, right, p) ->
      `Assoc
        ([
           ("type", `String "and");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Or (left, right, p) ->
      `Assoc
        ([
           ("type", `String "or");
           ("left", toJSON_exp left);
           ("right", toJSON_exp right);
         ]
        @ pos p)
  | Not (expr, p) ->
      `Assoc ([ ("type", `String "not"); ("value", toJSON_exp expr) ] @ pos p)
  | Tab (elements, p) ->
      `Assoc
        ([
           ("type", `String "tab");
           ("elements", `List (List.map toJSON_exp elements));
         ]
        @ pos p)
  | Ref (left_value, p) ->
      `Assoc
        ([
           ("type", `String "reference");
           ("left_value", toJSON_left_value left_value);
         ]
        @ pos p)
  | Sizeof (t, p) ->
      `Assoc ([ ("type", `String "sizeof"); ("typee", toJSON_type t) ] @ pos p)

and toJSON_left_value left_value =
  match left_value with
  | Var (name, p) ->
      `Assoc ([ ("type", `String "variable"); ("name", `String name) ] @ pos p)
  | Deref (address, p) ->
      `Assoc
        ([ ("type", `String "dereference"); ("address", toJSON_exp address) ]
        @ pos p)

and toJSON_type t =
  match t with
  | Int -> `Assoc [ ("type", `String "int") ]
  | Void -> `Assoc [ ("type", `String "void") ]
  | Char -> `Assoc [ ("type", `String "char") ]
  | Pointer t ->
      `Assoc [ ("type", `String "pointer"); ("sub_type", toJSON_type t) ]
  | TabType (t, size) ->
      `Assoc
        [
          ("type", `String "tab");
          ("sub_type", toJSON_type t);
          ("size", `Int size);
        ]

let rec toJSON_stmt stmt =
  match stmt with
  | Return (Some value, p) ->
      `Assoc
        ([ ("action", `String "return"); ("value", toJSON_exp value) ] @ pos p)
  | Return (None, p) -> `Assoc ([ ("action", `String "return") ] @ pos p)
  | Call (name, value, p) ->
      `Assoc
        ([
           ("action", `String "call");
           ("name", `String name);
           ("args", `List (List.map toJSON_exp value));
         ]
        @ pos p)
  | DefVarLocal (t, name, p) ->
      `Assoc
        ([
           ("action", `String "def_var_local");
           ("type", toJSON_type t);
           ("name", `String name);
         ]
        @ pos p)
  | VarSet (lv, value, p) ->
      `Assoc
        ([
           ("action", `String "var_set");
           ("left_value", toJSON_left_value lv);
           ("value", toJSON_exp value);
         ]
        @ pos p)
  | DefVarLocalSet (t, name, value, p) ->
      `Assoc
        ([
           ("action", `String "def_var_local_set");
           ("type", toJSON_type t);
           ("name", `String name);
           ("value", toJSON_exp value);
         ]
        @ pos p)
  | IfElse (cond, then_body, else_body, p) ->
      `Assoc
        ([
           ("action", `String "if_else");
           ("condition", toJSON_exp cond);
           ("then_body", toJSON_stmt then_body);
           ("else_body", toJSON_stmt else_body);
         ]
        @ pos p)
  | Block (stmts, p) ->
      `Assoc
        ([
           ("action", `String "block");
           ("statements", `List (List.map toJSON_stmt stmts));
         ]
        @ pos p)
  | While (cond, body, p) ->
      `Assoc
        ([
           ("action", `String "while");
           ("condition", toJSON_exp cond);
           ("body", toJSON_stmt body);
         ]
        @ pos p)
  | Break p -> `Assoc ([ ("action", `String "break") ] @ pos p)
  | Continue p -> `Assoc ([ ("action", `String "continue") ] @ pos p)

let toJSON_arg (t, name, p) =
  `Assoc ([ ("type", toJSON_type t); ("name", `String name) ] @ pos p)

let toJSON_global_def global_def =
  match global_def with
  | DefVarGlobal (t, name, p) ->
      `Assoc
        ([
           ("action", `String "def_var_global");
           ("type", toJSON_type t);
           ("name", `String name);
         ]
        @ pos p)
  | DefFun (t, name, args, body, p) ->
      `Assoc
        ([
           ("action", `String "def_fun");
           ("type", toJSON_type t);
           ("name", `String name);
           ("args", `List (List.map toJSON_arg args));
           ("body", toJSON_stmt body);
         ]
        @ pos p)

let toJSON p = `List (List.map toJSON_global_def p)
