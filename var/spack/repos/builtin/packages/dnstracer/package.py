# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnstracer(Package):
    """Dnstracer determines where a given Domain Name Server gets
    its information from, and follows the chain of DNS servers back to
    the servers which know the data."""

    homepage = "https://github.com/Orc/dnstracer"
    git      = "https://github.com/Orc/dnstracer.git"

    version('master', branch='master')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        configure = Executable('./configure.sh')
        configure('--prefix={0}'.format(prefix))

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')
