# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoHtml(PerlPackage):
    """Open an HTML file with automatic charset detection."""

    homepage = "http://search.cpan.org/~cjm/IO-HTML-1.001/lib/IO/HTML.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CJ/CJM/IO-HTML-1.001.tar.gz"

    version('1.001', sha256='ea78d2d743794adc028bc9589538eb867174b4e165d7d8b5f63486e6b828e7e0')
