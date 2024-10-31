# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class G2tmpl(CMakePackage):
    """Utilities for GRIB2 templates.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-g2tmpl"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-g2tmpl/archive/refs/tags/v1.10.0.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-g2tmpl"

    maintainers("edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("develop", branch="develop")
    version("1.13.0", sha256="7e52cccc91277bcedbd9e13ee3478480e744eb22d13c5b636bd0ad91bf43d38e")
    version("1.12.0", sha256="44272be7bde8da05565255a8ecdbd080c659d7f0669e356e1c8fef6bac05e723")
    version("1.11.0", sha256="00fde3b37c6b4d1f0eaf60f230159298ffcb47349a076c3bd6afa20c7ed791a9")
    version("1.10.2", sha256="4063361369f3691f75288c801fa9d1a2414908b7d6c07bbf69d4165802e2a7fc")
    version("1.10.1", sha256="0be425e5128fabb89915a92261aa75c27a46a3e115e00c686fc311321e5d1e2a")
    version("1.10.0", sha256="dcc0e40b8952f91d518c59df7af64e099131c17d85d910075bfa474c8822649d")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("shared", default=False, description="Build shared library")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
