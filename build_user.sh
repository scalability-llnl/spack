#!/usr/bin/env python3

from spack_install import install
from spack_install import check_pass
import os

# Register exernal packages
for pkg in ["jdk@8u141-b15%gcc@4.8.5",
            "bazel@0.4.5%gcc@4.8.5",
            "gcc@6.4.0%gcc@4.8.5",
            "gcc@5.4.0%gcc@4.8.5",
            "gcc@4.9.4%gcc@4.8.5",
            "maven@3.3.9%gcc@4.8.",
            "gradle@3.4%gcc@4.8.5",
            "ant@1.9.9%gcc@4.8.5",
            "sbt@0.13.12%gcc@4.8.5",
            "cmake@3.10.0%gcc@4.8.5",
            "environment-modules@3.2.10",
            "intel-parallel-studio@cluster.2017.5+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune  %intel@17.0.5 threads=openmp"]:
           os.system("spack install {}".format(pkg))
