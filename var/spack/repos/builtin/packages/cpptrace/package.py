# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cpptrace(CMakePackage):
    """Simple, portable, and self-contained stacktrace library for C++11 and newer"""

    homepage = "https://github.com/jeremy-rifkin/cpptrace"
    url = "https://github.com/jeremy-rifkin/cpptrace/archive/refs/tags/v0.6.3.tar.gz"

    maintainers("pranav-sivaraman")

    license("MIT", checked_by="pranav-sivaraman")

    version("0.6.3", sha256="665bf76645ec7b9e6d785a934616f0138862c36cdb58b0d1c9dd18dd4c57395a")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
