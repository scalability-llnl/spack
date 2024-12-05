# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlRegexp(PerlPackage):
    """This package contains regular expressions for the following XML tokens:
    BaseChar, Ideographic, Letter, Digit, Extender, CombiningChar,
    NameChar, EntityRef, CharRef, Reference, Name, NmToken, and
    AttValue."""

    homepage = "https://metacpan.org/pod/XML::RegExp"
    url = "https://cpan.metacpan.org/authors/id/T/TJ/TJMATHER/XML-RegExp-0.04.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.04", sha256="df1990096036085c8e2d45904fe180f82bfed40f1a7e05243f334ea10090fc54")
