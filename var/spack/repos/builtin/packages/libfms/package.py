# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfms(CMakePackage):
    """Field and Mesh Specification (FMS) library"""

    homepage = "https://github.com/CEED/FMS"
    git = "https://github.com/CEED/FMS.git"

    tags = ["FEM", "Meshes", "Fields", "High-order", "I/O", "Data-exchange"]

    maintainers("v-dobrev", "tzanio", "cwsmith")

    license("BSD-2-Clause")

    version("develop", branch="master")
    version("0.2.0", tag="v0.2", commit="a66cb96711cc404c411f1bf07ca8db09b6f894eb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("conduit", default=True, description="Build with Conduit I/O support")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("cmake@3.1:", type="build")
    depends_on("conduit@0.7.1:", when="+conduit")

    def cmake_args(self):
        args = []
        args.extend([self.define_from_variant("BUILD_SHARED_LIBS", "shared")])
        if self.spec.satisfies("+conduit"):
            args.extend([self.define("CONDUIT_DIR", self.spec["conduit"].prefix)])

        return args

    @property
    def headers(self):
        """Export the FMS headers.
        Sample usage: spec['libfms'].headers.cpp_flags
        """
        fms_h_names = ["fms", "fmsio"]
        hdrs = find_headers(fms_h_names, self.prefix.include, recursive=False)
        return hdrs or None  # Raise an error if no headers are found

    @property
    def libs(self):
        """Export the FMS library.
        Sample usage: spec['libfms'].libs.ld_flags
        """
        is_shared = self.spec.satisfies("+shared")
        libs = find_libraries("libfms", root=self.prefix, shared=is_shared, recursive=True)
        return libs or None  # Raise an error if no libs are found
