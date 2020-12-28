# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Portage(CMakePackage):
    """Portage is a framework that computational physics applications can use
       to build a highly customized, hybrid parallel (MPI+X) conservative
       remapping library for transfer of field data between meshes.
    """
    homepage = "http://portage.lanl.gov/"
    git      = "https://github.com/laristra/portage.git"

    # tarballs don't have submodules, so use git tags
    version('develop', branch='master', submodules=True)
    version('1.2.2', tag='v1.2.2', submodules=True)
    version('1.1.1', tag='v1.1.1', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)

    # fabs() needs math.h for gcc-7, got fixed in
    # versions above 1.2.2
    patch('gcc-7.patch', when='@:1.2.2 %gcc@7:')
    # part of https://github.com/laristra/cinch/commit/f87f848269fac25aa5b8d0bd5d9c9b2d2d6fb0ad
    # fixed in version above 1.2.2
    patch('p_lapacke_config.patch', when='@1.2.2')
    # don't enable debug prints in RelWithDebInfo build
    # fixed in version above 1.2.2
    patch('rel-with-deb-info.patch', when='@1.2.2')

    # intel/19.0.4 got an ICE (internal compiler error) compiling pairs.cc
    patch('p_intel_ice.patch', when='@1.2.2')

    variant('mpi', default=True, description='Support MPI')

    depends_on("cmake@3.1:", type='build')
    depends_on('mpi', when='+mpi')
    depends_on('lapack')
    depends_on('boost')

    def cmake_args(self):
        options = ['-DENABLE_UNIT_TESTS=ON', '-DENABLE_APP_TESTS=ON']

        if '+mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=ON',
                '-DENABLE_MPI_CXX_BINDINGS=ON',
                '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
                '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc,
            ])
        else:
            options.append('-DENABLE_MPI=OFF')

        options.append('-DBLA_VENDOR=' + self.spec['blas'].name.upper())
        options.append('-DBLAS_LIBRARIES=' + self.spec['blas'].libs.joined())
        options.append('-DLAPACK_LIBRARIES=' +
                       self.spec['lapack'].libs.joined())

        options.append("-DLAPACKE_LIBRARY=" +
                       self.spec["lapack:c"].libs.joined(";"))

        return options
