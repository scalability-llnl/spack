# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMimeTypes(PerlPackage):
    """Definition of MIME types"""

    homepage = "https://metacpan.org/pod/MIME::Types"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MARKOV/MIME-Types-2.24.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.24", sha256="629e361f22b220be50c2da7354e23c0451757709a03c25a22f3160edb94cb65f")
