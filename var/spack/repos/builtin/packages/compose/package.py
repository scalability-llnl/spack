# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Compose(MakefilePackage):
    """CompOSE: CompStar Online Supernovae Equations of State

    The online service CompOSE provides data tables for different
    state of the art equations of state (EoS) ready for further usage
    in astrophysical applications, nuclear physics and beyond."""

    homepage = "https://compose.obspm.fr/home"
    url = "https://compose.obspm.fr/download/code/codehdf5.zip"
    maintainers("eschnett")

    # Spack must not modify our url which doesn't contain a version number
    def url_for_version(self, version):
        return "https://compose.obspm.fr/download/code/codehdf5.zip"

    # There is no version number for the zip file itself. This is the version
    # number output by the `compose` executable.
    version("2.17", sha256="f3f68203a50bb898abe31ee0b3dc750a1f1164c9e5d7fb9c4546b4eaa0cd172b")

    depends_on("hdf5 +fortran")

    parallel = False

    executables = ["compose", "test_read_hdf5", "test_read_opacity"]

    @property
    def build_targets(self):
        return self.executables

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        for f in self.executables:
            install(f, prefix.bin)
