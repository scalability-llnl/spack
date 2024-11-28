# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sniffles(CMakePackage):
    """Structural variation caller using third generation sequencing."""

    homepage = "https://github.com/fritzsedlazeck/Sniffles/wiki"
    url = "https://github.com/fritzsedlazeck/Sniffles/archive/v1.0.5.tar.gz"

    license("MIT")

    version("1.0.7", sha256="03fa703873bdf9c32055c584448e1eece45f94b4bc68e60c9624cf3841e6d8a9")
    version("1.0.5", sha256="386c6536bdaa4637579e235bac48444c08297337c490652d1e165accd34b258f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")
    depends_on("bamtools", type="link")

    patch("unused_libs.patch")

    def cmake_args(self):
        i = self.spec["bamtools"].prefix.include.bamtools
        return ["-DCMAKE_CXX_FLAGS=-I{0}".format(i)]

    # the build process doesn't actually install anything, do it by hand
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        src = "bin/sniffles-core-{0}".format(spec.version.dotted)
        binaries = ["sniffles", "sniffles-debug"]
        for b in binaries:
            install(join_path(src, b), join_path(prefix.bin, b))
