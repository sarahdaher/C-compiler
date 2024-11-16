%{
  open Ast

  let rec create_type_and_name t name sizes =
      match sizes with
      | [] -> t, name
      | size :: tail -> let t, name = create_type_and_name t name tail
        in TabType (t, size), name
%}

%token EOF

(* Keywords *)
%token INT VOID CHAR RETURN WHILE BREAK CONTINUE IF ELSE SIZEOF

(* Delimiters *)
%token LPAREN RPAREN
%token RBRACE LBRACE
%token LBRACKET RBRACKET

(* Symbols *)
%token PLUS MINUS TIMES SLASH EQUAL EXCLAMATION_MARK EXCLAMATION_MARK_EQUAL
%token LESS LESS_EQUAL GREATER GREATER_EQUAL DOUBLE_AMPERSAND DOUBLE_PIPE
%token AMPERSAND COMMA SEMICOLON PERCENT DOUBLE_EQUAL

(* Variables *)
%token <string> IDENT
%token <int> INTEGER_CST
%token <char> CHAR_CST
%token <string> STR

(* Priorities *)
%nonassoc prec_if
%nonassoc ELSE
%left DOUBLE_PIPE
%left DOUBLE_AMPERSAND
%left DOUBLE_EQUAL EXCLAMATION_MARK_EQUAL
%left LESS LESS_EQUAL GREATER GREATER_EQUAL
%left PLUS, MINUS
%left TIMES, SLASH, PERCENT
%nonassoc unary_minus
%right EXCLAMATION_MARK
%nonassoc pointer
%nonassoc LBRACKET

%start prog

%type <Ast.program> prog

%%

prog:
| p = list (global_def) EOF { p }
;

types:
| INT { Int }
| VOID { Void }
| CHAR { Char }
| t = types TIMES { Pointer t }
;

type_sizeof:
| INT { Int }
| VOID { Void }
| CHAR { Char }
| t = types TIMES { Pointer t }
| t = type_sizeof LBRACKET size = INTEGER_CST RBRACKET {TabType(t, size)}

tab_type:
| { [] }
| LBRACKET size = INTEGER_CST RBRACKET tail = tab_type { size :: tail }
;

type_and_name:
| t = types name = IDENT sizes = tab_type { create_type_and_name t name sizes }
;

arg:
| r = type_and_name { let t, name = r in t, name, $loc }
;

args_list:
| { [] }
| head = arg { [head] }
| head = arg COMMA tail = args_list { head :: tail }
;

global_def:
| r = type_and_name SEMICOLON { let t, name = r in DefVarGlobal (t, name, $loc) } (* global variable *)
| t = types name = IDENT LPAREN args = args_list RPAREN body = block { DefFun (t, name, args, body, $loc) } (* function *)
;

block:
| LBRACE b = list(stmt) RBRACE { Block (b, $loc) }
;

stmt:
| b = block { b }
| name = IDENT LPAREN args = exp_list RPAREN SEMICOLON { Call (name, args, $loc) } (* appel de fonction *)

| r = type_and_name SEMICOLON { let t, name = r in DefVarLocal (t, name, $loc) } (* définition d'une variable locale *)
| lv = left_value EQUAL value = exp SEMICOLON { VarSet (lv, value, $loc) } (* assignation d'une variable *)
| r = type_and_name EQUAL value = exp SEMICOLON { let t, name = r in DefVarLocalSet(t, name, value, $loc) } (* définition et assignation d'une variable locale *)

| IF LPAREN cond = exp RPAREN then_body = stmt %prec prec_if { IfElse (cond, then_body, Block ([], $loc), $loc) } (* if seul *)
| IF LPAREN cond = exp RPAREN then_body = stmt ELSE else_body = stmt { IfElse (cond, then_body, else_body, $loc) } (* if et else *)
| WHILE LPAREN cond = exp RPAREN body = stmt { While (cond, body, $loc) } (* while *)

| RETURN value = exp SEMICOLON { Return (Some value, $loc) }
| RETURN SEMICOLON { Return (None, $loc) }
| BREAK SEMICOLON { Break $loc }
| CONTINUE SEMICOLON { Continue $loc }
;

exp_list:
| { [] }
| head = exp { [head] }
| head = exp COMMA tail = exp_list { head :: tail }
;

left_value:
| name = IDENT { Var (name, $loc) }
| lv = left_value LBRACKET index = exp RBRACKET { Deref(Add(Val(lv, $loc), index, $loc), $loc) } (* p[i] *)
| TIMES address = exp %prec pointer { Deref (address, $loc) } (* déréférence *)
;

exp:
| lv = left_value %prec pointer { Val (lv, $loc) }
| cst = INTEGER_CST { Integer (cst, $loc) } (* entier *)
| cst = CHAR_CST { Char (cst, $loc) } (* caractère *)
| str = STR { Str (str, $loc) } (* chaîne de caractères *)
| LPAREN e = exp RPAREN { e } (* parenthèses *)
| name = IDENT LPAREN args = exp_list RPAREN { CallExp (name, args, $loc) } (* appel de fonction *)
| LBRACE elements = exp_list RBRACE { Tab (elements, $loc) } (* tableau *)
| AMPERSAND lv = left_value %prec pointer { Ref (lv, $loc) } (* référence *)
| MINUS e = exp %prec unary_minus { Sub (Integer (0, $loc), e, $loc) } (* moins *)
| EXCLAMATION_MARK e = exp { Not (e, $loc) } (* négation *)
| SIZEOF LPAREN t = type_sizeof RPAREN { Sizeof (t, $loc) }

| left = exp PLUS right = exp { Add (left, right, $loc) }
| left = exp MINUS right = exp { Sub (left, right, $loc) }
| left = exp TIMES right = exp { Mul (left, right, $loc) }
| left = exp SLASH right = exp { Div (left, right, $loc) }
| left = exp PERCENT right = exp { Mod (left, right, $loc) }
| left = exp DOUBLE_AMPERSAND right = exp { And (left, right, $loc) }
| left = exp DOUBLE_PIPE right = exp { Or (left, right, $loc) }
| left = exp LESS right = exp { Less (left, right, $loc) }
| left = exp LESS_EQUAL right = exp { LessEqual (left, right, $loc) }
| left = exp GREATER right = exp { Greater (left, right, $loc) }
| left = exp GREATER_EQUAL right = exp { GreaterEqual (left, right, $loc) }
| left = exp DOUBLE_EQUAL right = exp { Equal (left, right, $loc) }
| left = exp EXCLAMATION_MARK_EQUAL right = exp { NonEqual (left, right, $loc) }
;
