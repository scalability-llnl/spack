# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Popt(AutotoolsPackage):
    """The popt library parses command line options."""

    homepage = "https://launchpad.net/popt"
    url      = "https://launchpad.net/popt/head/1.16/+download/popt-1.16.tar.gz"

    version('1.16', sha256='e728ed296fe9f069a0e005003c3d6b2dde3d9cad453422a10d6558616d304cc8')

    depends_on('iconv')

    def patch(self):
        # Remove flags not recognized by the NVIDIA compilers
        if self.spec.satisfies('%nvhpc@:20.11'):
            filter_file('CFLAGS="$CFLAGS -Wall -W"',
                        'CFLAGS="$CFLAGS -Wall"', 'configure', string=True)
