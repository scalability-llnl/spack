# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlFilterBuffertext(PerlPackage):
    """This is a very simple filter. One common cause of grief (and programmer
    error) is that XML parsers aren't required to provide character events in
    one chunk. They can, but are not forced to, and most don't. This filter
    does the trivial but oft-repeated task of putting all characters into a
    single event."""

    homepage = "https://metacpan.org/pod/XML::Filter::BufferText"
    url = "https://cpan.metacpan.org/authors/id/R/RB/RBERJON/XML-Filter-BufferText-1.01.tar.gz"

    version("1.01", sha256="8fd2126d3beec554df852919f4739e689202cbba6a17506e9b66ea165841a75c")
