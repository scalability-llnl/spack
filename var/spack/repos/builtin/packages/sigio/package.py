# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sigio(CMakePackage):
    """The SIGIO library provides an Application Program Interface for performing
    I/O on the sigma restart file of the NOAA global spectral model.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sigio"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-sigio/archive/refs/tags/v2.3.2.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-sigio"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("2.3.3", sha256="2b4a04be3be10f222d0ff47f973f65a03b8b5521dcad8e8866f3bfe4e8dfafab")
    version("2.3.2", sha256="333f3cf3a97f97103cbafcafc2ad89b24faa55b1332a98adc1637855e8a5b613")

    depends_on("fortran", type="build")

    conflicts("%oneapi", when="@:2.3.2", msg="Requires @2.3.3: for Intel OneAPI")

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    def setup_run_environment(self, env):
        lib = find_libraries("libsigio", root=self.prefix, shared=False, recursive=True)
        # Only one library version, but still need to set _4 to make NCO happy
        for suffix in ("4", ""):
            env.set("SIGIO_LIB" + suffix, lib[0])
            env.set("SIGIO_INC" + suffix, join_path(self.prefix, "include"))

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%fj"):
            if name == "fflags":
                flags.append("-Free")
        return (None, None, flags)

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
