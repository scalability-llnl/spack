# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Feynhiggs(AutotoolsPackage):
    """FeynHiggs is a Fortran code for the (diagrammatic/EFT/hybrid) calculation
    of the masses, mixings and much more of the Higgs bosons in the MSSM
    with real/complex parameters at the highest level of accuracy."""

    homepage = "https://wwwth.mpp.mpg.de/members/heinemey/feynhiggs/cFeynHiggs.html"
    url = "https://lcgpackages.web.cern.ch/tarFiles/sources/MCGeneratorsTarFiles/FeynHiggs-2.18.1.tar.gz"

    maintainers("vvolkl")
    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("2.18.1", sha256="3aba89cac6397d7e1a8a9d9dcfeed9fb32eeeee98768b0c0c9f444c2cc125ab9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def configure_args(self):
        return ["FFLAGS=-fPIC", "CFLAGS=-fPIC"]
