# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Qrupdate(MakefilePackage, SourceforgePackage):
    """qrupdate is a Fortran library for fast updates of QR and
    Cholesky decompositions."""

    homepage = "http://sourceforge.net/projects/qrupdate/"
    sourceforge_mirror_path = "qrupdate/qrupdate-1.1.2.tar.gz"

    version('1.1.2', sha256='e2a1c711dc8ebc418e21195833814cb2f84b878b90a2774365f0166402308e08')

    depends_on("blas")
    depends_on("lapack")

    def edit(self, spec, prefix):
        # BSD "install" does not understand GNU -D flag.
        # We will create the parent directory ourselves.
        makefile = FileFilter('src/Makefile')
        if (sys.platform == 'darwin'):
            makefile.filter('-D', '')
        return

    def install(self, spec, prefix):

        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        make_args = [
            'BLAS={0}'.format(lapack_blas.ld_flags),
            'LAPACK={0}'.format(lapack_blas.ld_flags)
        ]

        # If 64-bit BLAS is used:
        if (spec.satisfies('^openblas+ilp64') or
            spec.satisfies('^intel-mkl+ilp64') or
            spec.satisfies('^intel-parallel-studio+mkl+ilp64')):
            make_args.append('FFLAGS=-fdefault-integer-8')

        # Build static and dynamic libraries:
        make('lib', 'solib', *make_args)

        # "INSTALL" confuses "make install" on case-insensitive filesystems:
        if os.path.isfile("INSTALL"):
            os.remove("INSTALL")

        # Create lib folder:
        if (sys.platform == 'darwin'):
            mkdirp(prefix.lib)

        make("install", "PREFIX=%s" % prefix)

    @run_after('install')
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if (sys.platform == 'darwin'):
            fix_darwin_install_name(self.spec.prefix.lib)
