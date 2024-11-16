%{
  open Ast
%}

%token SEMICOLON INT
%token PLUS MINUS TIMES SLASH PERCENT
%token EOF
%token LBRACE RBRACE LPAREN RPAREN
%token EQUAL
%token <string> IDENT
%token <int> CST
%token RETURN
%token PRINT READ

%left PERCENT
%left PLUS, MINUS
%left TIMES, SLASH
%nonassoc uminus
%start prog

%type <Ast.program> prog

%%

prog:
  | p = list (global_def) EOF { p }
;

global_def:
  | INT name = IDENT SEMICOLON { DefVarGlobal (name, $loc) }
  | INT name = IDENT LPAREN INT arg = IDENT RPAREN LBRACE body = list (stmt) RBRACE { DefFun (name, arg, body, $loc) }
;

stmt:
  | PRINT LPAREN value = exp RPAREN SEMICOLON { Print (value, $loc) }
  | READ LPAREN name = IDENT RPAREN SEMICOLON { Read (name, $loc) }
  | RETURN value = exp SEMICOLON { Return (value, $loc) }
  | name = IDENT LPAREN value = exp RPAREN SEMICOLON { Call (name, value, $loc) }
  | INT name = IDENT SEMICOLON { DefVarLocal (name, $loc) }
  | name = IDENT EQUAL value = exp SEMICOLON { VarSet (name, value, $loc) }
  | INT name = IDENT EQUAL value = exp SEMICOLON { DefVarLocalSet (name, value, $loc) }
;

exp:
  | name = IDENT { VarGet (name, $loc) }
  | cst = CST { Cst (cst, $loc)}
  | left = exp PLUS right = exp { Add (left, right, $loc) }
  | left = exp MINUS right = exp { Sub (left, right, $loc) }
  | left = exp TIMES right = exp { Mul (left, right, $loc) }
  | left = exp SLASH right = exp { Div (left, right, $loc) }
  | left = exp PERCENT right = exp { Mod (left, right, $loc) }
  | name = IDENT LPAREN value = exp RPAREN { CallExp (name, value, $loc) }
  | MINUS value = exp %prec uminus { Sub (Cst (0, $loc), value, $loc) }
  | LPAREN value = exp RPAREN { value }
;
