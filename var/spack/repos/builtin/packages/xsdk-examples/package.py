# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class XsdkExamples(CMakePackage):
    """xSDK Examples show usage of libraries in the xSDK package."""

    homepage = 'http://xsdk.info'
    url      = 'https://github.com/xsdk-project/xsdk-examples/archive/v0.1.0.tar.gz'

    maintainers = ['acfisher', 'balay', 'balos1', 'luszczek']

    version('0.1.0', sha256='d24cab1db7c0872b6474d69e598df9c8e25d254d09c425fb0a6a8d6469b8018f')

    depends_on('xsdk@0.5.0', when='@0.1.0')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DMPI_DIR=%s' % spec['mpi'].prefix,
            '-DSUNDIALS_DIR=%s'     % spec['sundials'].prefix,
            '-DPETSC_DIR=%s'         % spec['petsc'].prefix,
            '-DPETSC_INCLUDE_DIR=%s' % spec['petsc'].prefix.include,
            '-DPETSC_LIBRARY_DIR=%s' % spec['petsc'].prefix.lib,
            '-DSUPERLUDIST_INCLUDE_DIR=%s' %
            spec['superlu-dist'].prefix.include,
            '-DSUPERLUDIST_LIBRARY_DIR=%s' % spec['superlu-dist'].prefix.lib,
        ]
        if 'trilinos' in spec:
            args.extend([
                '-DTRILINOS_DIR:PATH=%s' % spec['trilinos'].prefix,
            ])
        return args
