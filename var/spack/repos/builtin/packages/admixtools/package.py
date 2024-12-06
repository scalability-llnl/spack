# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Admixtools(MakefilePackage):
    """The ADMIXTOOLS package implements 5 methods described in
    Patterson et al. (2012) Ancient Admixture in Human History. Details
    of the methods and algorithm can be found in this paper.."""

    homepage = "https://github.com/DReichLab/AdmixTools"
    url = "https://github.com/DReichLab/AdmixTools/archive/v7.0.2.tar.gz"

    version("7.0.2", sha256="d1dc1963e01017f40e05e28009008e14388a14a3facc75cff46653da585bd91e")
    version("7.0.1", sha256="182dd6f55109e9a1569b47843b0d1aa89fe4cf4a05f9292519b9811faea67a20")
    version("7.0", sha256="c00faab626f02bbf9c25c6d2dcf661db225776e9ed61251f164e5edeb5a448e5")
    version("6.0", sha256="8fcd6c6834c7b33afdd7188516856d9c66b53c33dc82e133b72b56714fb67ad5")
    version("5.1", sha256="42b584cc785abfdfa9f39a341bdf81f800639737feaf3d07702de4a2e373557e")
    version("5.0", sha256="9f00637eac84c1ca152b65313d803616ee62c4156c7c737a33f5b31aeeac1367")
    version("1.0.1", sha256="ef3afff161e6a24c0857678373138edb1251c24d7b5308a07f10bdb0dedd44d0")
    version("1.0", sha256="cf0d6950285e801e8a99c2a0b3dbbbc941a78e867af1767b1d002ec3f5803c4b")

    depends_on("c", type="build")  # generated

    depends_on("lapack")
    depends_on("gsl")

    build_directory = "src"

    def edit(self, spec, prefix):
        makefile = FileFilter("src/Makefile")

        lapackflags = spec["lapack"].libs.ld_flags

        makefile.filter(
            "override LDLIBS += -lgsl -lopenblas -lm -lnick",
            "override LDLIBS += -lgsl -lm -lnick " + lapackflags,
        )

        makefile.filter("TOP=../bin", "TOP=./bin")

    def install(self, spec, prefix):
        with working_dir("src"):
            make("install")
            install_tree("bin", prefix.bin)
            install("twtable", prefix.bin)
