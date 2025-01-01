# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Professor(Package):
    """Professor Monte-Carlo tuning package"""

    homepage = "https://professor.hepforge.org/"
    url = "https://professor.hepforge.org/downloads/?f=Professor-2.3.3.tar.gz"

    maintainers("mjk655")

    version("2.5.0", sha256="19bfb4924d9f36a245ee1fa62cdd02a92b11f4ae3a13bdd068979155938c8079")
    # Note: version 2.4.2 tar ball name and content is different from other versions
    version("2.4.1", sha256="98efb19fa1590841dacd4f1e6c26e677cd419091bea69ef638c6111073732684")
    version("2.4.0", sha256="e6b28aa41d5df41d6c948056e7eaa7b47d3e4576f15d6bed8cafba8794e0e22e")
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
    depends_on("gmake", type="build")

    extends("python")

    def setup_build_environment(self, env):
        env.set("PROF_VERSION", self.spec.version)

    @when("@2.5.0:")
    def configure(self, spec, prefix):
        configure = Executable("configure")
        configure(f"--prefix={prefix}", f"--with-eigen={self.spec['eigen'].prefix}")

    def install(self, spec, prefix):
        make()
        make("PREFIX={0}".format(prefix), "install")
        if self.spec.satisfies("~interactive"):
            os.remove(join_path(prefix.bin, "prof2-I"))
