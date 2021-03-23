# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWarpx(PythonPackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    These are the Python bindings of WarpX with PICMI input support.
    See the C++ 'warpx' package for the WarpX application and library.
    """

    homepage = "https://ecp-warpx.github.io"
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'RemiLehe']

    version('develop', branch='development')

    variant('mpi', default=True,
            description='Enable MPI support')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-mpi4py@2.0.0:', type=('build', 'run'), when='+mpi')
    depends_on('py-periodictable@1.5:', type=('build', 'run'))
    depends_on('py-picmistandard', type=('build', 'run'))
    depends_on('py-setuptools@38.6:', type='build')
    depends_on('py-wheel', type='build')
    depends_on('warpx +lib ~mpi +shared', type=('build', 'link'), when='~mpi')
    depends_on('warpx +lib +mpi +shared', type=('build', 'link'), when='+mpi')

    def setup_build_environment(self, env):
        env.set('PYWARPX_LIB_DIR', self.spec['warpx'].prefix.lib)
