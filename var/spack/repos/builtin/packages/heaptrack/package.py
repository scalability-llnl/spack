# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Heaptrack(CMakePackage):
    """Heaptrack is a heap memory profiler that traces all memory allocations
    and annotates these events with stack traces.
    """

    homepage = "https://github.com/KDE/heaptrack"
    url      = "https://github.com/KDE/heaptrack/archive/v1.1.0.tar.gz"

    version('1.1.0', sha256='bd247ac67d1ecf023ec7e2a2888764bfc03e2f8b24876928ca6aa0cdb3a07309')

    depends_on('boost@1.41:')
    depends_on('cmake@2.8.9:', type='build')
    depends_on('elfutils')
    depends_on('libunwind')
    depends_on('zlib')
    depends_on('zstd')

    def cmake_args(self):

        spec = self.spec

        cmake_args = [
            "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
            "-DBOOST_LIBRARY_DIR={0}".format(spec['boost'].prefix.lib),
            "-DBOOST_INCLUDE_DIR={0}".format(spec['boost'].prefix.include),
            "-DBOOST_NO_SYSTEM_PATHS:BOOL=ON",
            "-DBoost_NO_BOOST_CMAKE:BOOL=ON",
        ]
        return cmake_args
