# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class KokkosNvccWrapper(Package):
    """The NVCC wrapper provides a wrapper around NVCC to make it a
       'full' C++ compiler that accepts all flags"""

    # We no longer maintain this as a separate repo
    # Download the Kokkos repo and install from there
    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/archive/3.1.01.tar.gz"

    version('3.2.00', sha256='05e1b4dd1ef383ca56fe577913e1ff31614764e65de6d6f2a163b2bddb60b3e9')
    version('3.1.01', sha256='ff5024ebe8570887d00246e2793667e0d796b08c77a8227fe271127d36eec9dd')
    version('3.1.00', sha256="b935c9b780e7330bcb80809992caa2b66fd387e3a1c261c955d622dae857d878")
    version('3.0.00', sha256="c00613d0194a4fbd0726719bbed8b0404ed06275f310189b3493f5739042a92b")
    version('master',  branch='master')
    version('develop', branch='develop')

    variant("mpi", default=True,
            description="use with MPI as the underlying compiler")
    depends_on("cuda")
    depends_on("mpi", when="+mpi")
    depends_on("cmake@3.10:", type='build')

    def install(self, spec, prefix):
        src = os.path.join("bin", "nvcc_wrapper")
        mkdir(prefix.bin)
        install(src, prefix.bin)

    def setup_dependent_build_environment(self, env, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        env.set('CUDA_ROOT', dependent_spec["cuda"].prefix)
        env.set('NVCC_WRAPPER_DEFAULT_COMPILER', self.compiler.cxx)
        env.set('KOKKOS_CXX', self.compiler.cxx)
        env.set('MPICH_CXX', wrapper)
        env.set('OMPI_CXX', wrapper)

    def setup_dependent_package(self, module, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        self.spec.kokkos_cxx = wrapper
