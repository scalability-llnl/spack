# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.compiler import UnsupportedCompilerFlag


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

    maintainers = ["tgamblin", "alalazo"]

    version('master', branch='master', submodules=True)
    version('spack', commit='2a025667090d71b2c9dce60fe924feb6bde8f667', submodules=True)

    version('5.5.0', sha256='c9d7004a0caec61b636ad1c1960fbf339ef8fdee9719321fc1b6b210613a8499')
    version('5.4.1', sha256='ac6606388abfe2482167ce8fd4eb0737ef6abeeb35a9d3ac3016c6f715bfee02')
    version('5.4.0', sha256='e2de331ee0a6d254193aab5995338a621372517adcf91568092be8ac511c18f3')
    version('5.3.0', sha256='b0d406d2809352caef7fccf69e8864d55e81ee84f4888b0744894977f703f976')
    version('5.2.2', sha256='da1ef8142e75c5a6f23c9403b90d4f40b9f862969ba71e2aaee9a257d058bfcf')

    variant("docs", default=False, description="build documentation with Doxygen")
    variant("python", default=True, description="build with python bindings")

    depends_on('doxygen', type="build", when="+docs")
    depends_on('re2c@0.13:', type="build")
    depends_on('bison@2.5:', type="build")

    depends_on('python', type=("build", "link", "run"), when="+python")
    extends('python', when='+python')

    # Clingo 5.5.0 supports Python 3.6 or later and needs CFFI
    depends_on(
        'python@3.6.0:',
        type=('build', 'link', 'run'), when='@5.5.0: +python'
    )
    depends_on('py-cffi', type=('build', 'run'), when='@5.5.0: +python')

    patch('python38.patch', when="@5.3:5.4")

    def patch(self):
        # Doxygen is optional but can't be disabled with a -D, so patch
        # it out if it's really supposed to be disabled
        if '+docs' not in self.spec:
            filter_file(r'find_package\(Doxygen\)',
                        'message("Doxygen disabled for Spack build.")',
                        'clasp/CMakeLists.txt',
                        'clasp/libpotassco/CMakeLists.txt')

    @property
    def cmake_python_hints(self):
        """Return standard CMake defines to ensure that the
        current spec is the one found by CMake find_package(Python, ...)
        """
        python_spec = self.spec['python']
        include_dir = python_spec.package.get_python_inc()
        return [
            self.define('Python_EXECUTABLE', str(python_spec.command)),
            self.define('Python_INCLUDE_DIR', include_dir)
        ]

    @property
    def cmake_py_shared(self):
        return self.define('CLINGO_BUILD_PY_SHARED', 'ON')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError('clingo requires a C++14-compliant C++ compiler')

        args = [
            '-DCLINGO_REQUIRE_PYTHON=ON',
            '-DCLINGO_BUILD_WITH_PYTHON=ON',
            '-DPYCLINGO_USER_INSTALL=OFF',
            '-DPYCLINGO_USE_INSTALL_PREFIX=ON',
            '-DCLINGO_BUILD_WITH_LUA=OFF',
            self.cmake_py_shared
        ]
        if self.spec['cmake'].satisfies('@3.16.0:'):
            args += self.cmake_python_hints

        return args
