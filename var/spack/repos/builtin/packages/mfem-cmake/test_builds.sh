#!/bin/bash

# Set a compiler to test with, e.g. '%gcc', '%clang', etc.
compiler=''

mfem='mfem'${compiler}
mfem_dev='mfem@develop'${compiler}

backends='+occa+raja+libceed'
backends_specs='^occa~cuda ^raja~openmp'

# Help the concrtizer find suitable hdf5 version (conduit constraint)
full_mpi_specs='^hdf5@1.8.19:1.8.999'
full_ser_specs='^hdf5@1.8.19:1.8.999'
# Restrict strumpack build
full_mpi_specs+=' ^strumpack~cuda'

builds=(
    # preferred version:
    ${mfem}
    ${mfem}'~mpi~metis~zlib'
    ${mfem}"$backends"'+superlu-dist+strumpack+suite-sparse+petsc \
        +sundials+pumi+gslib+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        ^petsc+suite-sparse+mumps'" $backends_specs"" $full_mpi_specs"
    ${mfem}'~mpi \
        '"$backends"'+suite-sparse+sundials+gslib+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs"" $full_ser_specs"
    # develop version:
    ${mfem_dev}'+shared~static'
    ${mfem_dev}'+shared~static~mpi~metis~zlib'

    # NOTE: Shared build with +gslib works on mac but not on linux
    # FIXME: As of 2020/11/03 the next config fails in PETSc ex5p:
    # ${mfem_dev}'+shared~static \
    #     '"$backends"'+superlu-dist+strumpack+suite-sparse+petsc \
    #     +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
    #     ^petsc+suite-sparse+mumps'" $backends_specs"" $full_mpi_specs"
    # Removing just petsc works:
    ${mfem_dev}'+shared~static \
        '"$backends"'+superlu-dist+strumpack+suite-sparse \
        +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
        '" $backends_specs"" $full_mpi_specs"
    # Removing just strumpack works on linux, fails on mac:
    # ${mfem_dev}'+shared~static \
    #     '"$backends"'+superlu-dist+suite-sparse+petsc \
    #     +sundials+pumi+mpfr+netcdf+zlib+gnutls+libunwind+conduit \
    #     ^petsc+suite-sparse+mumps'" $backends_specs"" ^hdf5@1.8.19:1.8.999"
    # Petsc and strumpack: fails on linux and mac in PETSc ex5p:
    # ${mfem_dev}'+shared~static +strumpack+petsc \
    #     ^petsc+suite-sparse+mumps ^strumpack~cuda'

    ${mfem_dev}'+shared~static~mpi \
        '"$backends"'+suite-sparse+sundials+mpfr+netcdf \
        +zlib+gnutls+libunwind+conduit'" $backends_specs"" $full_ser_specs"
)

builds2=(
    # preferred version
    ${mfem}"$backends $backends_specs"
    ${mfem}'+superlu-dist'
    ${mfem}'+strumpack ^strumpack~cuda'
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
    ${mfem}'+petsc ^petsc+suite-sparse+mumps'
    # develop version
    ${mfem_dev}"$backends $backends_specs"
    ${mfem_dev}'+superlu-dist'
    ${mfem_dev}'+strumpack ^strumpack~cuda'
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
    ${mfem_dev}'+petsc ^petsc+suite-sparse+mumps'
)

trap 'printf "\nScript interrupted.\n"; exit 33' INT

SEP='=========================================================================='
sep='--------------------------------------------------------------------------'

for bld in "${builds[@]}" "${builds2[@]}"; do
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
