# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAcmeDamn(PerlPackage):
    """Acme::Damn provides a single routine, damn(), which takes a blessed
    reference (a Perl object), and unblesses it, to return the original
    reference."""

    homepage = "https://metacpan.org/pod/Acme::Damn"
    url = "https://cpan.metacpan.org/authors/id/I/IB/IBB/Acme-Damn-0.08.tar.gz"

    version("0.08", sha256="310d2d03ff912dcd42e4d946174099f41fe3a2dd57a497d6bd65baf1759b7e0e")
