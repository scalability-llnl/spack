# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlXmlLibxslt(PerlPackage):
    """Interface to the GNOME libxslt library."""

    homepage = "https://metacpan.org/pod/XML::LibXSLT"
    url      = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXSLT-1.96.tar.gz"

    version('1.96', sha256='2a5e374edaa2e9f9d26b432265bfea9b4bb7a94c9fbfef9047b298fce844d473')

    depends_on('libxslt')
    depends_on('perl-xml-libxml')
