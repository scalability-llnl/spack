# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Laghos(MakefilePackage):
    """Laghos (LAGrangian High-Order Solver) is a CEED miniapp that solves the
       time-dependent Euler equations of compressible gas dynamics in a moving
       Lagrangian frame using unstructured high-order finite element spatial
       discretization and explicit high-order time-stepping.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://computing.llnl.gov/projects/co-design/laghos"
    url      = "https://github.com/CEED/Laghos/archive/v1.0.tar.gz"
    git      = "https://github.com/CEED/Laghos.git"

    maintainers = ['v-dobrev', 'tzanio', 'vladotomov']

    version('develop', branch='master')
    version('3.1', sha256='49b65edcbf9732c7f6c228958620e18980c43ad8381315a8ba9957ecb7534cd5')
    version('3.0', sha256='4db56286e15b42ecdc8d540c4888a7dec698b019df9c7ccb8319b7ea1f92d8b4')
    version('2.0', sha256='dd3632d5558889beec2cd3c49eb60f633f99e6d886ac868731610dd006c44c14')
    version('1.1', sha256='53b9bfe2af263c63eb4544ca1731dd26f40b73a0d2775a9883db51821bf23b7f')
    version('1.0', sha256='af50a126355a41c758fcda335a43fdb0a3cd97e608ba51c485afda3dd84a5b34')

    variant('metis', default=True, description='Enable/disable METIS support')

    depends_on('mfem+mpi+metis', when='+metis')
    depends_on('mfem+mpi~metis', when='~metis')

    depends_on('mfem@develop', when='@develop')
    depends_on('mfem@4.2.0', when='@3.1')
    depends_on('mfem@4.1.0:4.1.99', when='@3.0')
    # Recommended mfem version for laghos v2.0 is: ^mfem@3.4.1-laghos-v2.0
    depends_on('mfem@3.4.0:', when='@2.0')
    # Recommended mfem version for laghos v1.x is: ^mfem@3.3.1-laghos-v1.0
    depends_on('mfem@3.3.1-laghos-v1.0:', when='@1.0,1.1')

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % spec['mfem'].package.config_mk)
        targets.append('TEST_MK=%s' % spec['mfem'].package.test_mk)
        if spec.satisfies('@:2.0'):
            targets.append('CXX=%s' % spec['mpi'].mpicxx)

        return targets

    # See lib/spack/spack/build_systems/makefile.py
    def check(self):
        with working_dir(self.build_directory):
            make('test', *self.build_targets)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('laghos', prefix.bin)

    install_time_test_callbacks = []
