# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EpicsCaGateway(MakefilePackage):
    """The EPICS Channel Access PV Gateway is both a Channel Access
    server and Channel Access client. It provides a means for many
    clients to access a process variable, while making only one
    connection to the server that owns the process variable. It also
    provides additional access security beyond that on the server.
    The clients and the server may be on different subnets."""

    homepage = "https://epics.anl.gov/extensions/gateway/"
    url = "https://github.com/epics-extensions/ca-gateway/archive/refs/tags/v2.1.3.tar.gz"

    maintainers("glenn-horton-smith")

    version("2.1.3", sha256="f6e9dba46951a168d3208fc57054138759d56ebd8a7c07b496e8f5b8a56027d7")

    depends_on("cxx", type="build")  # generated

    depends_on("epics-base")
    depends_on("epics-pcas")

    @property
    def install_targets(self):
        return ["INSTALL_LOCATION={0}".format(self.prefix), "install"]

    def edit(self, spec, prefix):
        with open("configure/RELEASE.local", "w") as release_file:
            release_file.write("EPICS_BASE = " + env["EPICS_BASE"] + "\n")
            release_file.write("PCAS = " + spec["epics-pcas"].prefix)

    def setup_run_environment(self, envmod):
        envmod.prepend_path("PATH", join_path(self.prefix.bin, env["EPICS_HOST_ARCH"]))
