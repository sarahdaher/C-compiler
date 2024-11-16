#!/bin/bash

initial_dir=$(pwd)
dir="$(dirname -- "${BASH_SOURCE[0]}")"

cd $dir/MegaC/lexer_parser
dune build
cd ../..
cd $initial_dir
$dir/MegaC/lexer_parser/expr2json.exe $1
python3 $dir/MegaC/compiler/compile.py "${1%.c}.json"

if [ "$2" == "exec" ]; then
	gcc -g -o "${1%.c}.exe" "${1%.c}.s"
	"./${1%.c}.exe"
fi
