# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAnyUriEscape(PerlPackage):
    """Load URI::Escape::XS preferentially over URI::Escape"""

    homepage = "https://metacpan.org/pod/Any::URI::Escape"
    url = "https://cpan.metacpan.org/authors/id/P/PH/PHRED/Any-URI-Escape-0.01.tar.gz"

    maintainers("EbiArnie")

    version("0.01", sha256="e3813cec9f108fa5c0be66e08c1986bfba4d242151b0f9f4ec5e0c5e17108c4c")

    depends_on("perl-uri", type=("run"))
