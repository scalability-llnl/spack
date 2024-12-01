# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tracy(MakefilePackage):
    """A real time, nanosecond resolution, remote telemetry, hybrid frame and sampling
    profiler for games and other applications. Server applications."""

    homepage = "https://github.com/wolfpld/tracy"
    url = "https://github.com/wolfpld/tracy/archive/v0.0.0.tar.gz"
    maintainers("msimberg")

    license("BSD-3-Clause")

    version("master", git="https://github.com/wolfpld/tracy.git", branch="master")
    version("0.10", sha256="a76017d928f3f2727540fb950edd3b736caa97b12dbb4e5edce66542cbea6600")
    version("0.9", sha256="93a91544e3d88f3bc4c405bad3dbc916ba951cdaadd5fcec1139af6fa56e6bfc")
    version("0.8.2", sha256="4784eddd89c17a5fa030d408392992b3da3c503c872800e9d3746d985cfcc92a")
    version("0.8.1", sha256="004992012b2dc879a9f6d143cbf94d7ea30e88135db3ef08951605d214892891")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("capstone")
    depends_on("dbus")
    depends_on("freetype")
    # Linking fails unless glfw is built as a shared library:
    # https://github.com/wolfpld/tracy/issues/110
    depends_on("glfw +shared")

    def build(self, spec, prefix):
        with working_dir(join_path(self.build_directory, "capture/build/unix")):
            make()

        with working_dir(join_path(self.build_directory, "profiler/build/unix")):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.build_directory, "capture/build/unix/capture-release"), prefix.bin)
        install(join_path(self.build_directory, "profiler/build/unix/Tracy-release"), prefix.bin)
