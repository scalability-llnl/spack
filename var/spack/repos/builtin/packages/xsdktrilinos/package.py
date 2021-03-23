# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Xsdktrilinos(CMakePackage):
    """xSDKTrilinos contains the portions of Trilinos that depend on PETSc
    because they would cause a circular dependency if built as part of
    Trilinos.
    """
    homepage = "https://trilinos.org/"
    url      = "https://github.com/trilinos/xSDKTrilinos/archive/trilinos-release-12-8-1.tar.gz"
    git      = "https://github.com/trilinos/xSDKTrilinos.git"

    version('develop', tag='master')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('12.8.1', sha256='f545c0821743f23af3b48f242c66bbc4593e3804436336db4eb3bb08622ad794')
    version('12.6.4', sha256='a7664afeab37ccfcbb5aae0bb03cb73ca8e511e0fecc365b9ccd32ba208318e3')

    variant('hypre',  default=True, description='Compile with Hypre preconditioner')
    variant('petsc',  default=True, description='Compile with PETSc solvers')
    variant('shared', default=True, description='Enables the build of shared libraries')

    # MPI related dependencies
    depends_on('mpi')
    depends_on('hypre~internal-superlu', when='+hypre')
    depends_on('hypre@xsdk-0.2.0~internal-superlu', when='@xsdk-0.2.0+hypre')
    depends_on('hypre@develop~internal-superlu', when='@develop+hypre')
    depends_on('petsc@xsdk-0.2.0+mpi~complex', when='@xsdk-0.2.0+petsc')
    depends_on('petsc@main+mpi~complex', when='@develop+petsc')
    depends_on('trilinos@12.6.4', when='@12.6.4')
    depends_on('trilinos@12.8.1', when='@12.8.1')
    depends_on('trilinos@xsdk-0.2.0', when='@xsdk-0.2.0')
    depends_on('trilinos@develop', when='@develop')

    def url_for_version(self, version):
        url = "https://github.com/trilinos/xSDKTrilinos/archive/trilinos-release-{0}.tar.gz"
        return url.format(version.dashed)

    def cmake_args(self):
        spec = self.spec

        options = []

        mpi_bin = spec['mpi'].prefix.bin
        options.extend([
            '-DxSDKTrilinos_VERBOSE_CONFIGURE:BOOL=OFF',
            '-DxSDKTrilinos_ENABLE_TESTS:BOOL=ON',
            '-DxSDKTrilinos_ENABLE_EXAMPLES:BOOL=ON',
            '-DTrilinos_INSTALL_DIR=%s' % spec['trilinos'].prefix,
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DTPL_ENABLE_MPI:BOOL=ON',
            '-DMPI_BASE_DIR:PATH=%s' % spec['mpi'].prefix,
            '-DxSDKTrilinos_ENABLE_CXX11:BOOL=ON',
            '-DTPL_ENABLE_HYPRE:BOOL=%s' % (
                'ON' if '+hypre' in spec else 'OFF'),
            '-DTPL_ENABLE_PETSC:BOOL=%s' % (
                'ON' if '+petsc' in spec else 'OFF'),
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % self.prefix
        ])

        # Fortran lib
        if (spec.satisfies('%gcc') or
                spec.satisfies('%clang') or
                spec.satisfies('%apple-clang')):
            libgfortran = os.path.dirname(os.popen(
                '%s --print-file-name libgfortran.a' %
                join_path(mpi_bin, 'mpif90')).read())
            options.extend([
                '-DxSDKTrilinos_EXTRA_LINK_FLAGS:STRING=-L%s/ -lgfortran' % (
                    libgfortran),
                '-DxSDKTrilinos_ENABLE_Fortran=ON'
            ])

        return options
