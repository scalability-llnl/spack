# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob

from spack.package import *


class Raxml(Package):
    """RAxML (Randomized Axelerated Maximum Likelihood) is a program for
    sequential and parallel Maximum Likelihood based inference of large
    phylogenetic trees.
    """

    homepage = "https://sco.h-its.org/exelixis/web/software/raxml"
    url = "https://github.com/stamatak/standard-RAxML/archive/v8.2.11.tar.gz"

    version('8.2.11', sha256='08cda74bf61b90eb09c229e39b1121c6d95caf182708e8745bd69d02848574d7')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('pthreads', default=False, description='Enable pthreads version')

    depends_on('mpi', when='+mpi')

    patch('nox86.patch')

    # Compiles with either GCC or ICC.
    conflicts('%cce')
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    # can't build multiple binaries in parallel without things breaking
    parallel = False

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("Makefile.*")
        for file in files:
            makefile = FileFilter(file)
            makefile.filter('gcc', spack_cc)
            if spec.satisfies('+mpi'):
                makefile.filter('mpicc', self.spec['mpi'].mpicc)

        if spec.target.family == 'x86_64':
            if spec.satisfies('+mpi +pthreads') and 'avx' in spec.target:
                make('-f', 'Makefile.AVX.HYBRID.gcc')
                install('raxmlHPC-HYBRID-AVX', prefix.bin)

            if spec.satisfies('+mpi +pthreads') and 'sse3' in spec.target:
                make('-f', 'Makefile.SSE3.HYBRID.gcc')
                install('raxmlHPC-HYBRID-SSE3', prefix.bin)

            if spec.satisfies('+mpi +pthreads'):
                make('-f', 'Makefile.HYBRID.gcc')
                install('raxmlHPC-HYBRID', prefix.bin)

            if spec.satisfies('+mpi') and 'avx' in spec.target:
                make('-f', 'Makefile.AVX.MPI.gcc')
                install('raxmlHPC-MPI-AVX', prefix.bin)

            if spec.satisfies('+mpi') and 'sse3' in spec.target:
                make('-f', 'Makefile.SSE3.MPI.gcc')
                install('raxmlHPC-MPI-SSE3', prefix.bin)

            if spec.satisfies('+mpi'):
                make('-f', 'Makefile.MPI.gcc')
                install('raxmlHPC-MPI', prefix.bin)

            if spec.satisfies('+pthreads') and 'avx' in spec.target:
                make('-f', 'Makefile.AVX.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS-AVX', prefix.bin)

            if spec.satisfies('+pthreads') and 'sse3' in spec.target:
                make('-f', 'Makefile.SSE3.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS-SSE3', prefix.bin)

            if spec.satisfies('+pthreads'):
                make('-f', 'Makefile.PTHREADS.gcc')
                install('raxmlHPC-PTHREADS', prefix.bin)

            if 'sse3' in spec.target:
                make('-f', 'Makefile.SSE3.gcc')
                install('raxmlHPC-SSE3', prefix.bin)

            if 'avx' in spec.target:
                make('-f', 'Makefile.AVX.gcc')
                install('raxmlHPC-AVX', prefix.bin)

            make('-f', 'Makefile.gcc')
            install('raxmlHPC', prefix.bin)
        else:
            if spec.satisfies('+mpi +pthreads'):
                make('-f', 'Makefile.HYBRID.nox86.gcc')
                install('raxmlHPC-HYBRID', prefix.bin)

            if spec.satisfies('+mpi'):
                make('-f', 'Makefile.MPI.nox86.gcc')
                install('raxmlHPC-MPI', prefix.bin)

            if spec.satisfies('+pthreads'):
                make('-f', 'Makefile.PTHREADS.nox86.gcc')
                install('raxmlHPC-PTHREADS', prefix.bin)

            make('-f', 'Makefile.nox86.gcc')
            install('raxmlHPC', prefix.bin)
