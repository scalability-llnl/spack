# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Mgis(CMakePackage):
    """
    The MFrontGenericInterfaceSupport project (MGIS) provides helper
    functions for various solvers to interact with behaviour written
    using MFront generic interface.

    MGIS is written in C++.
    Bindings are provided for C and fortran (2003).
    A FEniCS binding is also available.
    """

    homepage = "https://thelfer.github.io/mgis/web/index.html"
    url      = "https://github.com/thelfer/MFrontGenericInterfaceSupport/archive/MFrontGenericInterfaceSupport-1.2.tar.gz"
    git      = "https://github.com/thelfer/MFrontGenericInterfaceSupport.git"
    maintainers = ['thelfer']

    # development branches
    version("master", branch="master")
    version("rliv-1.2", branch="rliv-1.2")
    version("rliv-1.1", branch="rliv-1.1")
    version("rliv-1.0", branch="rliv-1.0")

    # released version
    version('1.2',   sha256='ed82ab91cbe17c00ef36578dbfcb4d1817d4c956619b7cccbea3e3f1a3b31940')
    version('1.1',   sha256='06593d7a052678deaee87ef60b2213db7545c5be9823f261d3388b3978a0b7a5')
    version('1.0.1', sha256='6102621455bc5d9b1591cd33e93b2e15a9572d2ce59ca6dfa30ba57ae1265c08')
    version('1.0', sha256='279c98da00fa6855edf29c2b8f8bad6e7732298dc62ef67d028d6bbeaac043b3')

    # variants
    variant('c', default=True,
            description='Enables c bindings')
    variant('fortran', default=True,
            description='Enables fortran bindings')
    variant('python', default=True,
            description='Enables python bindings')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    # dependencies
    depends_on('tfel@3.4.0', when="@1.2")
    depends_on('tfel@3.3.0', when="@1.1")
    depends_on('tfel@3.2.1', when="@1.0.1")
    depends_on('tfel@3.2.0', when="@1.0")
    depends_on('tfel@rliv-3.4', when="@rliv-1.2")
    depends_on('tfel@rliv-3.3', when="@rliv-1.1")
    depends_on('tfel@rliv-3.2', when="@rliv-1.0")
    depends_on('tfel@master', when="@master")
    depends_on('boost+python+numpy', when='+python')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='+python')
    extends('python', when='+python')

    def cmake_args(self):

        args = []

        args.append("-DUSE_EXTERNAL_COMPILER_FLAGS=ON")

        for i in ['c', 'fortran', 'python']:
            if '+' + i  in self.spec:
                args.append("-Denable-{0}-bindings=ON".format(i))
            else:
                args.append("-Denable-{0}-bindings=OFF".format(i))

        if '+python' in self.spec:
            # adding path to python
            python = self.spec['python']
            args.append('-DPYTHON_LIBRARY={0}'.
                        format(python.libs[0]))
            args.append('-DPYTHON_INCLUDE_DIR={0}'.
                        format(python.headers.directories[0]))
            args.append('-DPython_ADDITIONAL_VERSIONS={0}'.
                        format(python.version.up_to(2)))
            # adding path to boost
            args.append('-DBOOST_ROOT={0}'.
                        format(self.spec['boost'].prefix))

        return args
