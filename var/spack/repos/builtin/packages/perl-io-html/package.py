# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoHtml(PerlPackage):
    """Open an HTML file with automatic charset detection."""

    homepage = "https://metacpan.org/pod/IO::HTML"
    url = "http://search.cpan.org/CPAN/authors/id/C/CJ/CJM/IO-HTML-1.001.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.004", sha256="c87b2df59463bbf2c39596773dfb5c03bde0f7e1051af339f963f58c1cbd8bf5")
    version("1.001", sha256="ea78d2d743794adc028bc9589538eb867174b4e165d7d8b5f63486e6b828e7e0")
