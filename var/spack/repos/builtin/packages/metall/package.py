# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.boost import Boost


class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"
    url      = "https://github.com/LLNL/metall/archive/v0.2.tar.gz"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('master', branch='master')
    version('develop', branch='develop')

    version('0.10', sha256='58b4b5507d4db5baca315b1bed2b728981755d755b91ef63bd0b6dfaf320f46b')
    version('0.9', sha256='2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927')

    depends_on('boost@1.64:', type=('build', 'link'))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=('build', 'link'))

    def cmake_args(self):
        args = []
        args.append('-DINSTALL_HEADER_ONLY=ON')
        return args

    def setup_run_environment(self, env):
        env.set('METALL_ROOT', self.prefix)
