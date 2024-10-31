# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zfp(CMakePackage, CudaPackage):
    """zfp is a compressed number format for multidimensional floating-point
    and integer arrays.

    zfp provides compressed-array classes that support high throughput
    read and write random access to individual array elements. zfp also
    supports serial and parallel (OpenMP and CUDA) compression of whole
    arrays.
    """

    # Package info
    homepage = "https://zfp.llnl.gov"
    url = "https://github.com/LLNL/zfp/releases/download/1.0.0/zfp-1.0.0.tar.gz"
    git = "https://github.com/LLNL/zfp.git"
    maintainers("lindstro", "GarrettDMorrison")
    tags = ["radiuss", "e4s"]

    license("BSD-3-Clause")

    # Versions
    version("develop", branch="develop")
    version("1.0.0", sha256="0ea08ae3e50e3c92f8b8cf41ba5b6e2de8892bc4a4ca0c59b8945b6c2ab617c4")
    version("0.5.5", sha256="fdf7b948bab1f4e5dccfe2c2048fd98c24e417ad8fb8a51ed3463d04147393c5")
    version("0.5.4", sha256="746e17aaa401c67dcffd273d6e6f95c76adfbbd5cf523dcad56d09e9d3b71196")
    version("0.5.3", sha256="a5d2f8e5b47a7c92e2a5775b82cbfb3a76c87d0ac83d25abb4ac10ea75a2856e")

    version(
        "0.5.2",
        sha256="9c738ec525cc76b4bb80b2b3f7c9f07507eeda3a341470e5942cda97efbe9a4f",
        url="https://github.com/LLNL/zfp/archive/0.5.2/zfp-0.5.2.tar.gz",
    )
    version(
        "0.5.1",
        sha256="f255dd1708c9ae4dc6a56dd2614e8b47a10d833c87fd349cbd47545a19c2b779",
        url="https://github.com/LLNL/zfp/archive/0.5.1/zfp-0.5.1.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Dependencies
    depends_on("cmake@3.9.0:", type="build")
    depends_on("cuda@7:", type=("build", "test", "run"), when="+cuda")
    depends_on("python", type=("build", "test", "run"), when="+python")
    depends_on("py-numpy", type=("build", "test", "run"), when="+python")
    depends_on("py-cython", type="build", when="+python")

    # Build targets
    variant("shared", default=True, description="Build shared libraries")
    variant("utilities", default=True, description="Build zfp utilities")

    # Language bindings
    variant("c", default=False, when="@0.5.4:", description="Enable compressed array C bindings")
    variant("python", default=False, when="@0.5.5:", description="Enable Python bindings")
    variant("fortran", default=False, when="@0.5.5:", description="Enable Fortran bindings")

    # Execution policies
    variant("openmp", default=False, when="@0.5.3:", description="Enable OpenMP execution")
    variant("cuda", default=False, when="@0.5.4:", description="Enable CUDA execution")

    # Advanced settings
    variant("aligned", default=False, description="Enable aligned memory allocation")

    variant(
        "bsws",
        default="64",
        values=("8", "16", "32", "64"),
        multi=False,
        description="Bit stream word size: "
        "use smaller for finer rate granularity. "
        "Use 8 for H5Z-ZFP filter.",
    )

    variant(
        "daz",
        default=False,
        when="@1.0.0:",
        description="Denormals are zero: "
        "Treat denormal-only blocks as containing "
        "all zeroes",
    )

    variant(
        "fasthash",
        default=False,
        when="@0.5.2:",
        description="Use a faster but more collision prone hash function",
    )

    variant("profile", default=False, when="@0.5.2:", description="Count cache misses")

    variant(
        "round",
        default="never",
        values=("never", "first", "last"),
        multi=False,
        when="@1.0.0:",
        description="EXPERIMENTAL: Set coefficient rounding method",
    )

    variant(
        "strided", default=False, description="Enable strided access for progressive zfp streams"
    )

    variant(
        "tight-error",
        default=False,
        when="@1.0.0:",
        description="EXPERIMENTAL: Use tighter error bound when rounding is enabled",
    )

    variant("twoway", default=False, description="Use two-way skew-associative cache")

    # Conflicts
    conflicts(
        "+tight-error",
        when="round=never",
        msg="Using zfp with tight error requires a rounding mode other than never",
    )

    # CMake options
    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_UTILITIES", "utilities"),
            self.define_from_variant("BUILD_CFP", "c"),
            self.define_from_variant("BUILD_ZFPY", "python"),
            self.define_from_variant("BUILD_ZFORP", "fortran"),
            self.define_from_variant("ZFP_WITH_OPENMP", "openmp"),
            self.define_from_variant("ZFP_WITH_CUDA", "cuda"),
            self.define_from_variant("ZFP_WITH_ALIGNED_ALLOC", "aligned"),
            self.define("ZFP_BIT_STREAM_WORD_SIZE", spec.variants["bsws"].value),
            self.define_from_variant("ZFP_WITH_DAZ", "daz"),
            self.define_from_variant("ZFP_WITH_CACHE_FAST_HASH", "fasthash"),
            self.define_from_variant("ZFP_WITH_CACHE_PROFILE", "profile"),
            self.define_from_variant("ZFP_WITH_BIT_STREAM_STRIDED", "strided"),
            self.define_from_variant("ZFP_WITH_TIGHT_ERROR", "tight-error"),
            self.define_from_variant("ZFP_WITH_CACHE_TWOWAY", "twoway"),
        ]

        if "round" in spec.variants:
            args.append(
                "ZFP_ROUNDING_MODE=ZFP_ROUND_{0}".format(spec.variants["round"].value.upper())
            )

        if "+cuda" in spec:
            args.append("-DCUDA_BIN_DIR={0}".format(spec["cuda"].prefix.bin))

            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                args.append("-DCMAKE_CUDA_FLAGS=-arch sm_{0}".format(cuda_arch[0]))

        return args
