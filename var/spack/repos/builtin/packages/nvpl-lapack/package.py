# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplLapack(Package):
    """
    NVPL LAPACK (NVIDIA Performance Libraries LAPACK) is part of NVIDIA Performance Libraries
    that provides standard Fortran 90 LAPACK APIs.
    """

    homepage = "https://docs.nvidia.com/nvpl/_static/lapack/index.html"
    url = (
        "https://developer.download.nvidia.com/compute/nvpl/redist"
        "/nvpl_lapack/linux-sbsa/nvpl_lapack-linux-sbsa-0.2.0.1-archive.tar.xz"
    )

    maintainers("albestro", "rasolca")

    license("UNKNOWN")

    version("0.2.3.1", sha256="25927df133c5486fd71d5976c93917c96e62275a78dffc354bcaf1b022f56f8e")
    version("0.2.2.1", sha256="cdfbf69517a044e99e3e6231c8b2f4e845fd0de57775ccad6b4b0b4fe7e91e84")
    version("0.2.0.1", sha256="7054f775b18916ee662c94ad7682ace53debbe8ee36fa926000fe412961edb0b")

    provides("lapack")

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")

    threadings = ("openmp", "none")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=threadings,
        multi=False,
    )

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    # propagate variants for depends_on("nvpl-blas")
    depends_on("nvpl-blas +ilp64", when="+ilp64")
    depends_on("nvpl-blas ~ilp64", when="~ilp64")
    for threads in threadings:
        depends_on(f"nvpl-blas threads={threads}", when=f"threads={threads}")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    conflicts("threads=openmp", when="%clang")

    def url_for_version(self, version):
        url = "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_lapack/linux-sbsa/nvpl_lapack-linux-sbsa-{0}-archive.tar.xz"
        return url.format(version)

    @property
    def lapack_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def lapack_libs(self):
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

        name = ["libnvpl_lapack_core", f"libnvpl_lapack_{int_type}_{threading_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
