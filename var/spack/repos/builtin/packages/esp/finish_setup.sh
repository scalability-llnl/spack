#!/bin/bash

# There are a few more steps to get CGT and other codes working with ESP

cd EngSketchPad
source ESPenv.sh
cd config
./makeEnv $CASROOT
cd ../src
make -j 16
