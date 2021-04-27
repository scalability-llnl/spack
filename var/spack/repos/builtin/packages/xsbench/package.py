# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xsbench(MakefilePackage):
    """XSBench is a mini-app representing a key computational
       kernel of the Monte Carlo neutronics application OpenMC.
       A full explanation of the theory and purpose of XSBench
       is provided in docs/XSBench_Theory.pdf."""

    homepage = "https://github.com/ANL-CESAR/XSBench/"
    url = "https://github.com/ANL-CESAR/XSBench/archive/v13.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('19', sha256='57cc44ae3b0a50d33fab6dd48da13368720d2aa1b91cde47d51da78bf656b97e')
    version('18', sha256='a9a544eeacd1be8d687080d2df4eeb701c04eda31d3806e7c3ea1ff36c26f4b0')
    version('14', sha256='595afbcba8c1079067d5d17eedcb4ab0c1d115f83fd6f8c3de01d74b23015e2d')
    version('13', sha256='b503ea468d3720a0369304924477b758b3d128c8074776233fa5d567b7ffcaa2')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('mpi', when='+mpi')

    @property
    def build_directory(self):
        if self.spec.satisfies('@:18'):
            return 'src'
        else:
            return 'openmp-threading'

    @property
    def build_targets(self):

        targets = []
        cflags = ''

        if not self.spec.satisfies('%nvhpc@:20.11'):
            cflags = '-std=gnu99'

        if '+mpi' in self.spec:
            targets.append('CC={0}'.format(self.spec['mpi'].mpicc))
            targets.append('MPI=yes')
        else:
            targets.append('CC={0}'.format(self.compiler.cc))
            targets.append('MPI=no')

        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS=-lm')

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir(self.build_directory):
            install('XSBench', prefix.bin)
