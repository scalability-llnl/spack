# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bfs(MakefilePackage):
    """A breadth-first version of the UNIX find command."""

    homepage = "https://github.com/tavianator/bfs"
    url = "https://github.com/tavianator/bfs/archive/refs/tags/3.0.1.tar.gz"

    maintainers("alecbcs")

    license("0BSD")

    version("4.0.1", sha256="8117b76b0a967887278a11470cbfa9e7aeae98f11a7eeb136f456ac462e5ba23")
    version("3.1.1", sha256="d73f345c1021e0630e0db930a3fa68dd1f968833037d8471ee1096e5040bf91b")
    version("3.1", sha256="aa6a94231915d3d37e5dd62d194cb58a575a8f45270020f2bdd5ab41e31d1492")
    version("3.0.4", sha256="7196f5a624871c91ad051752ea21043c198a875189e08c70ab3167567a72889d")
    version("3.0.2", sha256="d3456a9aeecc031064db0dbe012e55a11eb97be88d0ab33a90e570fe66457f92")
    version("3.0.1", sha256="a38bb704201ed29f4e0b989fb2ab3791ca51c3eff90acfc31fff424579bbf962")

    depends_on("c", type="build")

    depends_on("acl", when="platform=linux")
    depends_on("attr", when="platform=linux")
    depends_on("libcap", when="platform=linux")
    depends_on("liburing", when="platform=linux @3.1:")
    depends_on("oniguruma")

    @run_before("build", when="@4:")
    def configure(self):
        args = ["--enable-release", f"--prefix={self.prefix}"]

        configure_exe = Executable("./configure")
        configure_exe(*args)

    def install(self, spec, prefix):
        if spec.satisfies("@:3"):
            make("install", f"PREFIX={prefix}")
        else:
            make("install")
