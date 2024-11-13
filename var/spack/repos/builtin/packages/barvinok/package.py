# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Barvinok(AutotoolsPackage):
    """barvinok is a library for counting the number of integer points in parametric and
    non-parametric polytopes."""

    maintainers("vmiheer")
    homepage = "https://barvinok.gforge.inria.fr"
    url = "http://barvinok.gforge.inria.fr/barvinok-0.41.5.tar.bz2"

    version("0.41.5", sha256="e70493318fe76c0c202f98d7861bdf5dda8c4d79c21024af2e04b009ffa79734")
    variant(
        "pet",
        default=False,
        description="Enable pet support (Generate polyhedral model from c code)",
    )

    depends_on("gmp")
    depends_on("ntl")
    depends_on("llvm +clang", when="+pet")
    depends_on("libyaml", when="+pet")

    def setup_build_environment(self, env):
        env.set("CFLAGS", "-pthread")

    def configure_args(self):
        spec = self.spec
        args = ["--with-gmp-prefix={0}".format(self.spec["gmp"].prefix)]

        if spec.satisfies("+pet"):
            args.append("--with-pet=bundled")
        return args
