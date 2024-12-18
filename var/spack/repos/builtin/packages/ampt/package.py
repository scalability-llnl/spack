# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ampt(MakefilePackage):
    """A Multi-Phase Transport (AMPT) model is a Monte Carlo transport model for
    nuclear collisions at relativistic energies."""

    homepage = "https://myweb.ecu.edu/linz/ampt/"
    url = "https://myweb.ecu.edu/linz/ampt/ampt-v1.26t9b-v2.26t9b.zip"

    maintainers("vvolkl")

    tags = ["hep"]

    patch(
        "https://gitlab.cern.ch/sft/lcgcmake/-/raw/master/generators/patches/ampt-2.26t9b_atlas.patch",
        level=0,
        sha256="7a9a4f175f84dc3021301dae5d48adab1fc714fccf44ec17128a3ba1608bff4c",
        when="@2.26-t9b_atlas",
    )

    version(
        "2.26-t9b_atlas",
        sha256="9441b5f77c2ab91a57b291abd4afd12de7968f9cbe9f3cc8dbe60fbf5293ed55",
        url="http://myweb.ecu.edu/linz/ampt/ampt-v1.26t9b-v2.26t9b.zip",
    )
    version(
        "2.26-t9",
        sha256="9441b5f77c2ab91a57b291abd4afd12de7968f9cbe9f3cc8dbe60fbf5293ed55",
        url="http://myweb.ecu.edu/linz/ampt/ampt-v1.26t9b-v2.26t9b.zip",
    )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share.ampt)
        install("ampt", prefix.bin)
        install("input.ampt", prefix.share.ampt)
        install("readme", prefix.share.ampt)
