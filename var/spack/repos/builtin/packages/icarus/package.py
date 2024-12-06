# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Icarus(AutotoolsPackage):
    """Icarus Verilog is a Verilog simulation and synthesis tool."""

    homepage = "http://www.iverilog.icarus.com"
    url = "https://github.com/steveicarus/iverilog/archive/refs/tags/v12_0.tar.gz"
    git = "https://github.com/steveicarus/iverilog.git"

    maintainers("davekeeshan")

    license("GPL-2.0-only")

    version("master", branch="master")
    version("12_0", sha256="a68cb1ef7c017ef090ebedb2bc3e39ef90ecc70a3400afb4aa94303bc3beaa7d")
    version("11_0", sha256="6327fb900e66b46803d928b7ca439409a0dc32731d82143b20387be0833f1c95")
    version("10_3", commit="453c5465895eaca4a792d18b75e9ec14db6ea50e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("gperf @3.0:", type="build")
    depends_on("readline @4.2:", type=("build", "link"))
    depends_on("zlib-api", type=("build", "link"))

    patch("fix-gcc-10.patch", when="@v10_3")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autoconf.sh")

    @run_before("install")
    def create_install_folders(self):
        mkdirp(prefix.bin)
        mkdirp(join_path(prefix.include, "iverilog"))
        mkdirp(join_path(prefix.lib, "ivl"))
        mkdirp(join_path(prefix.lib, "ivl", "include"))
        mkdirp(join_path(prefix.share, "man"))
        mkdirp(join_path(prefix.share, "man", "man1"))

    # We need to fix the CC and CXX paths, as they point to the spack
    # wrapper scripts which aren't usable without spack
    @run_after("install")
    def patch_compiler(self):
        filter_file(
            r"^CC\s*=.*", f"CC={self.compiler.cc}", join_path(self.prefix.bin, "iverilog-vpi")
        )
        filter_file(
            r"^CXX\s*=.*", f"CXX={self.compiler.cxx}", join_path(self.prefix.bin, "iverilog-vpi")
        )
