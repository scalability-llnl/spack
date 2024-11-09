# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class All(CMakePackage):
    """A Load Balancing Library (ALL)

    The library aims to provide an easy way to include dynamic domain-based
    load balancing into particle based simulation codes.
    """

    homepage = "http://slms.pages.jsc.fz-juelich.de/websites/all-website/"
    url = "https://gitlab.jsc.fz-juelich.de/SLMS/loadbalancing/-/archive/v0.9.2/loadbalancing-v0.9.2.tar.gz"

    maintainers("junghans")

    license("BSD-3-Clause", checked_by="junghans")

    version("0.9.2", sha256="2b4ef52c604c3c0c467712d0912a33c82177610b67edc14df1e034779c6ddb71")

    variant("fortran", default=False, description="Build with fortran support")
    variant("shared", default=True, description="Build shared libraries")
    variant("vtk", default=False, description="Build with vtk support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")
    depends_on("vtk", when="+vtk")

    depends_on("mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CM_ALL_FORTRAN", "fortran"),
            self.define_from_variant("CM_ALL_USE_F08", "fortran"),
            self.define_from_variant("CM_ALL_VTK_OUTPUT", "vtk"),
        ]

        if self.run_tests:
            args.append("-DCM_ALL_TESTS=ON")
            args.append("-DCM_ALL_TESTS_INTEGRATION=ON")

        return args
