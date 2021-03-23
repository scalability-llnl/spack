#!/bin/bash

grep -e "No errors detected" "$1" > test-result.txt
grep -e "PASSED" "$2" >> test-result.txt

if cmp -s $3 test-result.txt; then
    echo "Test of n2p2 PASSED !"
else
    echo "Test of n2p2 Failed !"
fi

rm $1 $2 test-result.txt
