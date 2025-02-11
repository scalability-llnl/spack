#!/bin/bash
echo "Script 22 starting........"
cd /dev/shm/shea9/tmp/spack-stage/spack-stage-pigz-2.8-64f5mnl2bfwvzv56oa77vyk2liw7uhoj/spack-src
ln -f pigz unpigz #dependent on line 94, but a linking dependence not a compile time dependence 
echo "Script 22 done."
