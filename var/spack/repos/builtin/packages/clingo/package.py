# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clingo(CMakePackage):
    """Clingo: A grounder and solver for logic programs

       Clingo is part of the Potassco project for Answer Set
       Programming (ASP). ASP offers a simple and powerful modeling
       language to describe combinatorial problems as logic
       programs. The clingo system then takes such a logic program and
       computes answer sets representing solutions to the given
       problem."""

    homepage = "https://potassco.org/clingo/"
    url      = "https://github.com/potassco/clingo/archive/v5.2.2.tar.gz"
    git      = 'https://github.com/potassco/clingo.git'

    maintainers = ["tgamblin"]

    version('master', branch='master', submodules=True, preferred=True)
    version('spack', commit='2ab2e81bcb24f6070b7efce30a754d74ef52ee2d', submodules=True)

    version('5.4.0', sha256='e2de331ee0a6d254193aab5995338a621372517adcf91568092be8ac511c18f3')
    version('5.3.0', sha256='b0d406d2809352caef7fccf69e8864d55e81ee84f4888b0744894977f703f976')
    version('5.2.2', sha256='da1ef8142e75c5a6f23c9403b90d4f40b9f862969ba71e2aaee9a257d058bfcf')

    variant("docs", default=False, description="build documentation with Doxygen")
    variant("python", default=True, description="build with python bindings")
    variant("cxx11", default=False, description="build a C++11-compatible clingo")

    depends_on('doxygen', type="build", when="+docs")
    depends_on('re2c@0.13:', type="build")
    depends_on('bison@2.5:', type="build")

    depends_on('python+shared', type=("build", "link", "run"), when="+python")
    extends('python', when='+python')

    patch('python38.patch', when="@5.3:5.4^python@3.8:")
    patch('revert-python-abi-usage.patch', when="^python")

    def patch(self):
        # Doxygen is optional but can't be disabled with a -D, so patch
        # it out if it's really supposed to be disabled
        if '+docs' not in self.spec:
            filter_file(r'find_package\(Doxygen\)',
                        'message("Doxygen disabled for Spack build.")',
                        'clasp/CMakeLists.txt',
                        'clasp/libpotassco/CMakeLists.txt')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag as e:
            raise InstallError(
                'clingo requires a C++14-compliant C++ compiler',
                long_msg=str(e))

        # Don't build with lua for *any* variant.
        base_args = [
            '-DCLINGO_BUILD_WITH_LUA=OFF',
        ]

        if '+python' in self.spec:
            python = self.spec['python']
            python_args = [
                '-DCLINGO_REQUIRE_PYTHON=ON',
                '-DCLINGO_BUILD_WITH_PYTHON=ON',
                '-DCLINGO_BUILD_PY_SHARED=ON',
                '-DPYCLINGO_USER_INSTALL=OFF',
                '-DPYCLINGO_USE_INSTALL_PREFIX=ON',
                '-DPYTHON_EXECUTABLE={0}'.format(python.command.path),
                '-DPYTHON_LIBRARY={0}'.format(python.libs.libraries[0]),
                '-DPYTHON_INCLUDE_DIR={0}'.format(
                    python.headers.directories[0]),
                '-DCLINGO_PYTHON_VERSION:LIST={0};EXACT'.format(
                    python.version.up_to(3)),
            ]
        else:
            python_args = []

        args = base_args + python_args

        return args
