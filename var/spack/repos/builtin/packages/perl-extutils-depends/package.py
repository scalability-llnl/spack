# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsDepends(PerlPackage):
    """Easily build XS extensions that depend on XS extensions"""

    homepage = "http://search.cpan.org/~xaoc/ExtUtils-Depends/lib/ExtUtils/Depends.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-Depends-0.405.tar.gz"

    version('0.405', sha256='8ad6401ad7559b03ceda1fe4b191c95f417bdec7c542a984761a4656715a8a2c')
