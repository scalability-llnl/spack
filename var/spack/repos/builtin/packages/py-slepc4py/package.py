# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlepc4py(PythonPackage):
    """This package provides Python bindings for the SLEPc package.
    """

    homepage = "https://gitlab.com/slepc/slepc4py"
    url      = "https://gitlab.com/slepc/slepc4py/-/archive/3.12.0/slepc4py-3.12.0.tar.gz"
    git      = "https://gitlab.com/slepc/slepc4py.git"

    maintainers = ['dalcinl', 'joseeroman', 'balay']

    version('3.13.0', sha256='780eff0eea1a5217642d23cd563786ef22df27e1d772a1b0bb4ccc5701df5ea5')
    version('3.12.0', sha256='d8c06953b7d00f529a9a7fd016dfa8efdf1d05995baeea7688d1d59611f424f7')
    version('3.11.0', sha256='1e591056beee209f585cd781e5fe88174cd2a61215716a71d9eaaf9411b6a775')
    version('3.10.0', sha256='6494959f44280d3b80e73978d7a6bf656c9bb04bb3aa395c668c7a58948db1c6')
    version('3.9.0',  sha256='84cab4216268c2cb7d01e7cdbb1204a3c3e13cdfcd7a78ea057095f96f68c3c0')
    version('3.8.0',  sha256='988815b3650b69373be9abbf2355df512dfd200aa74b1785b50a484d6dfee971')
    version('3.7.0',  sha256='139f8bb325dad00a0e8dbe5b3e054050c82547936c1b6e7812fb1a3171c9ad0b')

    depends_on('py-setuptools', type='build')

    depends_on('py-petsc4py', type=('build', 'run'))
    depends_on('py-petsc4py@3.13:3.13.99', when='@3.13:3.13.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.12:3.12.99', when='@3.12:3.12.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.11:3.11.99', when='@3.11:3.11.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.10:3.10.99', when='@3.10:3.10.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.9:3.9.99', when='@3.9:3.9.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.8:3.8.99', when='@3.8:3.8.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.7:3.7.99', when='@3.7:3.7.99', type=('build', 'run'))
    depends_on('py-petsc4py@3.6:3.6.99', when='@3.6:3.6.99', type=('build', 'run'))

    depends_on('slepc')
    depends_on('slepc@3.12:3.12.99', when='@3.12:3.12.99')
    depends_on('slepc@3.11:3.11.99', when='@3.11:3.11.99')
    depends_on('slepc@3.10:3.10.99', when='@3.10:3.10.99')
    depends_on('slepc@3.9:3.9.99', when='@3.9:3.9.99')
    depends_on('slepc@3.8:3.8.99', when='@3.8:3.8.99')
    depends_on('slepc@3.7:3.7.99', when='@3.7:3.7.99')
    depends_on('slepc@3.6:3.6.99', when='@3.6:3.6.99')
