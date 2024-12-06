# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSereal(PerlPackage):
    """Fast, compact, powerful binary (de-)serialization"""

    homepage = "https://metacpan.org/pod/Sereal"
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-5.004.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("5.004", sha256="9c25bb7ae4bd736d24b1ad1d93d77395b0c65ca8741e266bfc0cbe542261d76f")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-sereal-decoder@5.004:", type=("build", "run", "test"))
    depends_on("perl-sereal-encoder@5.004:", type=("build", "run", "test"))
    depends_on("perl-test-deep", type=("build", "test"))
    depends_on("perl-test-differences", type=("build", "test"))
    depends_on("perl-test-longstring", type=("build", "test"))
    depends_on("perl-test-warn", type=("build", "test"))
