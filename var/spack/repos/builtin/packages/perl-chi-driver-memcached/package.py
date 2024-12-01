# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlChiDriverMemcached(PerlPackage):
    """Use Memcached for cache storage"""

    homepage = "https://metacpan.org/pod/CHI::Driver::Memcached"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSWARTZ/CHI-Driver-Memcached-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="cff9857fbf3f83247b8fc3ab41bdbf141ea0afe23b45109ee0b415f6baadb3c6")

    depends_on("perl-chi@0.33:", type=("build", "run", "test"))
    depends_on("perl-moose@0.66:", type=("build", "run", "test"))
    depends_on("perl-test-class", type=("build", "test"))
