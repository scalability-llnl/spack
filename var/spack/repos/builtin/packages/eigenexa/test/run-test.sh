#!/bin/bash

$@ 2>&1 | tee  run_test_results.txt
/usr/bin/sh result-check.sh run_test_results.txt 
