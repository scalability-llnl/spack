# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStreamBuffered(PerlPackage):
    """Temporary buffer to save bytes"""

    homepage = "https://metacpan.org/pod/Stream::Buffered"
    url = "https://cpan.metacpan.org/authors/id/D/DO/DOY/Stream-Buffered-0.03.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.03", sha256="9b2d4390b5de6b0cf4558e4ad04317a73c5e13dd19af29149c4e47c37fb2423b")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
