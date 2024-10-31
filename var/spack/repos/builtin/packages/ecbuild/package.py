# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ecbuild(CMakePackage):
    """ecBuild is the ECMWF build system. It is built on top of CMake and
    consists of a set of macros as well as a wrapper around CMake"""

    homepage = "https://github.com/ecmwf/ecbuild"
    url = "https://github.com/ecmwf/ecbuild/archive/refs/tags/3.6.1.tar.gz"

    maintainers("skosukhin", "climbfuji", "victoria-cherkas", "dominichofer")

    license("Apache-2.0")

    version("3.7.2", sha256="7a2d192cef1e53dc5431a688b2e316251b017d25808190faed485903594a3fb9")
    version("3.6.5", sha256="98bff3d3c269f973f4bfbe29b4de834cd1d43f15b1c8d1941ee2bfe15e3d4f7f")
    version("3.6.1", sha256="796ccceeb7af01938c2f74eab0724b228e9bf1978e32484aa3e227510f69ac59")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.11:", type=("build", "run"))

    # See https://github.com/ecmwf/ecbuild/issues/35
    depends_on("cmake@:3.19", type=("build", "run"), when="@:3.6.1")

    # Some of the installed scripts require running Perl:
    depends_on("perl", type=("build", "run"))

    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    @when("+fismahigh")
    def patch(self):
        filter_file('ssh://[^"]+', "", "cmake/compat/ecmwf_git.cmake")
        filter_file('https?://[^"]+', "", "cmake/compat/ecmwf_git.cmake")
        filter_file(
            "https?://.*test-data", "DISABLED_BY_DEFAULT", "cmake/ecbuild_check_urls.cmake"
        )
        filter_file(
            "https?://.*test-data", "DISABLED_BY_DEFAULT", "cmake/ecbuild_get_test_data.cmake"
        )
