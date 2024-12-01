# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dctz(CMakePackage):
    """DCTZ is a compressor based on FFTs"""

    homepage = "https://github.com/swson/DCTZ"
    url = "https://github.com/robertu94/DCTZ/archive/refs/tags/0.2.2.tar.gz"
    git = "https://github.com/robertu94/DCTZ"

    maintainers("robertu94")

    license("MIT", checked_by="robertu94")

    version("0.2.2", sha256="5d270199b93e81704292ad87787ce961b458865c6a60ef7da59d5073513f6cff")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", description="build a shared library", default=True)
    variant("libpressio", description="use libpressio support", default=True)

    depends_on("pkgconfig", type="build")
    depends_on("zlib")
    depends_on("fftw@3:")
    depends_on("libpressio@0.0.99:", when="+libpressio")
    depends_on("libstdcompat@0.0.21:", when="+libpressio")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("DCTZ_HAVE_LIBPRESSIO", "libpressio"),
        ]
        return args
