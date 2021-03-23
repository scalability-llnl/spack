# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bmi(AutotoolsPackage):
    """a communications framework and network abstraction layer"""

    homepage = 'https://github.com/radix-io/bmi/'
    git = 'https://github.com/radix-io/bmi.git'

    maintainers = ['carns']

    version('main', branch='main')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    # need to override 'autoreconf' so we can run BMI's 'prepare' script
    def autoreconf(self, spec, prefix):
        Executable('./prepare')()

    def configure_args(self):
        args = ["--enable-shared", "--enable-bmi-only"]
        return args
