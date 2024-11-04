# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bacio(CMakePackage):
    """The bacio library performs binary I/O for the NCEP models, processing
    unformatted byte-addressable data records, and transforming the little
    endian files and big endian files."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bacio"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-bacio/archive/refs/tags/v2.4.1.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-bacio"

    maintainers("edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("develop", branch="develop")
    version("2.6.0", sha256="03fef581e1bd3710fb8d2f2659a6c3e01a0437c1350ba53958d2ff1ffef47bcb")
    version("2.5.0", sha256="540a0ed73941d70dbf5d7b21d5d0a441e76fad2bfe37dfdfea0db3e98fc0fbfb")
    version("2.4.1", sha256="7b9b6ba0a288f438bfba6a08b6e47f8133f7dba472a74ac56a5454e2260a7200")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("pic", default=True, description="Build with position-independent-code")
    variant("shared", default=False, description="Build shared library", when="@2.6.0:")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic")]
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args

    def patch(self):
        if self.spec.satisfies("@2.4.1"):
            filter_file(".+", "2.4.1", "VERSION")

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
