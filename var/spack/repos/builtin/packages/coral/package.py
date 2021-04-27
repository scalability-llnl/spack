# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Coral(CMakePackage):
    """CORAL is an abstraction layer with an SQL-free API to access data stored
       using relational database technologies. It is used directly by
       experiment-specific applications and internally by COOL."""

    homepage = "https://coral-cool.docs.cern.ch/"
    git      = "https://gitlab.cern.ch/lcgcoral/coral.git"

    tags = ['hep']

    version('3.3.3', tag='CORAL_3_3_3')
    variant('binary_tag', default='auto')

    depends_on('ninja')
    depends_on('ccache')
    depends_on('boost')
    depends_on('cppunit')
    depends_on('expat')
    depends_on('frontier-client')
    depends_on('libaio')
    depends_on('mariadb')
    depends_on('python')
#    depends_on('qmtest')
    depends_on('xerces-c')
    depends_on('sqlite')
    depends_on('gperftools')
    depends_on('igprof')
    depends_on('libunwind')
    depends_on('valgrind')
    depends_on('oracle-instant-client')

    def determine_binary_tag(self):
        # As far as I can tell from reading the source code, `binary_tag`
        # can be almost arbitraryThe only real difference it makes is
        # disabling oracle dependency for non-x86 platforms
        if self.spec.variants['binary_tag'].value != 'auto':
            return self.spec.variants['binary_tag'].value

        binary_tag = str(self.spec.target.family) + \
            '-' + self.spec.os + \
            '-' + self.spec.compiler.name + str(self.spec.compiler.version.joined) + \
            ('-opt' if 'Rel' in self.spec.variants['build_type'].value else '-dbg')

        return binary_tag

    def cmake_args(self):
        args = ['-DBINARY_TAG=' + self.determine_binary_tag()]
        if self.spec['python'].version >= Version("3.0.0"):
            args.append('-DLCG_python3=on')

        return args
