# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cprnc(CMakePackage):
    """CPRNC is a netcdf file comparison tool used by CESM
    and other scientific programs."""

    url = "https://github.com/ESMCI/cprnc/archive/refs/tags/v1.0.1.tar.gz"
    homepage = "https://github.com/ESMCI/cprnc"

    maintainers("jedwards4b", "billsacks")

    version("1.0.8", sha256="94ee3b4e724bc06161e576d45f34401f1452acf738803528cb80726eed230cae")
    version("1.0.3", sha256="3e7400f9a13d5de01964d7dd95151d08e6e30818d2a1efa9a9c7896cf6646d69")
    version("1.0.2", sha256="02edfa8050135ac0dc4a74aea05d19b0823d769b22cafa88b9352e29723d4179")
    version("1.0.1", sha256="b8a8fd4ad7e2716968dfa60f677217c55636580807b1309276f4c062ee432ccd")
    version("1.0.0", sha256="70ff75bbf01a0cef885db3074c78f39a8890949ca505530c0407398b8803552c")

    depends_on("fortran", type="build")  # generated

    depends_on("netcdf-fortran")
    depends_on("cmake@3:", type="build")

    # Still need a patch for 1.0.8 ...
    patch("install_rpath.patch", when="@:1.0.7")
    patch("install_rpath_108.patch", when="@1.0.8")

    resource(
        name="genf90",
        git="https://github.com/PARALLELIO/genf90",
        tag="genf90_200608",
        destination="genf90-resource",
    )

    def cmake_args(self):
        args = [
            self.define("GENF90_PATH", join_path(self.stage.source_path, "genf90-resource/genf90"))
        ]

        return args
