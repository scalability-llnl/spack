#!/bin/bash

# Set a compiler to test with, e.g. '%gcc', '%clang', etc.
compiler=''
cuda_arch="70"

mfem='mfem'${compiler}
mfem_dev='mfem@develop'${compiler}

backends='+occa+raja+libceed'
backends_specs='^occa~cuda ^raja~openmp'

# help the concrtizer find suitable hdf5 version (conduit constraint)
hdf5_spec='^hdf5@1.8.19:1.8.999'
# petsc spec
petsc_spec='^petsc+suite-sparse+mumps'
# strumpack spec without cuda
strumpack_spec='^strumpack~cuda'

builds=(
    # preferred version:
    ${mfem}
    ${mfem}'~mpi~metis~zlib'
    ${mfem}"$backends"'+superlu-dist+strumpack+suite-sparse+petsc+slepc \
        +sundials+pumi+gslib+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        '"$backends_specs $petsc_spec $strumpack_spec $hdf5_spec"
    ${mfem}'~mpi \
        '"$backends"'+suite-sparse+sundials+gslib+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs $hdf5_spec"
    # develop version:
    ${mfem_dev}'+shared~static'
    ${mfem_dev}'+shared~static~mpi~metis~zlib'

    # NOTE: Shared build with +gslib works on mac but not on linux
    # FIXME: As of 2020/11/03 the next config fails in PETSc ex5p:
    # ${mfem_dev}'+shared~static \
    #     '"$backends"'+superlu-dist+strumpack+suite-sparse+petsc \
    #     +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
    #     '"$backends_specs $petsc_spec $strumpack_spec $hdf5_spec"
    # Removing just petsc works:
    ${mfem_dev}'+shared~static \
        '"$backends"'+superlu-dist+strumpack+suite-sparse \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        '"$backends_specs $strumpack_spec $hdf5_spec"
    # Removing just strumpack works on linux, fails on mac:
    # ${mfem_dev}'+shared~static \
    #     '"$backends"'+superlu-dist+suite-sparse+petsc \
    #     +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
    #     '"$backends_specs $petsc_spec $hdf5_spec"
    # Petsc and strumpack: fails on linux and mac in PETSc ex5p:
    # ${mfem_dev}'+shared~static +strumpack+petsc \
    #     '$petsc_spec $strumpack_spec"

    ${mfem_dev}'+shared~static~mpi \
        '"$backends"'+suite-sparse+sundials+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs $hdf5_spec"
)

builds2=(
    # preferred version
    ${mfem}"$backends $backends_specs"
    ${mfem}'+superlu-dist'
    ${mfem}'+strumpack'" $strumpack_spec"
    ${mfem}'+suite-sparse~mpi'
    ${mfem}'+suite-sparse'
    ${mfem}'+sundials~mpi'
    ${mfem}'+sundials'
    ${mfem}'+pumi'
    ${mfem}'+gslib'
    ${mfem}'+netcdf~mpi'
    ${mfem}'+netcdf'
    ${mfem}'+mpfr'
    ${mfem}'+gnutls'
    ${mfem}'+conduit~mpi'
    ${mfem}'+conduit'
    ${mfem}'+umpire'
    ${mfem}'+petsc'" $petsc_spec"
    ${mfem}'+petsc+slepc'" $petsc_spec"
    # develop version
    ${mfem_dev}"$backends $backends_specs"
    ${mfem_dev}'+superlu-dist'
    ${mfem_dev}'+strumpack'" $strumpack_spec"
    ${mfem_dev}'+suite-sparse~mpi'
    ${mfem_dev}'+suite-sparse'
    ${mfem_dev}'+sundials~mpi'
    ${mfem_dev}'+sundials'
    ${mfem_dev}'+pumi'
    ${mfem_dev}'+gslib'
    ${mfem_dev}'+netcdf~mpi'
    ${mfem_dev}'+netcdf'
    ${mfem_dev}'+mpfr'
    ${mfem_dev}'+gnutls'
    ${mfem_dev}'+conduit~mpi'
    ${mfem_dev}'+conduit'
    ${mfem_dev}'+umpire'
    ${mfem_dev}'+petsc'" $petsc_spec"
    ${mfem_dev}'+petsc+slepc'" $petsc_spec"
)

builds_cuda=(
    ${mfem}'+cuda cuda_arch=sm_'"${cuda_arch}"

    ${mfem}'+cuda+raja+occa+libceed cuda_arch=sm_'"${cuda_arch}"' \
        ^raja+cuda~openmp cuda_arch='"${cuda_arch}"' \
        ^occa+cuda ^libceed+cuda'

    ${mfem}'+cuda+openmp+raja+occa+libceed cuda_arch=sm_'"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+petsc+slepc \
        +sundials+pumi+gslib+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        ^raja+cuda+openmp cuda_arch='"${cuda_arch}"' \
        ^occa+cuda ^libceed+cuda'" $petsc_spec"' \
        ^strumpack cuda_arch='"${cuda_arch} $hdf5_spec"

    # same builds as above with ${mfem_dev}
    ${mfem_dev}'+cuda cuda_arch=sm_'"${cuda_arch}"

    ${mfem_dev}'+cuda+raja+occa+libceed cuda_arch=sm_'"${cuda_arch}"' \
        ^raja+cuda~openmp cuda_arch='"${cuda_arch}"' \
        ^occa+cuda ^libceed+cuda'

    # add '^sundials+hypre' to help the concretizer
    ${mfem_dev}'+cuda+openmp+raja+occa+libceed cuda_arch=sm_'"${cuda_arch}"' \
        +superlu-dist+strumpack+suite-sparse+petsc+slepc \
        +sundials+pumi+gslib+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        ^raja+cuda+openmp cuda_arch='"${cuda_arch}"' \
        ^occa+cuda ^libceed+cuda'" $petsc_spec ^sundials+hypre"' \
        ^strumpack cuda_arch='"${cuda_arch} $hdf5_spec"
)


trap 'printf "\nScript interrupted.\n"; exit 33' INT

SEP='=========================================================================='
sep='--------------------------------------------------------------------------'

run_builds=("${builds[@]}" "${builds2[@]}")
# run_builds=("${builds_cuda[@]}")

for bld in "${run_builds[@]}"; do
    printf "\n%s\n" "${SEP}"
    printf "    %s\n" "${bld}"
    printf "%s\n" "${SEP}"
    eval bbb="\"${bld}\""
    spack spec -I $bbb || exit 1
    printf "%s\n" "${sep}"
    spack install --test=root $bbb || exit 2
done

# Uninstall all mfem builds:
# spack uninstall --all mfem
