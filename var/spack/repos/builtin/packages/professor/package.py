# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Professor(Package):
    """Professor Monte-Carlo tuning package"""

    homepage = "https://professor.hepforge.org/"
    url = "https://professor.hepforge.org/downloads/?f=Professor-2.3.3.tar.gz"

    maintainers("mjk655")

    version("2.3.3", sha256="60c5ba00894c809e2c31018bccf22935a9e1f51c0184468efbdd5d27b211009f")

    depends_on("cxx", type="build")  # generated

    variant(
        "interactive",
        default=True,
        description="Install prof-I (Interactive parametrization explorer)",
    )

    depends_on("yoda")
    depends_on("eigen")
    depends_on("py-cython")
    depends_on("py-iminuit")
    depends_on("py-matplotlib")
    depends_on("py-matplotlib backend=wx", when="+interactive")
    depends_on("root")

    extends("python")

    def setup_build_environment(self, env):
        env.set("PROF_VERSION", self.spec.version)

    def install(self, spec, prefix):
        make()
        make("PREFIX={0}".format(prefix), "install")
        if self.spec.satisfies("~interactive"):
            os.remove(join_path(prefix.bin, "prof2-I"))
