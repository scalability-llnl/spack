# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Relax(CMakePackage):
    """A set of Reflex libraries for the most common used general data types in
    the LHC Computing Grid"""

    homepage = "https://twiki.cern.ch/twiki/bin/view/LCG/RELAX"
    url = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/RELAX-1.tar.gz"

    tags = ["hep"]

    version("root6", sha256="1d24b1a0884bbe99d60f7d02fea45d59695c158ab5e53516ac3fb780eb460bb4")

    depends_on("cxx", type="build")  # generated

    depends_on("clhep")
    depends_on("gsl")
    depends_on("hepmc@:2")
    depends_on("root@6.0.0:")

    def cmake_args(self):
        spec = self.spec
        cxxstd = self.spec["root"].variants["cxxstd"].value
        hepmc_lib = spec["hepmc"].prefix.lib.join("libHepMC.so")

        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DROOT_BINARY_PATH={0}".format(spec["root"].prefix.bin),
            "-DHEPMC_INCLUDE_DIR={0}".format(spec["hepmc"].prefix.include),
            "-DHEPMC_LIBRARIES={0}".format(hepmc_lib),
        ]

        return args
