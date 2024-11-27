# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rr(CMakePackage):
    """Application execution recorder, player and debugger"""

    homepage = "https://rr-project.org/"
    url = "https://github.com/mozilla/rr/archive/4.5.0.tar.gz"

    version("4.5.0", sha256="19f28259c0aa562c9518ae51207377fa93071a7dc270a0738d8d39e45ae2b1c0")
    version("4.4.0", sha256="b2b24a3f67df47576126421746cd2942a458d2825faa76e8bb3ca43edffa03d3")
    version("4.3.0", sha256="46933cdd706d71c3de05b55937c85ee055c08e67e5c1e6a1278c7feb187ca37a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gdb")
    depends_on("git")
    depends_on("zlib-api")
    # depends_on('capnproto', when='@4.6:')  # not yet in spack
    # depends_on('libcapnp')    # needed for future releases
    depends_on("pkgconfig", type="build")
    depends_on("py-pexpect", type="test")

    # rr needs architecture Nehalem and beyond, how can spack
    # test this?

    # Only 'Release' is supported at the moment
    variant(
        "build_type", default="Release", description="The build type to build", values=("Release",)
    )

    def patch(self):
        # because otherwise CMake would try and fail to set RPATH of
        # rr_exec_stub
        filter_file(r"^(install\(TARGETS .*)\s*rr_exec_stub", r"\1", "CMakeLists.txt")

    def cmake_args(self):
        return ["-Ddisable32bit=ON"]

    @run_after("install")
    def install_stub(self):
        with working_dir(self.build_directory):
            mkdirp(self.prefix.bin)
            install("bin/rr_exec_stub", self.prefix.bin)
