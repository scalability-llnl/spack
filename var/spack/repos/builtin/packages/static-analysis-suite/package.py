# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class StaticAnalysisSuite(CMakePackage):
    """SAS (Static Analysis Suite) is a powerful tool for running static
    analysis on C++ code."""

    homepage = "https://github.com/dpiparo/SAS"
    url      = "https://github.com/dpiparo/SAS/archive/0.1.3.tar.gz"

    version('0.2.0', sha256='a369e56f8edc61dbf59ae09dbb11d98bc05fd337c5e47e13af9c913bf7bfc538')
    version('0.1.4', sha256='9b2a3436efe3c8060ee4882f3ed37d848ee79a63d6055a71a23fad6409559f40')
    version('0.1.3', sha256='93c3194bb7d518c215e79436bfb43304683832b3cc66bfc838f6195ce4574943')

    depends_on('python@2.7:')
    depends_on('llvm@3.5:')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        args = [
            '-DLLVM_DEV_DIR=%s' % self.spec['llvm'].prefix
        ]
        return args
