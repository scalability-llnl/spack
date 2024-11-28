# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHttpMultipartparser(PerlPackage):
    """HTTP MultiPart Parser"""

    homepage = "https://metacpan.org/pod/HTTP::MultiPartParser"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHANSEN/HTTP-MultiPartParser-0.02.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.02", sha256="5eddda159f54d16f868e032440ac2b024e55aac48931871b62627f1a16d00b12")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-deep", type=("build", "link"))
