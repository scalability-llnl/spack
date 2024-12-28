# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRhdf5filters(RPackage):
    """HDF5 Compression Filters.

    Provides a collection of compression filters for use with HDF5 datasets."""

    bioc = "rhdf5filters"

    license("BSD-2-Clause")

    version("1.18.0", commit="1e07604afaa8a9482c35d059ba1e0fca8ea565c4")
    version("1.16.0", commit="1d29c0e77bd0ae14662e0dfc004c0dccd3149e3d")
    version("1.14.1", commit="2a2e71e8016592cc2d7b50d0faee4ac6dd1594ec")
    version("1.12.0", commit="4deabdef71c0349c4eaf7e5604cb7f389809f006")
    version("1.10.0", commit="6131538e2c5896dca0af33882bc2da961d79e49a")
    version("1.8.0", commit="b0b588b71a5595b30f4e698a50b84310dc19745d")
    version("1.6.0", commit="5f7f3a5b7dabd6e7d0c50cda70290e2472ff4f53")
    version("1.2.0", commit="25af0180f926b4b3ea11b30ec9277d26ad3d56b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r-rhdf5lib", type=("build", "run"))
    depends_on("gmake", type="build")
    depends_on("zlib-api")
    depends_on("zstd")

    def configure_args(self):
        args = []
        if self.spec.target.family == "aarch64":
            args.append("ax_cv_gcc_check_x86_cpu_init=yes")
            args.append("ax_cv_gcc_x86_cpu_supports_sse2=no")
        return args
