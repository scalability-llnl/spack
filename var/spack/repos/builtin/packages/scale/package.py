# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Scale(MakefilePackage):
    """SCALE (Scalable Computing for Advanced Library and Environment) is
    a basic library for weather and climate model of the earth and planets
    aimed to be widely used in various models.
    The SCALE library is developed with co-design by researchers of
    computational science and computer science."""

    homepage = "https://scale.riken.jp/"
    url = "https://scale.riken.jp/archives/scale-5.4.4.tar.gz"

    maintainers("t-yamaura")

    license("BSD-2-Clause")

    version(
        "5.4.4",
        sha256="7d0ec4069c15d8b9ec7166f32c9a2eda772d975a8e08e420e6b16891ceebb316",
        preferred=True,
    )
    version("5.3.6", sha256="3ab0d42cdb16eee568c65b880899e861e464e92088ceb525066c726f31d04848")
    version("5.2.6", sha256="e63141d05810e3f41fc89c9eb15e2319d753832adabdac8f7c8dd7acc0f5f8ed")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi@2:", type=("build", "link", "run"))
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("parallel-netcdf")

    patch("fj-own_compiler.patch", when="%fj")

    parallel = False

    def setup_build_environment(self, build_env):
        build_env.set("PREFIX", self.prefix)

    def build(self, spec, prefix):
        scale_sys_str = ""
        if self.spec.satisfies("platform=linux %gcc"):
            scale_sys_str = "Linux64-gnu-ompi"
        elif self.spec.satisfies("platform=linux %intel"):
            scale_sys_str = "Linux64-intel-impi"
        elif self.spec.satisfies("platform=linux %pgi"):
            scale_sys_str = "Linux64-pgi-ompi"
        elif self.spec.satisfies("platform=linux target=arm %gcc"):
            scale_sys_str = "LinuxARM-gnu-ompi"
        elif self.spec.satisfies("platform=linux target=a64fx %fj"):
            scale_sys_str = "FUGAKU"
        elif self.spec.satisfies("platform=linux target=s64fx %fj"):
            scale_sys_str = "FX100"
        elif self.spec.satisfies("platform=darwin %gcc"):
            scale_sys_str = "MacOSX-gnu-ompi"

        if scale_sys_str == "":
            raise InstallError("unsupported arch and compiler combination.")
        env["SCALE_SYS"] = scale_sys_str

        # set SCALE_NETCDF_INCLUDE
        nc_config = which("nc-config")
        nc_str = nc_config("--cflags", "--fflags", output=str)
        try:
            env["SCALE_NETCDF_INCLUDE"] = nc_str.replace("\n", " ")
        except TypeError:  # for python3
            env["SCALE_NETCDF_INCLUDE"] = nc_str.decode().replace("\n", " ")

        # set SCALE_NETCDF_LIBS
        nc_config = which("nc-config")
        nc_str = nc_config("--libs", "--flibs", output=str)
        try:
            env["SCALE_NETCDF_LIBS"] = nc_str.replace("\n", " ")
        except TypeError:  # for python3
            env["SCALE_NETCDF_LIBS"] = nc_str.decode().replace("\n", " ")

        make()

    def install(self, spec, prefix):
        make("install")

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("doc", prefix.share.docs)
        install_tree(os.path.join("scale-rm", "test"), os.path.join(prefix.share, "test"))
