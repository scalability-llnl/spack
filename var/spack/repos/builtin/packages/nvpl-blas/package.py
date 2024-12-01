# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplBlas(Package):
    """
    NVPL BLAS (NVIDIA Performance Libraries BLAS) is part of NVIDIA Performance Libraries
    that provides standard Fortran 77 BLAS APIs as well as C (CBLAS).
    """

    homepage = "https://docs.nvidia.com/nvpl/_static/blas/index.html"
    url = (
        "https://developer.download.nvidia.com/compute/nvpl/redist"
        "/nvpl_blas/linux-sbsa/nvpl_blas-linux-sbsa-0.1.0-archive.tar.xz"
    )

    maintainers("albestro", "rasolca")

    license("UNKNOWN")

    version("0.3.0", sha256="b51cb199a440c1e8673d3d845d395950c9a9020d4e83af2655eb96c23c6ec90d")
    version("0.2.0.1", sha256="ba29f6a9d3831b6ae5c9265b4d124c13b9b9e0faea025359b02b41ad230975c2")
    version("0.1.0", sha256="4ccc894593cbcbfaa1a4f3c54505982691971667acf191c9ab0f4252a37c8063")

    provides("blas")

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    conflicts("threads=openmp", when="%clang")

    def url_for_version(self, version):
        url = "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_blas/linux-sbsa/nvpl_blas-linux-sbsa-{0}-archive.tar.xz"
        return url.format(version)

    @property
    def blas_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def blas_libs(self):
        spec = self.spec

        if "+ilp64" in spec:
            int_type = "ilp64"
        else:
            int_type = "lp64"

        if spec.satisfies("threads=openmp"):
            threading_type = "gomp"
        else:
            # threads=none
            threading_type = "seq"

        name = ["libnvpl_blas_core", f"libnvpl_blas_{int_type}_{threading_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
