#!/bin/bash

cd lexer_parser
dune clean
cd ..
cd tests
rm *.res *.s *.exe *.json
cd ..
