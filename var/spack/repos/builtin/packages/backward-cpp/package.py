# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class BackwardCpp(CMakePackage):
    """A beautiful stack trace pretty printer for C++."""

    homepage = "https://github.com/bombela/backward-cpp"
    git = "https://github.com/bombela/backward-cpp.git"
    url = "https://github.com/bombela/backward-cpp/archive/refs/tags/v1.6.tar.gz"

    license("MIT")

    version("master", branch="master")
    version("1.6", sha256="c654d0923d43f1cea23d086729673498e4741fb2457e806cfaeaea7b20c97c10")
    version("1.5", sha256="faf7d4fe7ca65117ed4fe7be9bff9628927bd95b49f71df63d5f99af233d1915")
    version("1.4", sha256="ad73be31c5cfcbffbde7d34dba18158a42043a109e7f41946f0b0abd589ed55e")
    version("1.3", sha256="4bf3fb7029ff551acda6578d9d8e13d438ebdd82a787a82b157728e3af6b5dec")
    version("1.2", sha256="0a44fdad126cf2c53f93c33fd6418abaf99672048c98a5a57e2a2e43a38d5f84")
    version("1.1", sha256="36139e98b8b6a8ff84b28c50fd6443054ccee93cf63231fdd1db0036093553c4")

    depends_on("cxx", type="build")  # generated

    variant("dwarf", default=False, description="Use libdwarf/libelf to read debug info")

    depends_on("libdwarf", when="+dwarf")

    def cmake_args(self):
        return ["-DBACKWARD_SHARED=ON"]
