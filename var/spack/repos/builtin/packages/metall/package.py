# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Metall(CMakePackage):
    """A Persistent Memory Allocator For Data-Centric Analytics"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"
    url      = "https://github.com/LLNL/metall/archive/v0.2.tar.gz"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('master', branch='master')
    version('develop', branch='develop')

    version('0.13', sha256='959d37d0a7e7e5b4d5e6c0334aaaeef1b463e855fa8e807042f662c993ed60b1')
    version('0.12', sha256='b757b354b355e866bd6d42da53b0160442f3b7f663a19ba113da1ffc1a76176e')
    version('0.11', sha256='7cfa6a7eaaeb7fd11ecfbe43a172a36c8cde200601d6cd3b309d7a0acf752f3c')
    version('0.10', sha256='58b4b5507d4db5baca315b1bed2b728981755d755b91ef63bd0b6dfaf320f46b')
    version('0.9', sha256='2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927')

    depends_on('cmake@3.10:', type='build')
    depends_on('boost@1.64:', type=('build', 'link'))
    # googletest is required only for test
    # 'make test' is executed if '--run-tests' or '--test=root' is specified
    depends_on('googletest', type=('test'))

    def cmake_args(self):
        if self.run_tests:
            args = ['-DBUILD_TEST=ON', '-DSKIP_DOWNLOAD_GTEST=ON']
            return args
        else:
            args = ['-DINSTALL_HEADER_ONLY=ON']
            return args

    # Set environmental variables for the build step
    # setup_environment() was replaced by setup_build_environment()?
    # (https://github.com/spack/spack/pull/11115)
    # This page has not been updated?
    # https://spack-tutorial.readthedocs.io/en/latest/tutorial_advanced_packaging.html
    def setup_build_environment(self, env):
        # Configure the directories for test
        if self.run_tests:
            env.set(
                'METALL_TEST_DIR',
                join_path(self.build_directory, 'build_test')
            )

    # 'spack load metall' sets METALL_ROOT environmental variable
    def setup_run_environment(self, env):
        env.set('METALL_ROOT', self.prefix)
