#!/bin/bash

for file in tests/*.c
do
	res=${file%.c}.res
	expect=${file%.c}.txt
	in=${file%.c}.in
	if [ -f $in ]; then
		../interpret.sh $file < $in > $res 2> /dev/null
	else
		../interpret.sh $file > $res 2> /dev/null
	fi
	if diff $res $expect > /dev/null; then
		echo -e "\033[0;32m[OK] $file\033[0m"
	else
		echo -e "\033[0;31m[KO] $file\033[0m"
		diff $res $expect
		echo ""
	fi
done
