# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppcoro(CMakePackage):
    """A library of C++ coroutine abstractions."""

    homepage = "https://github.com/andreasbuhr/cppcoro"
    git = "https://github.com/andreasbuhr/cppcoro.git"

    maintainers("pbrady")

    license("MIT")

    version("develop", branch="master")
    version("2021-01-13", commit="7cc9433436fe8f2482138019cfaafce8e1d7a896")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
