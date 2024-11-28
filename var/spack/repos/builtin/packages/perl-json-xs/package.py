# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJsonXs(PerlPackage):
    """JSON serialising/deserialising, done correctly and fast"""

    homepage = "https://metacpan.org/pod/JSON::XS"
    url = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-4.03.tar.gz"

    maintainers("EbiArnie")

    version("4.03", sha256="515536f45f2fa1a7e88c8824533758d0121d267ab9cb453a1b5887c8a56b9068")

    depends_on("perl-canary-stability", type=("build"))
    depends_on("perl-common-sense", type=("build", "run", "test"))
    depends_on("perl-types-serialiser", type=("build", "run", "test"))

    def setup_build_environment(self, env):
        env.set("PERL_CANARY_STABILITY_NOPROMPT", "1")
