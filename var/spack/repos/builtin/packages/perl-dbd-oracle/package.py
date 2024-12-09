# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdOracle(PerlPackage):
    """Oracle database driver for the DBI module"""

    homepage = "https://metacpan.org/pod/DBD::Oracle"
    url = "https://cpan.metacpan.org/authors/id/Z/ZA/ZARQUON/DBD-Oracle-1.83.tar.gz"

    maintainers("EbiArnie")

    version("1.83", sha256="51fe9c158955fda0ca917a806863f0bc51068b533fbbc7423b3cc4ad595ed153")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-dbi@1.623:", type=("build", "run", "test"))
    depends_on("perl-test-nowarnings", type=("build", "link"))
    depends_on("oracle-instant-client", type=("build", "link", "run", "test"))

    def setup_build_environment(self, env):
        env.set("ORACLE_HOME", self.spec["oracle-instant-client"].prefix)
