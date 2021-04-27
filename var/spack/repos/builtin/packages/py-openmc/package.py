# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyOpenmc(PythonPackage):
    """The OpenMC project aims to provide a fully-featured Monte Carlo particle
       transport code based on modern methods. It is a constructive solid
       geometry, continuous-energy transport code that uses ACE format cross
       sections. The project started under the Computational Reactor Physics
       Group at MIT."""

    homepage = "http://openmc.readthedocs.io/"
    url = "https://github.com/openmc-dev/openmc/tarball/v0.11.0"
    git = "https://github.com/openmc-dev/openmc.git"

    version('develop', branch='develop')
    version('master', branch='master')
    version('0.12.0', tag='v0.12.0', submodules=True)
    version('0.11.0', sha256='19a9d8e9c3b581e9060fbd96d30f1098312d217cb5c925eb6372a5786d9175af')

    variant('mpi', default=False, description='Enable MPI support')

    # keep py-openmc and openmc at the same version
    for ver in ['develop', 'master', '0.12.0', '0.11.0']:
        depends_on(
            'openmc+mpi@{0}'.format(ver), when='@{0}+mpi'.format(ver),
            type=('build', 'run')
        )
        depends_on(
            'openmc~mpi@{0}'.format(ver), when='@{0}~mpi'.format(ver),
            type=('build', 'run')
        )

    depends_on('git', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('py-h5py~mpi', when='~mpi', type=('build', 'run'))
    depends_on('py-h5py+mpi', when='+mpi', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-uncertainties', type=('build', 'run'))

    @run_after('install')
    def install_lib(self):
        install(join_path(self.spec['openmc'].prefix.lib, 'libopenmc.*'),
                self.prefix.lib)
