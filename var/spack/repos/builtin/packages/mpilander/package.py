# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpilander(CMakePackage):
    """There can only be one (MPI process)!"""

    homepage = "https://github.com/MPILander/MPILander"
    git      = "https://github.com/MPILander/MPILander.git"

    maintainers = ['ax3l']

    version('develop', branch='master')

    # variant('cuda', default=False, description='Enable CUDA support')
    # variant(
    #     'schedulers',
    #     description='List of supported schedulers',
    #     values=('alps', 'lsf', 'tm', 'slurm', 'sge', 'loadleveler'),
    #     multi=True
    # )

    depends_on('cmake@3.9.2:', type='build')

    provides('mpi@:3.1')

    # compiler support
    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.8')
    conflicts('%apple-clang@:7.4')
    conflicts('%intel@:16')

    def cmake_args(self):
        args = [
            # tests and examples
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBUILD_EXAMPLES:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
        ]

        return args
