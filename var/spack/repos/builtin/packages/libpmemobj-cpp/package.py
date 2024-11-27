# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpmemobjCpp(CMakePackage):
    """C++ bindings for libpmemobj (https://github.com/pmem/pmdk)"""

    homepage = "https://github.com/pmem/libpmemobj-cpp"
    url = "https://github.com/pmem/libpmemobj-cpp/archive/1.12.tar.gz"
    git = "https://github.com/pmem/libpmemobj-cpp.git"

    version("develop", branch="master")
    version("1.13.0", sha256="1fd204303b86ff9974e39d6cdb4037556402df981bebcc824a9125e12bf48c80")
    version("1.12", sha256="5a7e082a862affbd87ff174b790be7db77f7d85d4c583acc34011f1104bc54a9")
    version("1.11", sha256="2818f3ce23c861222d2765c377e6d4ccf8a2e2f66e4d23e4e2c35f4246f4a403")
    version("1.10", sha256="bba31d9a1c21b38c20cbe2d2b152effef7e2debfa89a87e0c32de616c31d9191")
    version("1.9", sha256="0284c20e7f642f16b3d49d576a6540bcf68330962ac273e11b07158b6e769689")
    version("1.8", sha256="dcf60be1140a90f10b8eeb763d53e3dfcdf5a5b345e10f78d469356642527b32")
    version("1.7", sha256="53af87a648ff28a74d6856ce2125ca4acdb0c4b78062df1cba18d50d35e3eada")
    version("1.6", sha256="791bf86c6b9401451e3d20f19cb8799d312b9d58659cb93aa532cd724db554ae")
    version("1.5.1", sha256="0448bac4697f6563789e5bf22b8556288ae67ab916608bc45d0a3baa24c67985")
    version("1.5", sha256="6254aa2fb77977f8b91998eb866216d2af22f4ccbffdfc7932df1dff151da61e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # libpmemobj only supports 'Debug' and 'Release'
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release"),
    )

    depends_on("pmdk@master", when="@develop")
    depends_on("pmdk@1.9:", when="@1.12:")
    depends_on("pmdk@1.8:", when="@1.9:")
    depends_on("pmdk@1.7:", when="@1.8:")
    depends_on("pmdk@1.4:", when="@1.5:")

    def cmake_args(self):
        args = ["-DTESTS_USE_VALGRIND=OFF"]
        return args
