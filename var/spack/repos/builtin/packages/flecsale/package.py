# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.boost import Boost


class Flecsale(CMakePackage):
    """Flecsale is an ALE code based on FleCSI"""

    homepage = "https://github.com/laristra/flecsale"
    git      = "https://github.com/laristra/flecsale.git"

    version('develop', branch='master', submodules=True)

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')

    depends_on("pkgconfig", type='build')
    depends_on("cmake@3.1:", type='build')
    depends_on("flecsi~mpi", when='~mpi')
    depends_on("flecsi+mpi", when='+mpi')
    depends_on("python")
    depends_on("openssl")
    depends_on("boost~mpi", when='~mpi')
    depends_on("boost+mpi", when='+mpi')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("exodusii~mpi", when='~mpi')
    depends_on("exodusii+mpi", when='+mpi')

    def cmake_args(self):
        options = [
            '-DENABLE_UNIT_TESTS=ON'
            '-DENABLE_OPENSSL=ON'
            '-DENABLE_PYTHON=ON'
        ]

        if '+mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=ON',
                '-DFLECSI_RUNTIME_MODEL=legion'
            ])

        return options
