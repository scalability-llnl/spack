# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Landsfcutil(CMakePackage):
    """Utility routines useful for initializing land-surface states in
    NCEP models.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-landsfcutil"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-landsfcutil/archive/refs/tags/v2.4.1.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-landsfcutil"

    maintainers("edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("develop", branch="develop")
    version("2.4.2", sha256="ac0ee4edaab3d273d9a6acffea8aa8a5b363366c3ade3e32539c057e84e4fa73")
    version("2.4.1", sha256="831c5005a480eabe9a8542b4deec838c2650f6966863ea2711cc0cc5db51ca14")

    depends_on("fortran", type="build")

    depends_on("pfunit", type="test")

    conflicts("%oneapi", when="@:2.4.1", msg="Requires @2.4.2: for Intel oneAPI")

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    def setup_run_environment(self, env):
        for suffix in ("4", "d"):
            lib = find_libraries(
                "liblandsfcutil_" + suffix, root=self.prefix, shared=False, recursive=True
            )

            env.set("LANDSFCUTIL_LIB" + suffix, lib[0])
            env.set("LANDSFCUTIL_INC" + suffix, join_path(self.prefix, "include_" + suffix))

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%fj"):
            if name == "fflags":
                flags.append("-Free")
        return (None, None, flags)

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
