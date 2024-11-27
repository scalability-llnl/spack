# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sctk(Package):
    """The NIST Scoring Toolkit (SCTK) is a collection of software tools
    designed to score benchmark test evaluations of Automatic Speech
    Recognition (ASR) Systems. The toolkit is currently used by NIST,
    benchmark test participants, and reserchers worldwide to as a
    common scoring engine."""

    homepage = "https://www.nist.gov/itl/iad/mig/tools"
    url = "https://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2"

    version(
        "2.4.10",
        sha256="9cef424ce3a899f83b9527dc6fa83badf1bb14151529a78580301dd248bd2bf9",
        url="https://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2",
    )
    version(
        "2.4.9",
        sha256="262c92cca47755539dfa28add6120aa3ec4983b44b51f053f601e601c064617c",
        url="https://www.openslr.org/resources/4/sctk-2.4.9-20141015-1634Z.tar.bz2",
    )
    version(
        "2.4.8",
        sha256="ca9c5164cd06439ff85e681bc94a02a67139c7111591c628667151d386a02d5b",
        url="https://www.openslr.org/resources/4/sctk-2.4.8-20130429-2145.tar.bz2",
    )
    version(
        "2.4.0",
        sha256="73886bf3b879882a132141967ffe6b365178a2226390d2212f51a63e5df066e2",
        url="https://www.openslr.org/resources/4/sctk-2.4.0-20091110-0958.tar.bz2",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        make("config")
        make("all")
        make("install")
        install_tree("bin", prefix.bin)
