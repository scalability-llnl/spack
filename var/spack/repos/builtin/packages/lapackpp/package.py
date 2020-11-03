# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Lapackpp(CMakePackage):
    """LAPACK++: C++ API for the LAPACK Linear Algebra Package. Developed
       by the Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = "https://bitbucket.org/icl/lapackpp"
    git = homepage
    url = 'https://bitbucket.org/icl/lapackpp/downloads/lapackpp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('master', branch='master')
    version('2020.10.02', sha256='8dde9b95d75b494c4f8b893d68034e95b7a7541981359acb97b6c1c4a9c45cd9')
    version('2020.10.01', sha256='ecd659730b4c3cfb8d2595f9bbb6af65d96b79397db654f17fe045bdfea841c0')
    version('2020.10.00', sha256='5f6ab3bd3794711818a3a50198efd29571520bf455e13ffa8ba50fa8376d7d1a')

    variant('shared', default=True, description='Build shared library')

    # Needs to compile against a matching blaspp version
    depends_on('blaspp')
    for ver in ['master', '2020.10.02', '2020.10.01', '2020.10.00']:
        depends_on('blaspp@' + ver, when='@' + ver)
    depends_on('blas')
    depends_on('lapack')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            '-Dbuild_tests=%s'       % self.run_tests,
            '-DLAPACK_LIBRARIES=%s'  % spec['lapack'].libs.joined(';')
        ]

    def check(self):
        # If the tester fails to build, ensure that the check() fails.
        if os.path.isfile(join_path(self.build_directory, 'test', 'tester')):
            make('check')
        else:
            raise Exception('The tester was not built!')
