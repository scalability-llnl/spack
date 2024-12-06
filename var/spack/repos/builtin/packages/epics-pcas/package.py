# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EpicsPcas(MakefilePackage):
    """EPICS Portable Channel Access Server and Generic Data Descriptor
    C++ libraries, split off from EPICS Base 3.16.1 as a separate module
    for EPICS 7."""

    homepage = "https://github.com/epics-modules/pcas"
    url = "https://github.com/epics-modules/pcas/archive/refs/tags/v4.13.3.tar.gz"

    maintainers("glenn-horton-smith")

    version("4.13.3", sha256="5004e39339c8e592fcb9b4275c84143635c6e688c0fbe01f17dafe19850398a0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("epics-base", type=("build", "link", "run"))

    @property
    def install_targets(self):
        return ["INSTALL_LOCATION={0}".format(self.prefix), "install"]

    def edit(self, spec, prefix):
        with open("configure/RELEASE.local", "w") as release_file:
            release_file.write("EPICS_BASE = " + env["EPICS_BASE"] + "\n")

    def setup_run_environment(self, envmod):
        envmod.prepend_path("PATH", join_path(self.prefix.bin, env["EPICS_HOST_ARCH"]))
