# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Verilator(AutotoolsPackage):
    """Verilator is the fastest free Verilog HDL simulator.

    It compiles synthesizable Verilog (not test-bench code!), plus some PSL,
    SystemVerilog and Synthesis assertions into C++ or SystemC code. It is
    designed for large projects where fast simulation performance is of primary
    concern, and is especially well suited to generate executable models of
    CPUs for embedded software design teams.

    Please do not download this program if you are expecting a full featured
    replacement for NC-Verilog, VCS or another commercial Verilog simulator
    or Verilog compiler for a little project! (Try Icarus instead.) However, if
    you are looking for a path to migrate synthesizable Verilog to C++ or
    SystemC, and writing just a touch of C code and Makefiles doesn't scare you
    off, this is the free Verilog compiler for you.

    Verilator supports the synthesis subset of Verilog, plus initial
    statements, proper blocking/non-blocking assignments, functions, tasks,
    multi-dimensional arrays, and signed numbers. It also supports very simple
    forms of SystemVerilog assertions and coverage analysis. Verilator supports
    the more important Verilog 2005 constructs, and some SystemVerilog
    features, with additional constructs being added as users request them.

    Verilator has been used to simulate many very large multi-million gate
    designs with thousands of modules."""

    homepage = "https://www.veripool.org/projects/verilator"
    url = "https://github.com/verilator/verilator/archive/refs/tags/v5.026.tar.gz"
    git = "https://github.com/verilator/verilator.git"

    maintainers("davekeeshan")

    license("LGPL-3.0-only")

    version("master", branch="master")

    version("5.026", sha256="87fdecf3967007d9ee8c30191ff2476f2a33635d0e0c6e3dbf345cc2f0c50b78")
    version("5.024", sha256="88b04c953e7165c670d6a700f202cef99c746a0867b4e2efe1d7ea789dee35f3")
    version("5.022", sha256="3c2f5338f4b6ce7e2f47a142401acdd18cbf4c5da06092618d6d036c0afef12d")
    version("5.020", sha256="41ca9abfadf8d2413efbff7f8277379733d0095957fe7769dc38f8fd1bc899a6")
    version("5.018", sha256="8b544273eedee379e3c1a3bb849e14c754c9b5035d61ad03acdf3963092ba6c0")
    version("5.016", sha256="66fc36f65033e5ec904481dd3d0df56500e90c0bfca23b2ae21b4a8d39e05ef1")
    version("5.014", sha256="36e16c8a7c4b376f88d87411cea6ee68710e6d1382a13faf21f35d65b54df4a7")
    version("5.012", sha256="db19a7d7615b37d9108654e757427e4c3f44e6e973ed40dd5e0e80cc6beb8467")
    version("5.010", sha256="ca82b57ce2d2b34eed3f04d5daf7eae6ad41276cda88efbb59ebd6467e65d635")
    version("5.008", sha256="1d19f4cd186eec3dfb363571e3fe2e6d3377386ead6febc6ad45402f0634d2a6")
    version("5.006", sha256="eb4ca4157ba854bc78c86173c58e8bd13311984e964006803dd45dc289450cfe")
    version("5.004", sha256="7d193a09eebefdbec8defaabfc125663f10cf6ab0963ccbefdfe704a8a4784d2")
    version("5.002", sha256="72d68469fc1262e6288d099062b960a2f65e9425bdb546cba141a2507decd951")
    version("4.228", sha256="be6af6572757013802be5b0ff9c64cbf509e98066737866abaae692fe04edf09")
    version("4.226", sha256="70bc941d86e4810253d51aa94898b0802d916ab76296a398f8ceb8798122c9be")
    version("4.224", sha256="010ff2b5c76d4dbc2ed4a3278a5599ba35c8ed4c05690e57296d6b281591367b")
    version("4.222", sha256="15c60175807c0f3536c3c5b435f131c2b1e8725aefd30645efd946bf401b4c84")
    version("4.220", sha256="e00e0c31a0c00887bebbaf7a8c771efa09420a4d1fbae54d45843baf50df4426")
    version("4.218", sha256="ef7b1e6ddb715ddb3cc998fcbefc7150cfa2efc5118cf43ddb594bf41ea41cc7")
    version("4.216", sha256="64e5093b629a7e96178e3b2494f208955f218dfac6f310a91e4fc07d050c980b")
    version("4.214", sha256="e14c7f6ffb00a6746ae2a8ea0424e90a1a30067e8ae4c96b8c42689ca1ca0b1f")
    version("4.212", sha256="7b655859e4e75c9673141aede8f5a20f47e4c380055d1a588d5be60cbbc73619")
    version("4.210", sha256="3a2e6f27a5d80116a268ba054a3be61aca924bc54c5556ea25e75ee974201abb")
    version("4.204", sha256="dbad9bd3cac34e63bbd945fff9a59eaabe31dae1e1c93c847d0f894db9919498")
    version("4.202", sha256="a60c02f299ddb5bb8e963dc7d81983c55c293d97718685c1cd4b66638a33d98e")
    version("4.200", sha256="2cd0fd48152f152d0487eaac23803d35ff75e924734435b366a523deb1185407")
    version("4.110", sha256="603c23944577a5d53a2e09191d04d5c61740a77b58f3a590a70e56f4526a5a0b")
    version("4.108", sha256="ce521dc57754e5a325ff7000c434ce23674c8e1de30e1f2a6506dc3a33bd7c55")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("help2man", type="build")
    depends_on("bison", type="build")
    depends_on("flex")
    depends_on("perl", type=("build", "run"))
    depends_on("ccache", type=("build", "run"), when="@5.018:")

    conflicts("%gcc@:6", msg="C++14 support required")

    # we need to fix the CXX and LINK paths, as they point to the spack
    # wrapper scripts which aren't usable without spack
    filter_compiler_wrappers("verilated.mk", relative_root="include")
    filter_compiler_wrappers("verilated.mk", relative_root="share/verilator/include")

    @when("@:5.022")
    def setup_run_environment(self, env):
        env.prepend_path("VERILATOR_ROOT", self.prefix)

    def autoreconf(self, spec, prefix):
        autoconf()

    # verilator requires access to its shipped scripts (bin) and include
    # but the standard make doesn't put it in the correct places
    @run_before("install")
    def install_include(self):
        install_tree("include", prefix.include)
        install_tree("bin", prefix.bin)
