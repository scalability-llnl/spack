# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"
    url      = "https://github.com/LLNL/metall/archive/v0.2.tar.gz"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('master', branch='master')
    version('develop', branch='develop')

    version('0.12', sha256='b757b354b355e866bd6d42da53b0160442f3b7f663a19ba113da1ffc1a76176e')
    version('0.11', sha256='7cfa6a7eaaeb7fd11ecfbe43a172a36c8cde200601d6cd3b309d7a0acf752f3c')
    version('0.10', sha256='58b4b5507d4db5baca315b1bed2b728981755d755b91ef63bd0b6dfaf320f46b')
    version('0.9', sha256='2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927')

    depends_on('cmake@3.10:', type='build')
    depends_on('boost@1.64:', type=('build', 'link'))

    def cmake_args(self):
        args = []
        args.append('-DINSTALL_HEADER_ONLY=ON')
        return args

    def setup_run_environment(self, env):
        env.set('METALL_ROOT', self.prefix)
