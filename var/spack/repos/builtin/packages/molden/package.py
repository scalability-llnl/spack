# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Molden(MakefilePackage):
    """A package for displaying Molecular Density from various
       Ab Initio packages"""

    homepage = "https://www3.cmbi.umcn.nl/molden/"
    url      = "ftp://ftp.cmbi.ru.nl/pub/molgraph/molden/molden6.5.tar.gz"

    maintainers = ['dev-zero']

    version('6.5', sha256='192631a0996b2bfa9f6b0769f83da38a9e4f83b1db9358982b23d6a594b4e8d4')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('gl@3:')
    depends_on('glu@1.3')
    depends_on('makedepend', type='build')

    parallel = False  # building in parallel is broken

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')

        # never register extensions
        makefile.filter(r'(\s*)EXTEN = .*', r'\1EXTEN =')

        # always Spacks wrappers:
        makefile.filter(r'(\s*)CC = .*', r'\1CC = cc')
        makefile.filter(r'(\s*)FC = .*', r'\1FC = f77')

        # make sure we don't link in system X11 libs:
        makefile.filter(
            r'(.+)-L/usr/(?:X11R6/lib|X11R6/lib64|lib/X11) (.*)',
            r'\1 \2')
        makefile.filter(
            r'(.+)-I/usr/(?:X11R6/include|include/X11) (.*)',
            r'\1 \2')

        # enable basic optimization flags, arch-specific is done via wrappers
        cflags = '-O2 -funroll-loops'
        fflags = cflags

        if '%gcc@10:' in self.spec:
            fflags += '-fallow-argument-mismatch'

        makefile.filter(r'CFLAGS = (.*)', r'CFLAGS = {0} \1'.format(cflags))
        makefile.filter(r'FFLAGS = (.*)', r'FFLAGS = {0} \1'.format(fflags))

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
