# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GslLite(CMakePackage):
    """A single-file header-only version of ISO C++ Guidelines Support Library
    (GSL) for C++98, C++11, and later"""

    homepage = "https://github.com/gsl-lite/gsl-lite"
    git = "https://github.com/gsl-lite/gsl-lite.git"
    url = "https://github.com/gsl-lite/gsl-lite/archive/refs/tags/v0.38.1.tar.gz"

    maintainers("AlexanderRichert-NOAA", "climbfuji", "edwardhartnett", "Hang-Lei-NOAA")

    license("MIT")

    version("0.41.0", sha256="4682d8a60260321b92555760be3b9caab60e2a71f95eddbdfb91e557ee93302a")
    version("0.40.0", commit="d6c8af99a1d95b3db36f26b4f22dc3bad89952de")
    version("0.39.0", commit="d0903fa87ff579c30f608bc363582e6563570342")
    version("0.38.1", sha256="c2fa2315fff312f3897958903ed4d4e027f73fa44235459ecb467ad7b7d62b18")
    version("0.38.0", sha256="5d25fcd31ea66dac9e14da1cad501d95450ccfcb2768fffcd1a4170258fcbc81")
    version("0.37.0", sha256="a31d51b73742bb234acab8d2411223cf299e760ed713f0840ffed0dabe57ca38")
    version("0.36.0", sha256="c052cc4547b33cedee6f000393a7005915c45c6c06b35518d203db117f75c71c")
    version("0.34.0", sha256="a7d5b2672b78704ca03df9ef65bc274d8f8cacad3ca950365eef9e25b50324c5")

    depends_on("cxx", type="build")  # generated

    variant("tests", default=False, description="Build and perform gsl-lite tests")
    variant("cuda_tests", default=False, description="Build and perform gsl-lite CUDA tests")
    variant("examples", default=False, description="Build gsl-lite examples")
    variant(
        "static_analysis_demos",
        default=False,
        description="Build and perform gsl-lite static analysis demos",
    )
    variant(
        "cmake_export_package_registry",
        default=False,
        description="Export build directory to CMake user package registry",
    )
    variant(
        "compat_header", default=False, description="Install MS-GSL compatibility header <gsl/gsl>"
    )
    variant(
        "legacy_headers",
        default=False,
        description="Install legacy headers <gsl.h>, <gsl.hpp>, <gsl/gsl-lite.h>",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("GSL_LITE_OPT_BUILD_TESTS", "tests"),
            self.define_from_variant("GSL_LITE_OPT_BUILD_CUDA_TESTS", "cuda_tests"),
            self.define_from_variant("GSL_LITE_OPT_BUILD_EXAMPLES", "examples"),
            self.define_from_variant(
                "GSL_LITE_LOPT_BUILD_STATIC_ANALYSIS_DEMOS", "static_analysis_demos"
            ),
            self.define_from_variant(
                "CMAKE_EXPORT_PACKAGE_REGISTRY", "cmake_export_package_registry"
            ),
            self.define_from_variant("GSL_LITE_OPT_INSTALL_COMPAT_HEADER", "compat_header"),
            self.define_from_variant("GSL_LITE_OPT_INSTALL_LEGACY_HEADERS", "legacy_headers"),
        ]
        return args
