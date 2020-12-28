# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Minigmg(Package):
    """miniGMG is a compact benchmark for understanding the performance
    challenges associated with geometric multigrid solvers
    found in applications built from AMR MG frameworks
    like CHOMBO or BoxLib when running
    on modern multi- and manycore-based supercomputers.
    It includes both productive reference examples as well as
    highly-optimized implementations for CPUs and GPUs.
    It is sufficiently general that it has been used to evaluate
    a broad range of research topics including PGAS programming models
    and algorithmic tradeoffs inherit in multigrid. miniGMG was developed
    under the CACHE Joint Math-CS Institute.

    Note, miniGMG code has been supersceded by HPGMG. """

    homepage = "http://crd.lbl.gov/departments/computer-science/PAR/research/previous-projects/miniGMG/"
    url      = "http://crd.lbl.gov/assets/Uploads/FTG/Projects/miniGMG/miniGMG.tar.gz"

    version('master', sha256='1c2d27496a881f655f5e849d6a7a132625e535739f82575991c511cc2cf899ac')

    depends_on('mpi')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spec['mpi'].mpicc)
        cc('-O3', self.compiler.openmp_flag, 'miniGMG.c',
            'mg.c', 'box.c', 'solver.c', 'operators.ompif.c', 'timer.x86.c',
            '-D__MPI', '-D__COLLABORATIVE_THREADING=6',
            '-D__TEST_MG_CONVERGENCE', '-D__PRINT_NORM', '-D__USE_BICGSTAB',
            '-o', 'run.miniGMG', '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('run.miniGMG', prefix.bin)
        mkdir(prefix.jobs)
        install('job*', prefix.jobs)
