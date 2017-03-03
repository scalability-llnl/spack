#!/bin/sh

function s {
	spack find $@ | grep 'No package'
	if [ $? -eq 0 ]
	then
		spack install $@
	else
		echo "$@ has been installed."
	fi
}

compilers=(
    %gcc@6.3.0
    %intel@17.0.1
)

mpis=(
    openmpi@1.6.5
    openmpi@1.10.3
    openmpi@2.0.2
    mvapich2
    mpich
)

pkgs=(
    mdtest
    simul
    sga
)

# CUDA
s cuda@8.0.44 %gcc@5
s cuda@8.0.44 %intel@16
s cuda@7.5.18 %gcc@4.8.5
s cuda@7.5.18 %intel@15

# Perl
s perl@5.24.1 %gcc@6
s perl@5.24.1 %intel@17 cflags="-fPIC"

# Python, R, Boost
for compiler in "${compilers[@]}"
do
s python@2.7.13 $compiler
s python@3.6.0  $compiler
s r@3.3.2 	    $compiler
s boost 	    $compiler
done

# MPI and MPI-dependent Libraries
for compiler in "${compilers[@]}"
do
	for mpi in "${mpis[@]}"
	do
		s $mpi $compiler
		for pkg in "${pkgs[@]}"
			s $pkg ^$mpi $compiler
	done
done

# Other packages
