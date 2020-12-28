# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPegex(PerlPackage):
    """Acmeist PEG Parser Framework"""

    homepage = "http://search.cpan.org/~ingy/Pegex-0.64/lib/Pegex.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IN/INGY/Pegex-0.64.tar.gz"

    version('0.64', sha256='27e00264bdafb9c2109212b9654542032617fecf7b7814915d2bdac198f067cd')

    depends_on('perl-file-sharedir-install', type=('build', 'run'))
    depends_on('perl-yaml-libyaml', type=('build', 'run'))
