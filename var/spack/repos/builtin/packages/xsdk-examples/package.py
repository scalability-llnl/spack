# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class XsdkExamples(CMakePackage):
    """xSDK Examples show usage of libraries in the xSDK package."""

    homepage = 'http://xsdk.info'
    url      = 'https://github.com/xsdk-project/xsdk-examples/archive/v0.1.0.tar.gz'
    git      = "https://github.com/xsdk-project/xsdk-examples"

    maintainers = ['acfisher', 'balay', 'balos1', 'luszczek']

    version('develop', branch='master')
    version('0.2.0', sha256='cf26e3a16a83eba6fb297fb106b0934046f17cf978f96243b44d9d17ad186db6')
    version('0.1.0', sha256='d24cab1db7c0872b6474d69e598df9c8e25d254d09c425fb0a6a8d6469b8018f')

    variant('cuda', default=False, description='Compile CUDA examples')

    depends_on('xsdk+cuda', when='+cuda')
    depends_on('xsdk@0.6.0', when='@0.2.0')
    depends_on('xsdk@0.5.0', when='@0.1.0')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DMETIS_INCLUDE_DIRS=%s' % spec['metis'].prefix.include,
            '-DMETIS_LIBRARY=%s' % spec['metis'].libs,
            '-DMPI_DIR=%s' % spec['mpi'].prefix,
            '-DSUNDIALS_DIR=%s'      % spec['sundials'].prefix,
            '-DHYPRE_DIR=%s'         % spec['hypre'].prefix,
            '-DHYPRE_INCLUDE_DIR=%s' % spec['hypre'].prefix.include,
            '-DPETSC_DIR=%s'         % spec['petsc'].prefix,
            '-DPETSC_INCLUDE_DIR=%s' % spec['petsc'].prefix.include,
            '-DPETSC_LIBRARY_DIR=%s' % spec['petsc'].prefix.lib,
            '-DSUPERLUDIST_DIR=%s' % spec['superlu-dist'].prefix,
            '-DSUPERLUDIST_INCLUDE_DIR=%s' %
            spec['superlu-dist'].prefix.include,
            '-DSUPERLUDIST_LIBRARY_DIR=%s' % spec['superlu-dist'].prefix.lib,
            '-DSUPERLUDIST_LIBRARY=%s' % spec['superlu-dist'].libs,
            '-DMFEM_DIR=%s' % spec['mfem'].prefix,
            '-DMFEM_INCLUDE_DIR=%s' % spec['mfem'].prefix.include,
            '-DMFEM_LIBRARY_DIR=%s' % spec['mfem'].prefix.include.lib,
            '-DGINKGO_DIR=%s' % spec['ginkgo'].prefix,
            '-DGINKGO_INCLUDE_DIR=%s' % spec['ginkgo'].prefix.include,
            '-DGINKGO_LIBRARY_DIR=%s' % spec['ginkgo'].prefix.include.lib,
            # allow use of default `find_package(Ginkgo)`
            '-DCMAKE_PREFIX_PATH=%s/cmake' % spec['ginkgo'].prefix.include.lib
        ]
        if '+cuda' in spec:
            args.extend([
                '-DENABLE_CUDA=ON'
            ])
        if 'trilinos' in spec:  # if trilinos variant was activated for xsdk
            args.extend([
                '-DTRILINOS_DIR_PATH=%s' % spec['trilinos'].prefix,
            ])
        if 'zlib' in spec:  # if zlib variant was activated for MFEM
            args.extend([
                '-DZLIB_LIBRARY_DIR=%s' % spec['zlib'].prefix.lib,
            ])
        return args
