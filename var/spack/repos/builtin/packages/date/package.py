# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Date(CMakePackage):
    """A date and time library based on the C++11/14/17 <chrono> header"""

    homepage = "https://github.com/HowardHinnant/date"
    url = "https://github.com/HowardHinnant/date/archive/v3.0.0.zip"

    license("MIT")

    version("3.0.1", sha256="f4300b96f7a304d4ef9bf6e0fa3ded72159f7f2d0f605bdde3e030a0dba7cf9f")
    version("3.0.0", sha256="ddbec664607bb6ec7dd4c7be1f9eefc3d8ce88293ffc9391486ce6ce887ec9b2")

    variant(
        "cxxstd",
        default="17",
        values=("11", "14", "17"),
        description="Use the specified C++ standard when building",
    )
    variant("shared", default=False, description="Build shared instead of static libraries")
    variant("tz", default=False, description="Build/install of TZ library")
    variant(
        "tzdb",
        default="download",
        values=("download", "system", "manual"),
        description="Timezone database source (automatic download, use "
        "operating system's database, or manually specify)",
    )

    depends_on("cmake@3.7.0:", type="build")
    depends_on("curl", when="+tz tzdb=download")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("CMAKE_CXX_STANDARD", spec.variants["cxxstd"].value),
            self.define("CMAKE_CXX_STANDARD_REQUIRED", True),
            self.define("BUILD_SHARED_LIBS", "+shared" in spec),
            self.define("BUILD_TZ_LIB", "+tz" in spec),
        ]

        tzdb = spec.variants["tzdb"].value
        args.extend(
            [
                self.define("USE_SYSTEM_TZ_DB", tzdb == "system"),
                self.define("MANUAL_TZ_DB", tzdb == "manual"),
            ]
        )

        return args
