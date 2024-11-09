# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hepmc(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
    High Energy Physics Monte Carlo generators and simulation."""

    homepage = "https://hepmc.web.cern.ch/hepmc/"
    url = "https://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.11.tgz"

    tags = ["hep"]

    license("GPL-2.0-or-later")

    version("2.06.11", sha256="86b66ea0278f803cde5774de8bd187dd42c870367f1cbf6cdaec8dc7cf6afc10")
    version("2.06.10", sha256="5adedd9e3f7447e1e5fc01b72f745ab87da2c1611df89208bb3d7c6ea94c11a4")
    version("2.06.09", sha256="e0f8fddd38472c5615210894444686ac5d72df3be682f7d151b562b236d9b422")
    version("2.06.08", sha256="8be6c1793e0a045f07ddb88bb64b46de7e66a52e75fb72b3f82f9a3e3ba8a8ce")
    version("2.06.07", sha256="a0bdd6f36a3cc4cb59d6eb15cef9d46ce9b3739cae3324e81ebb2df6943e4594")
    version("2.06.06", sha256="8cdff26c10783ed4248220a84a43b7e1f9b59cc2c9a29bd634d024ca469db125")
    version("2.06.05", sha256="4c411077cc97522c03b74f973264b8d9fd2b6ccec0efc7ceced2645371c73618")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("length", default="MM", values=("CM", "MM"), multi=False, description="Unit of length")
    variant(
        "momentum",
        default="GEV",
        values=("GEV", "MEV"),
        multi=False,
        description="Unit of momentum",
    )

    depends_on("cmake@2.8.9:", type="build")

    def cmake_args(self):
        return [self.define_from_variant("momentum"), self.define_from_variant("length")]

    def url_for_version(self, version):
        if version <= Version("2.06.08"):
            url = "http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-{0}.tar.gz"
        else:
            url = "https://hepmc.web.cern.ch/hepmc/releases/hepmc{0}.tgz"
        return url.format(version)
