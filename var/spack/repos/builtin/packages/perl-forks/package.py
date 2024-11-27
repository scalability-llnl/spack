# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlForks(PerlPackage):
    """The "forks" pragma allows a developer to use threads without having to
    have a threaded perl, or to even run 5.8.0 or higher."""

    homepage = "https://metacpan.org/pod/forks"
    url = "https://cpan.metacpan.org/authors/id/R/RY/RYBSKEJ/forks-0.36.tar.gz"

    version("0.36", sha256="61be24e44f4c6fea230e8354678beb5b7adcfefd909a47db8f0a251b0ab65993")

    depends_on("perl-acme-damn", type=("build", "run"))
    depends_on("perl-devel-symdump", type=("build", "run"))
    depends_on("perl-list-moreutils", type=("build", "run"))
    depends_on("perl-sys-sigaction", type=("build", "run"))

    def setup_build_environment(self, env):
        if "perl~threads" in self.spec:
            env.set("FORKS_SIMULATE_USEITHREADS", "1")
