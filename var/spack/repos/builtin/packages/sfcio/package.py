# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sfcio(CMakePackage):
    """The SFCIO library provides an API to read the NCEP Spectral model surface
    files.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sfcio"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-sfcio/archive/refs/tags/v1.4.1.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-sfcio"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("1.4.2", sha256="bfde52320b836886a766ff8d0d6707b8a533c903b947f8b49250c544aaccaaac")
    version("1.4.1", sha256="d9f900cf18ec1a839b4128c069b1336317ffc682086283443354896746b89c59")

    depends_on("fortran", type="build")

    depends_on("pfunit", type="test")

    conflicts("%oneapi", when="@:1.4.1", msg="Requires @1.4.2: for Intel oneAPI")

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    def setup_run_environment(self, env):
        lib = find_libraries("libsfcio", root=self.prefix, shared=False, recursive=True)
        # Only one library version, but still need to set _4 to make NCO happy
        for suffix in ("4", ""):
            env.set("SFCIO_LIB" + suffix, lib[0])
            env.set("SFCIO_INC" + suffix, join_path(self.prefix, "include"))

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%fj"):
            if name == "fflags":
                flags.append("-Free")
        return (None, None, flags)

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
