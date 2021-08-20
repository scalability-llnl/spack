# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Fpchecker(CMakePackage):
    """FPChecker (Floating-Point Checker) is a dynamic analysis tool to detect floating-point errors in HPC applications."""

    homepage = "https://fpchecker.org/"
    url      = "https://github.com/LLNL/FPChecker/archive/refs/tags/v0.3.0.tar.gz"

    maintainers = ['ilagunap']

    version('0.3.0', sha256='dc4f74b8104cbe0bd9f1a37c3dab1593d5d281658136ae880ec99668ec6b77e0')

    depends_on('llvm@12.0.1', type=('build', 'link'))
    depends_on('cmake@3.4:', type='build')
    depends_on('python@3:', type='run')

    def cmake_args(self):
        args = ['-DCMAKE_C_COMPILER=clang', '-DCMAKE_CXX_COMPILER=clang++']
        return args

