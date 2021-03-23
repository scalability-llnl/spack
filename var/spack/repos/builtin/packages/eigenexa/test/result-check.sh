#!/bin/bash

grep -q "Benchmark completed" $@
if [ $? -eq 1 ]; then
  echo "EigenExa Test Failed !"
  exit 1
fi

while read line;do
  case $line in
    *'Eigenvalue Relative Error'* )
      tmp=$line
      read line
      if [[ "$line" != '|w| is too small, so it is not severe.' ]]; then
        echo "${tmp}" >> output.txt
      fi
      ;;
    *'Eigenvalue Absolute Error'* )
      tmp=$line
      read line
      if [ "$line" != 'Do not mind it. Condition number is too large.' ] && \
         [ "$line" != 'Do not mind it. Relative error is small enough' ]; then
         echo "${tmp}" >> output.txt
      fi
      ;;
    *'Residual Error Test'* | *'Orthogonality  Test'* ) 
      echo "${line}" >> output.txt ;;
  esac
done < $@

grep -q "FAILED" output.txt
if [ $? -eq 1 ]; then
  echo "EigenExa Test Passed !"
elif [ $? -eq 0 ]; then
  echo "EigenExa Test Failed !"
fi
