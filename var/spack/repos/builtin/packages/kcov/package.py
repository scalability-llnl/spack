# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kcov(CMakePackage):
    """Code coverage tool for compiled programs, Python and Bash which uses
    debugging information to collect and report data without special
    compilation options"""

    homepage = "http://simonkagstrom.github.io/kcov/index.html"
    url      = "https://github.com/SimonKagstrom/kcov/archive/38.tar.gz"

    version('38', sha256='b37af60d81a9b1e3b140f9473bdcb7975af12040feb24cc666f9bb2bb0be68b4')

    depends_on('cmake@2.8.4:', type='build')
    depends_on('zlib')
    depends_on('curl')
    depends_on('elfutils', when='platform=linux')
    depends_on('binutils +libiberty', when='platform=linux', type='link')

    def cmake_args(self):
        # Necessary at least on macOS, fixes linking error to LLDB
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/kcov.rb
        return ['-DSPECIFY_RPATH=ON']

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        # The help message exits with an exit code of 1
        kcov = Executable(self.prefix.bin.kcov)
        kcov('-h', ignore_errors=1)
