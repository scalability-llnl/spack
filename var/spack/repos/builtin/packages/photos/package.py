# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Photos(AutotoolsPackage):
    """Photos is a Monte Carlo program for bremsstrahlung in the decay
    of particles and resonances."""

    homepage = "https://photospp.web.cern.ch/photospp/"
    url = "https://photospp.web.cern.ch/photospp/resources/PHOTOS.3.61/PHOTOS.3.61-LHC.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-only")

    version("3.64", sha256="cb4096b4804289fc4d54a992caa566cbbd33f41f65f8906deb01200dc5163027")
    version("3.61", sha256="acd3bcb769ba2a3e263de399e9b89fd6296405c9cbc5045b83baba3e60db4b26")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hepmc", default=True, description="Build with HepMC2 support")
    variant("hepmc3", default=False, description="Build with HepMC3 support")

    maintainers("vvolkl")

    depends_on("hepmc", when="+hepmc")
    depends_on("hepmc3", when="+hepmc3")

    def configure_args(self):
        args = []

        args.extend(self.with_or_without("hepmc", "prefix"))
        args.extend(self.with_or_without("hepmc3", "prefix"))

        return args
