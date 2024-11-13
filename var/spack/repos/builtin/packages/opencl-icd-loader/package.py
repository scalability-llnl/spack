# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpenclIcdLoader(CMakePackage):
    """Khronos official OpenCL ICD Loader"""

    homepage = "https://github.com/KhronosGroup/OpenCL-ICD-Loader"
    url = "https://github.com/KhronosGroup/OpenCL-ICD-Loader/archive/refs/tags/v2024.05.08.tar.gz"

    maintainers("uphoffc")

    license("Apache-2.0", checked_by="uphoffc")

    version(
        "2024.05.08", sha256="eb2c9fde125ffc58f418d62ad83131ba686cccedcb390cc7e6bb81cc5ef2bd4f"
    )
    version(
        "2023.12.14", sha256="af8df96f1e1030329e8d4892ba3aa761b923838d4c689ef52d97822ab0bd8917"
    )
    version(
        "2023.04.17", sha256="173bdc4f321d550b6578ad2aafc2832f25fbb36041f095e6221025f74134b876"
    )
    version(
        "2023.02.06", sha256="f31a932b470c1e115d6a858b25c437172809b939953dc1cf20a3a15e8785d698"
    )
    version(
        "2022.09.30", sha256="e9522fb736627dd4feae2a9c467a864e7d25bb715f808de8a04eea5a7d394b74"
    )
    version(
        "2022.09.23", sha256="937bbdb52819922e0e38ae765e3c3d76b63be185d62f25e256ea3f77fdaa9913"
    )
    version(
        "2022.05.18", sha256="71f70bba797a501b13b6b0905dc852f3fd6e264d74ce294f2df98d29914c4303"
    )
    version(
        "2022.01.04", sha256="9f21d958af68c1b625a03c2befddd79da95d610614ddab6c291f26f01a947dd8"
    )
    version(
        "2021.06.30", sha256="a50557ed6ff18c81aa1ed5e74700521e389c84ca5cd9188d35d368936e0a4972"
    )
    version(
        "2021.04.29", sha256="c2eb8a15b3d6d0795d609f55a4cea92eaa34571f6a21428d5593673b568ac6fd"
    )

    depends_on("c", type="build")  # generated

    depends_on("opencl-c-headers@2024.05.08", when="@2024.05.08")
    depends_on("opencl-c-headers@2023.12.14", when="@2023.12.14")
    depends_on("opencl-c-headers@2023.04.17", when="@2023.04.17")
    depends_on("opencl-c-headers@2023.02.06", when="@2023.02.06")
    depends_on("opencl-c-headers@2022.09.30", when="@2022.09.30")
    depends_on("opencl-c-headers@2022.09.23", when="@2022.09.23")
    depends_on("opencl-c-headers@2022.05.18", when="@2022.05.18")
    depends_on("opencl-c-headers@2022.01.04", when="@2022.01.04")
    depends_on("opencl-c-headers@2021.06.30", when="@2021.06.30")
    depends_on("opencl-c-headers@2021.04.29", when="@2021.04.29")

    provides("opencl@:3.0")

    def cmake_args(self):
        headers_include_dir = self.spec["opencl-c-headers"].prefix.include
        args = [self.define("OPENCL_ICD_LOADER_HEADERS_DIR", headers_include_dir)]
        return args
