# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crmc(CMakePackage):
    """CRMC (Cosmic Ray Monte Carlo package). CRMC is a package providing
    a common interface to access the output from event generators used
    to model the secondary particle production in hadronic collisons."""

    homepage = "https://web.ikp.kit.edu/rulrich/crmc.html"
    # Original URL has non-recognized certificate + is password-protected
    # url = "https://devel-ik.fzk.de/wsvn/mc/crmc/tags/crmc.v1.7.0/?op=dl"
    url = "https://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/crmc.v1.7.0.tar.gz"

    version("2.0.1", sha256="c607733c7534b188c9aede9e18cd7d4eac4f0a37d6728c1f406c434f74aed743")
    # Version 1.7.0 has issues linking phojet, devs contacted but no response
    # version('1.7.0', sha256='59086f4e654d775a4f6c3974ae89bbfd995391c4677f266881604878b47563d1')
    version("1.6.0", sha256="ae2ba5aa2a483d20aa60bef35080f555b365715d1a8fae54b473c275813345c1")
    version("1.5.7", sha256="ec7456c08b60a40665e9ff31d6029e0151b0cdf2ca98bd09a8b570b1e33f6053")
    version("1.5.6", sha256="a546a9352dcbdb8a1df3d63530eacf16f8b64a190e224b72afd434f78388a8a0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("hepmc")
    depends_on("boost+filesystem+iostreams+system+program_options")
    depends_on("root")

    patch(
        "https://gitlab.cern.ch/sft/lcgcmake/-/raw/master/generators/patches/crmc-1.6.0.patch",
        sha256="af07d9abbf8883dfbf54959f0e971e1429c5a1c43a602afa25dc790ba9758f15",
        when="@1.6.0",
        level=0,
    )
    patch(
        "https://gitlab.cern.ch/sft/lcgcmake/-/raw/master/generators/patches/crmc-1.5.6.patch",
        sha256="fcf767b821cca404569d558f748acb83f692d5b4aca6fd6c8473fcf06c734cf6",
        when="@1.5.6:1.5.7",
        level=0,
    )

    def cmake_args(self):
        args = [
            "-D__PYTHIA__=ON",
            "-D__SIBYLL__=ON",
            "-D__PHOJET__=ON",
            "-D__DPMJET__=ON",
            "-D__QGSJETII04__=ON",
            "-DCMAKE_CXX_FLAGS=-std=c++" + self.spec["root"].variants["cxxstd"].value,
        ]
        if self.spec.satisfies("@1.6.0:"):
            args.append("-D__HIJING__=ON")
        if self.spec.satisfies("%gcc@9:") or self.spec.satisfies("%clang@13:"):
            args.append("-DCMAKE_Fortran_FLAGS=-fallow-argument-mismatch")
        return args
