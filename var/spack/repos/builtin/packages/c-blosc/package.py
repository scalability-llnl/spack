# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class CBlosc(CMakePackage):
    """Blosc, an extremely fast, multi-threaded, meta-compressor library"""

    homepage = "https://www.blosc.org"
    url = "https://github.com/Blosc/c-blosc/archive/v1.11.1.tar.gz"

    license("BSD-3-Clause")

    version("1.21.5", sha256="32e61961bbf81ffea6ff30e9d70fca36c86178afd3e3cfa13376adec8c687509")
    version("1.21.4", sha256="e72bd03827b8564bbb3dc3ea0d0e689b4863871ce3861d946f2efd7a186ecf3e")
    version("1.21.2", sha256="e5b4ddb4403cbbad7aab6e9ff55762ef298729c8a793c6147160c771959ea2aa")
    version("1.21.1", sha256="f387149eab24efa01c308e4cba0f59f64ccae57292ec9c794002232f7903b55b")
    version("1.21.0", sha256="b0ef4fda82a1d9cbd11e0f4b9685abf14372db51703c595ecd4d76001a8b342d")
    version("1.17.0", sha256="75d98c752b8cf0d4a6380a3089d56523f175b0afa2d0cf724a1bd0a1a8f975a4")
    version("1.16.3", sha256="bec56cb0956725beb93d50478e918aca09f489f1bfe543dbd3087827a7344396")
    version("1.15.0", sha256="dbbb01f9fedcdf2c2ff73296353a9253f44ce9de89c081cbd8146170dce2ba8f")
    version("1.12.1", sha256="e04535e816bb942bedc9a0ba209944d1eb34e26e2d9cca37f114e8ee292cb3c8")
    version("1.11.1", sha256="d15937961d37b0780b8fb0641483eb9f6d4c379f88ac7ee84ff5dd06c2b72360")
    version("1.9.2", sha256="6349ab927705a451439b2e23ec5c3473f6b7e444e6d4aafaff76b789713e9fee")
    version("1.9.1", sha256="e4433fb0708517607cf4377837c4589807b9a8c112b94f7978cc8aaffb719bf0")
    version("1.9.0", sha256="0cb5b5f7a25f71227e3dced7a6035e8ffd94736f7ae9fae546efa3b7c6e7a852")
    version("1.8.1", sha256="1abf048634c37aeca53eeb6a9248ea235074077028d12b3560eccf1dff7143b8")
    version("1.8.0", sha256="e0f8b9e12e86776a1b037385826c55006da6e2ae4973dac5b5ad3cfcf01e9043")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("avx2", default=True, description="Enable AVX2 support")

    depends_on("cmake@2.8.10:", type="build")
    depends_on("snappy")
    depends_on("zlib-api")
    depends_on("zstd")
    depends_on("lz4")

    patch("gcc.patch", when="@1.12.1:1.17.0")
    patch("test_forksafe.patch", when="@1.15.0:1.17.0%intel")

    @property
    def libs(self):
        return find_libraries("libblosc", root=self.prefix, recursive=True)

    def cmake_args(self):
        args = []

        if self.spec.satisfies("+avx2"):
            args.append("-DDEACTIVATE_AVX2=OFF")
        else:
            args.append("-DDEACTIVATE_AVX2=ON")

        if self.spec.satisfies("@1.12.0:"):
            args.append("-DPREFER_EXTERNAL_SNAPPY=ON")
            args.append("-DPREFER_EXTERNAL_ZLIB=ON")
            args.append("-DPREFER_EXTERNAL_ZSTD=ON")
            args.append("-DPREFER_EXTERNAL_LZ4=ON")

            if self.run_tests:
                args.append("-DBUILD_TESTS=ON")
                args.append("-DBUILD_BENCHMARKS=ON")
            else:
                args.append("-DBUILD_TESTS=OFF")
                args.append("-DBUILD_BENCHMARKS=OFF")

        return args

    @run_after("install")
    def darwin_fix(self):
        if sys.platform == "darwin":
            fix_darwin_install_name(self.prefix.lib)
