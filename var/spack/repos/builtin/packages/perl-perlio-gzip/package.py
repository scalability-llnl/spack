# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlioGzip(PerlPackage):
    """Perl extension to provide a PerlIO layer to gzip/gunzip"""

    homepage = "https://metacpan.org/pod/PerlIO::gzip"
    url = "http://search.cpan.org/CPAN/authors/id/N/NW/NWCLARK/PerlIO-gzip-0.19.tar.gz"

    version("0.20", sha256="4848679a3f201e3f3b0c5f6f9526e602af52923ffa471a2a3657db786bd3bdc5")
    version("0.19", sha256="d2e9351d58b8a93c86811e25a898ee651fc393a157413652bf42f9aada2eb284")

    depends_on("zlib-api", type="link")

    def configure_args(self):
        p = self.spec["zlib-api"].prefix.include
        return ["INC=-I{0}".format(p)]
