# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlQuote(PerlPackage):
    """This module provides functions to quote/dequote strings in "xml"-way.

    All functions are written in XS and are very fast; they correctly process
    utf8, tied, overloaded variables and all the rest of perl "magic"."""

    homepage = "https://metacpan.org/pod/XML::Quote"
    url = "https://cpan.metacpan.org/authors/id/G/GD/GDSL/XML-Quote-1.02.tar.gz"

    version("1.02", sha256="4705b86a8dcc002bffc6ff154ec5c55f0bfb6e99a3f744d1e77ae6541c6af228")
