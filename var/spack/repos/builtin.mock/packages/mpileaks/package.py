# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version(1.0, 'foobarbaz')
    version(2.1, 'foobarbaz')
    version(2.2, 'foobarbaz')
    version(2.3, 'foobarbaz')

    variant('debug', default=False, description='Debug variant')
    variant('opt',   default=False, description='Optimized variant')
    variant('shared', default=True, description='Build shared library')
    variant('static', default=True, description='Build static library')

    depends_on("mpi")
    depends_on("callpath")

    # Will be used to try raising an exception
    libs = None

    def install(self, spec, prefix):
        touch(prefix.mpileaks)

    def setup_environment(self, senv, renv):
        renv.set('FOOBAR', self.name)
