{
  open Lexing
  open Parser
   
  exception Lexing_error of char

  let id_or_kwd s = match s with
  | "int" -> INT
  | "char" -> CHAR
  | "void" -> VOID
  | "return" -> RETURN
  | "if" -> IF 
  | "else" -> ELSE 
  | "while" -> WHILE
  | "break" -> BREAK
  | "continue" -> CONTINUE
  | "sizeof" -> SIZEOF
  | s -> IDENT s  
}

let letter = ['a'-'z' 'A'-'Z']
let digit = ['0'-'9']
let ident = letter (letter | digit | '_')*
let space = [' ' '\t']
let chaine = ([^'\"']|'\\''\n'|'\\''\"')*

rule token = parse
  | '\n' { new_line lexbuf; token lexbuf }
  | space+ { token lexbuf }
  | ident as id { id_or_kwd id }
  | digit+ as d { INTEGER_CST (int_of_string d) }
  | ';' { SEMICOLON }
  | '{' { LBRACE }
  | '}' { RBRACE }
  | '(' { LPAREN }
  | ')' { RPAREN }
  | '[' { LBRACKET }
  | ']' { RBRACKET }
  | '+' { PLUS }
  | '-' { MINUS }
  | '*' { TIMES }
  | '/' { SLASH }
  | '%' { PERCENT }
  | '=' { EQUAL }
  | "==" { DOUBLE_EQUAL }
  | '!' { EXCLAMATION_MARK }
  | "!=" { EXCLAMATION_MARK_EQUAL }
  | '<' { LESS }
  | '>' { GREATER }
  | "<=" { LESS_EQUAL }
  | ">=" { GREATER_EQUAL }
  | "&&" { DOUBLE_AMPERSAND }
  | "||" { DOUBLE_PIPE }
  | ',' { COMMA }
  | '&' { AMPERSAND }
  | eof { EOF }
  | ''' _ as c ''' { CHAR_CST (String.get c 1) }
  | '\"' (chaine as s) '\"' { STR s }  
  | "'\\n'" { CHAR_CST '\n' }
  | "'\\0'" { CHAR_CST '\x00' }
  | _ as c { raise (Lexing_error c) }
