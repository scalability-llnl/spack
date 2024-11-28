# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlXmlLibxslt(PerlPackage):
    """Interface to the GNOME libxslt library."""

    homepage = "https://metacpan.org/pod/XML::LibXSLT"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXSLT-1.96.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.002001", sha256="df8927c4ff1949f62580d1c1e6f00f0cd56b53d3a957ee4b171b59bffa63b2c0")
    version("1.96", sha256="2a5e374edaa2e9f9d26b432265bfea9b4bb7a94c9fbfef9047b298fce844d473")

    depends_on("c", type="build")  # generated

    depends_on("libxslt")
    depends_on("perl-xml-libxml")
