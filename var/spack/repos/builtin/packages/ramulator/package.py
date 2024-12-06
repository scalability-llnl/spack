# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ramulator(MakefilePackage):
    """
    Ramulator is a fast and cycle-accurate DRAM simulator that supports
    a wide array of commercial, as well as academic, DRAM standards.
    """

    homepage = "https://github.com/CMU-SAFARI/ramulator"
    git = "https://github.com/CMU-SAFARI/ramulator"

    maintainers("jjwilke")

    license("MIT")

    version("sst", commit="7d2e72306c6079768e11a1867eb67b60cee34a1c")

    depends_on("cxx", type="build")  # generated

    patch("ramulator_sha_7d2e723_gcc48Patch.patch", when="@sst")
    patch("ramulator_sha_7d2e723_libPatch.patch", when="@sst")

    def patch(self):
        filter_file("-fpic", self.compiler.cxx_pic_flag, "Makefile")

    def build(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            make("libramulator.a")
        else:
            make("libramulator.so")

    def install(self, spec, prefix):
        install_tree(".", prefix)
