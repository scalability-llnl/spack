# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jansson(CMakePackage):
    """Jansson is a C library for encoding, decoding and manipulating JSON
    data."""

    homepage = "https://www.digip.org/jansson/"
    url = "https://github.com/akheron/jansson/archive/v2.9.tar.gz"
    maintainers("ax3l")

    license("MIT")

    version("2.14", sha256="c739578bf6b764aa0752db9a2fdadcfe921c78f1228c7ec0bb47fa804c55d17b")
    version("2.13.1", sha256="f22901582138e3203959c9257cf83eba9929ac41d7be4a42557213a22ebcc7a0")
    version("2.13", sha256="beb47da10cb27668de3012cc193a1873a898ad5710a1126be9e6d3357beb5b30")
    version("2.12", sha256="76260d30e9bbd0ef392798525e8cd7fe59a6450c54ca6135672e3cd6a1642941")
    version("2.11", sha256="6ff0eab3a8baf64d21cae25f88a0311fb282006eb992080722a9099469c32881")
    version("2.10", sha256="b0a899f90ade82e42da0ecabc8af1fa296d69691e7c0786c4994fb79d4833ebb")
    version("2.9", sha256="952fa714b399e71c1c3aa020e32e899f290c82126ca4d0d14cff5d10af457656")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")

    def cmake_args(self):
        return [
            self.define_from_variant("JANSSON_BUILD_SHARED_LIBS", "shared"),
            self.define("JANSSON_BUILD_DOCS", False),
        ]
