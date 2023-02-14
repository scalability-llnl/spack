# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack import *


class Fckit(CMakePackage):
    """A Fortran toolkit for interoperating Fortran with C/C++."""

    homepage = "https://software.ecmwf.int/wiki/display/fckit"
    git = "https://github.com/ecmwf/fckit.git"
    url = "https://github.com/ecmwf/fckit/archive/0.9.0.tar.gz"

    maintainers = ['rhoneyager', 'climbfuji']

    version('master', branch='master')
    version('develop', branch='develop')
    version('0.9.5', commit='7ec9cf8ad8b619a8319199e834171c11e111c888', preferred=True)
    version('0.9.4', commit='a83cfe6d4ed22c954548dd7c31e1fbad3cd2f908')
    version('0.9.3', commit='3f612e107682c61c0b6806ea3fc12e9509a90664')
    version('0.9.2', commit='26439f09a421b29d745f4c4810d7d40f2820f5ec')
    version('0.9.1', commit='0b2c04d29ff141d1963e21da2add2e70f01163ce')
    version('0.9.0', commit='9cd993a524264e079ae260dbc89faea599e270fc')
    version('0.8.0', commit='4cd749f1eeac64eece00adb50abd072ea14fa2b1')
    version('0.7.0', commit='5a9ad884c087ae4c188a5937acf078514519778f')

    depends_on('mpi')
    depends_on('python')
    depends_on('ecbuild', type=('build'))

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    variant('eckit', default=True)
    depends_on('eckit+mpi', when='+eckit')

    variant('openmp', default=True, description='Use OpenMP?')
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    variant('shared', default=True)
    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_ECKIT', 'eckit'),
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            "-DPYTHON_EXECUTABLE:FILEPATH=" + self.spec['python'].command.path,
            '-DFYPP_NO_LINE_NUMBERING=ON'
        ]

        if '~shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        if self.spec.satisfies('%intel') or self.spec.satisfies('%gcc'):
            cxxlib = 'stdc++'
        elif self.spec.satisfies('%clang') or self.spec.satisfies('%apple-clang'):
            cxxlib = 'c++'
        else:
            raise InstallError("C++ library not configured for compiler")
        args.append('-DECBUILD_CXX_IMPLICIT_LINK_LIBRARIES={}'.format(cxxlib))

        return args

    @when("+fismahigh")
    def patch(self):
        patterns = ["tools/install-*", "tools/github-sha*", ".travis.yml"]
        for pattern in patterns:
            for path in glob.glob(pattern):
                os.remove(path)
