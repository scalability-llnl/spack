# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vvtest(Package):
    """Vvtest is a test harness originally authored by Richard Drake for the
    Alegra-Emphasis project, written in pure Python, and designed for running
    verification, validation, and regression type tests. Being a stand-alone
    product, it can also be used by analysts to help manage sets of
    simulations, especially useful on batch platforms."""

    homepage = "https://github.com/rrdrake/vvtest"
    url = "https://github.com/rrdrake/vvtest/archive/1.0.0.tar.gz"
    git = "https://github.com/rrdrake/vvtest.git"
    maintainers("mrmundt", "rrdrake")

    license("Unlicense")

    version("1.2.0", sha256="d6b2432a2e6c43fb0d87ffc0eaa34a74d2268a732f7709ebdcf1344fbcaee154")
    version("1.1.0", sha256="674585f12d393ab9745a5ab26f59cb0f0e213f9c597b37467125979b5955ca79")
    version("1.0.0", sha256="acd04e8e6635ed1b1725b793e8287a58831d6380759a81159142a6ff3397a8dd")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6.0:3", type=("build", "run"))

    def install(self, spec, prefix):
        python = spec["python"].command
        python("install_vvtest", prefix.bin)
