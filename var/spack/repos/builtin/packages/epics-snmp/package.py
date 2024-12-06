# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EpicsSnmp(MakefilePackage):
    """This module provides EPICS device-layer support for hardware
    devices that communicate via SNMP (Simple Network Management
    Protocol)."""

    homepage = "https://groups.nscl.msu.edu/controls/files/devSnmp.html"
    url = "https://groups.nscl.msu.edu/controls/files/epics-snmp-1.1.0.3.zip"

    maintainers("glenn-horton-smith")

    version("1.1.0.3", sha256="fe8b2cb25412555a639e3513f48a4da4c4cc3cc43425176349338be27b1e26d3")

    depends_on("epics-base")
    depends_on("net-snmp")

    @property
    def install_targets(self):
        return ["INSTALL_LOCATION={0}".format(self.prefix), "install"]

    def edit(self, spec, prefix):
        config_release = FileFilter(
            "configure/RELEASE", "NventSGP/configure/RELEASE", "WienerCrate/configure/RELEASE"
        )
        config_release.filter("EPICS_BASE *=.*", "EPICS_BASE = " + env["EPICS_BASE"])
        makefile = FileFilter("snmpApp/src/Makefile")
        makefile.filter("USR_CPPFLAGS", "USR_CPPFLAGS += `net-snmp-config --cflags`\nUSR_CPPFLAGS")

    def setup_run_environment(self, envmod):
        envmod.prepend_path("PATH", join_path(self.prefix.bin, env["EPICS_HOST_ARCH"]))
