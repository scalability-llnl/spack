# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kripke(CMakePackage):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
       transport proxy/mini app.
    """
    homepage = "https://computing.llnl.gov/projects/co-design/kripke"
    git      = "https://github.com/LLNL/Kripke.git"

    tags = ['proxy-app']
    version('1.2.4', submodules=True, tag='v1.2.4')
    version('1.2.3', submodules=True, tag='v1.2.3')
    version('1.2.2', submodules=True, tag='v1.2.2-CORAL2')
    version('1.2.1', submodules=True, tag='v1.2.1-CORAL2')
    version('1.2.0', submodules=True, tag='v1.2.0-CORAL2')

    variant('mpi',    default=True, description='Build with MPI.')
    variant('openmp', default=True, description='Build with OpenMP enabled.')
    variant('caliper', default=False, description='Build with Caliper support enabled.')

    depends_on('mpi', when='+mpi')
    depends_on('cmake@3.0:', type='build')
    depends_on('caliper', when='+caliper')

    def cmake_args(self):
        def enabled(variant):
            return (1 if variant in self.spec else 0)

        return [
            '-DENABLE_OPENMP=%d' % enabled('+openmp'),
            '-DENABLE_MPI=%d' % enabled('+mpi'),
            '-DENABLE_CALIPER=%d' % enabled('+caliper'),
        ]

    def install(self, spec, prefix):
        # Kripke does not provide install target, so we have to copy
        # things into place.
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, 'bin/kripke.exe'), prefix.bin)
