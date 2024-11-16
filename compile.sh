#!/bin/bash

initial_dir=$(pwd)
dir="$(dirname -- "${BASH_SOURCE[0]}")"

cd $dir/MicroC/lexer_parser
dune build
cd ../..
cd $initial_dir
$dir/MicroC/lexer_parser/expr2json.exe $1
python3 $dir/MicroC/compiler/compile.py "${1%.c}.json"
