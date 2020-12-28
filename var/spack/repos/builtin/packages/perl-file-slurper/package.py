# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSlurper(PerlPackage):
    """A simple, sane and efficient module to slurp a file"""

    homepage = "http://search.cpan.org/~leont/File-Slurper/lib/File/Slurper.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/File-Slurper-0.011.tar.gz"

    version('0.011', sha256='f6494844b9759b3d1dd8fc4ffa790f8e6e493c4eb58e88831a51e085f2e76010')
