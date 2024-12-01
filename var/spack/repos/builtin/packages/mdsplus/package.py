# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mdsplus(AutotoolsPackage):
    """A set of software tools for data acquisition and storage and a
    methodology for management of complex scientific data."""

    homepage = "https://mdsplus.org"
    git = "https://github.com/MDSplus/mdsplus.git"

    maintainers("wmvanvliet")

    parallel = False

    license("BSD-2-Clause")

    version(
        "stable_release-7-96-17",
        tag="stable_release-7-96-17",
        commit="83928a157ee0a5875135aeee0996634ecb802523",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("java", default=True, description="Build java libraries and applications")
    variant("python", default=True, description="Install python module")

    # Autotools needed for building
    depends_on("autoconf", type="build")
    depends_on("autoconf-archive", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    # Libs needed for building and linking
    depends_on("libxml2")
    depends_on("readline")

    # GUI bindings
    depends_on("motif")

    # Language bindings
    depends_on("java", type=("build", "run"), when="+java")

    def configure_args(self):
        return self.enable_or_disable("java")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap")

    def setup_run_environment(self, env):
        env.set("MDSPLUS_DIR", self.prefix)
        if "+python" in self.spec:
            env.prepend_path("PYTHONPATH", "{0}/python".format(self.prefix))
