# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Professor(Package):
    """Professor Monte-Carlo tuning package"""

    homepage = "https://professor.hepforge.org/"
    url = "https://gitlab.com/hepcedar/professor/-/archive/professor-2.5.1/professor-professor-2.5.1.tar.gz"

    maintainers("mjk655")

    version("2.5.1", sha256="c49174d1e4117da13083928a57e9bd6a52be25b9ccadee620315742f8e6b9430")
    version("2.5.0", sha256="3b5791ff02e415fec9fd8ddd7e8e7e35977e1aec51efae39509cf4709dfd2252")
    version("2.4.2", sha256="469d9b92d078fd621ea2c67383de10457811a1348a64b08fb585fc3a3e1046c1")
    version("2.4.1", sha256="943199e8a45ae3c48c6d411f810b7ff8f0789db64a9149709e549678cff0b630")
    version("2.4.0", sha256="8488f12a87080571837809b364864ce4ef079398089b6ea071def30ae43941aa")
    version("2.3.4", sha256="a4e932170804c8da5ebb41e819d5b3b5484ccfd54b2dcf39e1a1c0ace50b19b7")
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
    depends_on("py-iminuit@2:", when="@2.4.0:")
    depends_on("py-matplotlib")
    depends_on("py-matplotlib backend=wx", when="+interactive")
    depends_on("root")
    depends_on("gmake", type="build")
    depends_on("py-pip", type="build", when="@2.3.4:")

    extends("python")

    def url_for_version(self, version):
        if self.spec.satisfies("@2.4:"):
            return f"https://gitlab.com/hepcedar/professor/-/archive/professor-{version}/professor-professor-{version}.tar.gz"
        else:
            return f"https://professor.hepforge.org/downloads/?f=Professor-{version}.tar.gz"

    def setup_build_environment(self, env):
        env.set("PROF_VERSION", self.spec.version)

    @run_before("install")
    def configure(self):                                           
        if self.spec.satisfies("@2.5.0:"):
            with working_dir(self.stage.source_path):
                Executable("./configure")(f"--prefix={self.prefix}", f"--with-eigen={self.spec['eigen'].prefix}")

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            make()
            make(f"PREFIX={prefix}", "install")
            if self.spec.satisfies("~interactive"):
                os.remove(join_path(prefix.bin, "prof2-I"))
