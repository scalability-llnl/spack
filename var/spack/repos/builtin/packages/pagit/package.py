# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pagit(Package):
    """PAGIT addresses the need for software to generate high quality draft
    genomes."""

    homepage = "https://www.sanger.ac.uk/science/tools/pagit"
    url = "ftp://ftp.sanger.ac.uk/pub/resources/software/pagit/PAGIT.V1.01.64bit.tgz"

    version("1.01", sha256="8069c1d236804cf4ea782495adcc50d18561ef466af06b21946b980b3c37ad55")

    depends_on("c", type="build")  # generated

    depends_on("java", type=("build", "run"))
    depends_on("perl", type=("build", "run"))

    def install(self, spec, prefix):
        with working_dir("PAGIT"):
            install_tree("ABACAS", prefix.ABACAS)
            install_tree("bin", prefix.bin)
            install_tree("ICORN", prefix.ICORN)
            install_tree("IMAGE", prefix.IMAGE)
            install_tree("lib", prefix.lib)
            install_tree("RATT", prefix.RATT)

    def setup_run_environment(self, env):
        env.set("PAGIT_HOME", self.prefix)
        env.set("PILEUP_HOME", join_path(self.prefix.bin, "pileup_v0.5"))
        env.set("ICORN_HOME", self.prefix.icorn)
        env.set("SNPOMATIC_HOME", self.prefix.bin)
        env.set("RATT_HOME", self.prefix.RATT)
        env.set("RATT_CONFIG", join_path(self.prefix.RATT, "RATT_config"))
        env.prepend_path("PATH", join_path(self.prefix.bin, "pileup_v0.5", "ssaha2"))
        env.prepend_path("PATH", join_path(self.prefix.bin, "pileup_v0.5"))
        env.prepend_path("PATH", self.prefix.IMAGE)
        env.prepend_path("PATH", self.prefix.ABACAS)
        env.prepend_path("PATH", self.prefix.ICORN)
        env.prepend_path("PATH", self.prefix.RATT)
        env.prepend_path("PERL5LIB", self.prefix.lib)
