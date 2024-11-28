# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Starlight(CMakePackage):
    """STARlight is a Monte Carlo that simulates two-photon
    and photon-Pomeron interactions between relativistic nuclei and protons."""

    homepage = "https://starlight.hepforge.org"
    url = "https://starlight.hepforge.org/downloads?f=starlight_r313.tar"

    tags = ["hep"]

    maintainers("vvolkl")

    version(
        "313",
        sha256="afff1ac01bc312cb443931eb425808a85ac7e349ed3df228405a4ba87d780f23",
        url="https://starlight.hepforge.org/downloads?f=starlight_r313.tar",
    )
    version(
        "300",
        sha256="e754212f173fb42a96611b3519cb386c772429e690f3e088396bd103c2cf9348",
        url="https://starlight.hepforge.org/downloads?f=starlight_r300.tar",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch(
        "https://gitlab.cern.ch/sft/lcgcmake/-/raw/master/generators/patches/starlight-r313.patch",
        sha256="c70f70fd7c96dc0417f9254d25b584222abcb2c452e1e6dd4b8cfb0b64bf10e0",
        when="@300:",
        level=0,
    )
