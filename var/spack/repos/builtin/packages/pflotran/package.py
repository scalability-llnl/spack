# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pflotran(AutotoolsPackage):
    """PFLOTRAN is an open source, state-of-the-art massively parallel
       subsurface flow and reactive transport code.
    """

    homepage = "http://www.pflotran.org"
    git      = "https://bitbucket.org/pflotran/pflotran.git"

    maintainers = ['ghammond86', 'balay']

    version('develop')
    version('xsdk-0.6.0', commit='46e14355c1827c057f2e1b3e3ae934119ab023b2')
    version('xsdk-0.5.0', commit='98a959c591b72f73373febf5f9735d2c523b4c20')
    version('xsdk-0.4.0', commit='c851cbc94fc56a32cfdb0678f3c24b9936a5584e')
    version('xsdk-0.3.0', branch='release/xsdk-0.3.0')
    version('xsdk-0.2.0', commit='4da763c6136df57caff43f98c926433958cfdea6')

    depends_on('mpi')
    depends_on('hdf5@1.8.12:+mpi+fortran+hl')
    depends_on('petsc@main:+hdf5+metis', when='@develop')
    depends_on('petsc@3.14:+hdf5+metis', when='@xsdk-0.6.0')
    depends_on('petsc@3.12:+hdf5+metis', when='@xsdk-0.5.0')
    depends_on('petsc@3.10:+hdf5+metis', when='@xsdk-0.4.0')
    depends_on('petsc@xsdk-0.2.0+hdf5+metis', when='@xsdk-0.2.0')
    depends_on('petsc@3.8.0:+hdf5+metis', when='@xsdk-0.3.0')

    @property
    def parallel(self):
        return (self.spec.satisfies('@xsdk-0.4.0:'))
