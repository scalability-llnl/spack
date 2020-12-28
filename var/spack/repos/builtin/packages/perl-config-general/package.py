# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigGeneral(PerlPackage):
    """Config::General - Generic Config Module"""

    homepage = "https://metacpan.org/pod/Config::General"
    url      = "https://cpan.metacpan.org/authors/id/T/TL/TLINDEN/Config-General-2.63.tar.gz"

    version('2.63', sha256='0a9bf977b8aabe76343e88095d2296c8a422410fd2a05a1901f2b20e2e1f6fad')
