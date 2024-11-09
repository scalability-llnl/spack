# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sartre(CMakePackage):
    """Sartre 1 is an event generator for exclusive diffractive vector
    meson production and DVCS in ep and eA collisions based on the
    dipole model."""

    homepage = "https://sartre.hepforge.org"
    url = "https://sartre.hepforge.org/downloads/?f=sartre-1.39-src.tgz"
    list_url = "https://sartre.hepforge.org/downloads/"

    maintainers("wdconinc")

    license("GPL-3.0-or-later")

    version("1.39", sha256="82ed77243bea61bb9335f705c4b132f0b53d0de17c26b89389fa9cd3adcef44d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    parallel = False

    depends_on("gsl")
    depends_on("root")
    depends_on("boost@1.39: +thread")

    # FIXME cuba is vendored in 1.39
    # depends_on("cuba@4:")

    def patch(self):
        for file in ["CMakeLists.txt", "src/CMakeLists.txt", "gemini/CMakeLists.txt"]:
            filter_file(
                r"set\(CMAKE_CXX_STANDARD 11\)",
                'set(CMAKE_CXX_STANDARD 11 CACHE STRING "C++ standard")',
                file,
            )
            filter_file(r"\$\{CMAKE_INSTALL_PREFIX\}/sartre", "${CMAKE_INSTALL_PREFIX}", file)
            filter_file(r"DESTINATION sartre/", "DESTINATION ", file)

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec["root"].variants["cxxstd"].value),
            "-DMULTITHREADED=ON",
        ]
        return args
