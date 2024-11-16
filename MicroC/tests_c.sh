#!/bin/bash

for file in tests/*.c
do
	res=${file%.c}.res
	expect=${file%.c}.txt
	in=${file%.c}.in
	exe=${file%.c}.exe
	assembler=${file%.c}.s
	../compile.sh $file
	gcc -o $exe $assembler
	if [ -f $in ]; then
		$exe < $in > $res
	else
		$exe > $res
	fi
	if diff $res $expect > /dev/null; then
		echo -e "\033[0;32m[OK] $file\033[0m"
	else
		echo -e "\033[0;31m[KO] $file\033[0m"
		diff --color=always $res $expect
		echo ""
	fi
done
