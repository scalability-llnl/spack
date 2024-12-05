# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Casper(MakefilePackage):
    """CASPER (Context-Aware Scheme for Paired-End Read) is state-of-the art
    merging tool in terms of accuracy and robustness. Using this
    sophisticated merging method, we could get elongated reads from the
    forward and reverse reads."""

    homepage = "http://best.snu.ac.kr/casper/index.php?name=main"
    url = "http://best.snu.ac.kr/casper/program/casper_v0.8.2.tar.gz"
    git = "https://github.com/skwonPNU/casper.git"

    version("20220916", commit="08655cad5af7e801f05fdb9e643dcd859f823cba")
    version(
        "0.8.2",
        sha256="3005e165cebf8ce4e12815b7660a833e0733441b5c7e5ecbfdccef7414b0c914",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("jellyfish@2.2.3:")
    depends_on("boost+exception")

    conflicts("%gcc@7.1.0")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("@:0.8.2") and name.lower() == "cxxflags":
            flags.append(self.compiler.cxx98_flag)
        return (flags, None, None)

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec.prefix)
