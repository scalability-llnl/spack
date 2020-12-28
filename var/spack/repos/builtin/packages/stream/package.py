# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stream(MakefilePackage):
    """The STREAM benchmark is a simple synthetic benchmark program that
    measures sustainable memory bandwidth (in MB/s) and the corresponding
    computation rate for simple vector kernels."""

    homepage = "https://www.cs.virginia.edu/stream/ref.html"
    git      = "https://github.com/jeffhammond/STREAM.git"

    version('5.10')

    variant('openmp', default=False, description='Build with OpenMP support')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

        # Use the Spack compiler wrappers
        makefile.filter('CC = .*', 'CC = cc')
        makefile.filter('FC = .*', 'FC = f77')

        cflags = '-O2'
        fflags = '-O2'
        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
            fflags += ' ' + self.compiler.openmp_flag

        # Set the appropriate flags for this compiler
        makefile.filter('CFLAGS = .*', 'CFLAGS = {0}'.format(cflags))
        makefile.filter('FFLAGS = .*', 'FFLAGS = {0}'.format(fflags))

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        install('stream_c.exe', prefix.bin)
        install('stream_f.exe', prefix.bin)
