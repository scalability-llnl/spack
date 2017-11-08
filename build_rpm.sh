#!/bin/sh

function s {
    spack find $@ | grep 'No package'
    if [ $? -eq 0 ]
    then
        spack install --restage $@
    else
        echo "$@ has been installed."
    fi
}

externpkgs=(
    jdk@8u141-b15%gcc@4.8.5
    bazel@0.4.5%gcc@4.8.5
    gradle@3.4%gcc@4.8.5
    ant@1.9.9%gcc@4.8.5
    sbt@0.13.12%gcc@4.8.5
    cmake@3.8.1%gcc@4.8.5
)

compilers=(
    gcc@5.4.0
    intel@17.0.4
)

mpis=(
    'openmpi@2.1.1~cuda fabrics=pmi,verbs ~java schedulers=slurm'
    'openmpi@2.1.1+cuda fabrics=pmi,verbs ~java schedulers=slurm'
    'mvapich2@2.2+debug~cuda fabrics=mrail process_managers=slurm'
    # 'mvapich2@2.2+debug+cuda fabrics=mrail process_managers=slurm'
    'mpich@3.2+hydra+pmi+romio+verbs'
)

mpipkgs=(
    fftw@3.3.6-pl2+mpi+float+long_double+openmp
    # gromacs@5.1.4+mpi+plumed
    # gromacs@5.1.4+mpi+plumed+cuda
)

nonmpipkgs=(
    python@2.7.13
    python@3.6.1
    miniconda2@4.3.14
    miniconda3@4.3.14
    openblas@0.2.20 threads=openmp
    perl@5.24.1
    sga@0.10.15
    boost@1.64.0
    cuda@9.0.176
    cuda@8.0.61
    cuda@7.5.18
    cuda@6.5.14
    cudnn@7.0.cuda9
    cudnn@7.0.cuda8
    cudnn@6.0.cuda8
    cudnn@5.1.cuda8
    samtools@1.6
)

otherpkgs=(
    "r@3.4.1+external-lapack%gcc@5.4.0 ^openblas+openmp"
    "r@3.4.1+external-lapack%intel@17.0.4 ^intel-parallel-studio+mkl"
)

trandeps=(
    autoconf
    automake
    bison
    gperf
    flex
    m4
    inputproto
    help2man
    pkg-config
)

# Register external packages
for pkg in "${externpkgs[@]}"
do
    spack install $pkg
done

# MPI-dependent Libraries
for mpi in "${mpis[@]}"
do
    for compiler in "${compilers[@]}"
    do
        s $mpi %$compiler
        for pkg in "${mpipkgs[@]}"
        do
            s $pkg %$compiler ^$mpi
        done
    done
done

# Non-MPI packages
for compiler in "${compilers[@]}"
do
    for pkg in "${nonmpipkgs[@]}"
    do
        s $pkg %$compiler
    done
done

# Other packages
for pkg in "${otherpkgs[@]}"
do
    s $pkg
done

# Remove transit dependency
for pkg in "${trandeps[@]}"
do
    spack uninstall -y --all $pkg 2>&1 > /dev/null
done
