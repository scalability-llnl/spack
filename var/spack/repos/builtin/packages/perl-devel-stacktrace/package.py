# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelStacktrace(PerlPackage):
    """An object representing a stack trace."""

    homepage = "http://search.cpan.org/~drolsky/Devel-StackTrace-2.02/lib/Devel/StackTrace.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Devel-StackTrace-2.02.tar.gz"

    version('2.02', sha256='cbbd96db0ecf194ed140198090eaea0e327d9a378a4aa15f9a34b3138a91931f')
