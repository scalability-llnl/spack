# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsDepends(PerlPackage):
    """Easily build XS extensions that depend on XS extensions"""

    homepage = "https://metacpan.org/pod/ExtUtils::Depends"
    url = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-Depends-0.405.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.8001", sha256="673c4387e7896c1a216099c1fbb3faaa7763d7f5f95a1a56a60a2a2906c131c5")
    version("0.405", sha256="8ad6401ad7559b03ceda1fe4b191c95f417bdec7c542a984761a4656715a8a2c")
