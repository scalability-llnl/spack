# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailMimeEncodings(PerlPackage):
    """A unified interface to MIME encoding and decoding"""

    homepage = "https://metacpan.org/pod/Email::MIME::Encodings"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-MIME-Encodings-1.317.tar.gz"

    maintainers("EbiArnie")

    version("1.317", sha256="4a9a41671a9d1504c4da241be419a9503fa3486262526edb81eca9e2ebea0baf")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
