# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Cli11(CMakePackage):
    """CLI11 is a command line parser for C++11 and beyond that provides a rich
    feature set with a simple and intuitive interface."""

    homepage = "https://cliutils.github.io/CLI11/book/"
    url      = "https://github.com/CLIUtils/CLI11/archive/v1.9.1.tar.gz"
    maintainers = ['nightlark']

    version('1.9.1', sha256='c780cf8cf3ba5ec2648a7eeb20a47e274493258f38a9b417628e0576f473a50b')

    depends_on('cmake@3.4:', type='build')

    def cmake_args(self):
        args = [
            '-DCLI11_BUILD_DOCS=OFF',
            '-DCLI11_BUILD_TESTS=OFF',
        ]
        return args
