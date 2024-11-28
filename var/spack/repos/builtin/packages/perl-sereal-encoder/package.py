# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSerealEncoder(PerlPackage):
    """Fast, compact, powerful binary serialization"""

    homepage = "https://metacpan.org/pod/Sereal::Encoder"
    url = "https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Encoder-5.004.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("5.004", sha256="5e5a86ccd32dae34ed80932ecbe5c68e29752b5de0e9b0a793ab7eb2ca55cb1b")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-devel-checklib@1.16:", type=("build"))
    depends_on("perl-sereal-decoder@5.004:", type=("build", "link", "run", "test"))
    depends_on("perl-test-deep", type=("build", "link", "test"))
    depends_on("perl-test-differences", type=("build", "link", "test"))
    depends_on("perl-test-longstring", type=("build", "link", "test"))
    depends_on("perl-test-warn", type=("build", "link", "test"))
    depends_on("zstd", type=("build", "link", "run", "test"))

    def setup_build_environment(self, env):
        # These are not currently available in Spack
        env.set("SEREAL_USE_BUNDLED_CSNAPPY", "1")
        env.set("SEREAL_USE_BUNDLED_MINIZ", "1")
        env.set("USE_UNALIGNED", "1")
        env.set("USE_UNALIGNED", "1")
        env.set("NO_ASM", "0")
        env.set("ZSTD_DISABLE_ASM", "0")
