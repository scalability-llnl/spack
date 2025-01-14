# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import join as pjoin

from spack.package import *


class Vtr(MakefilePackage):
    """The Verilog to Routing (VTR) project provides open-source CAD tools for
    FPGA architecture and CAD research.
    """

    homepage = "https://verilogtorouting.org/"
    git = "https://github.com/verilog-to-routing/vtr-verilog-to-routing.git"

    maintainers("ueqri")  # For maintaining this package in the Spack community.

    variant("eigen3", default=True, description="Build VTR with Eigen 3 library")

    variant(
        "tbb",
        default=True,
        description="Build VTR with Intel Threading Building Blocks (TBB) library",
    )

    variant(
        "python",
        default=True,
        description="Install Python and required Python packages within Spack "
        + "environment (not system wide)",
    )

    # Shallow clones on the 'master' branch will hinder VTR build.
    version("master", branch="master", get_full_repo=True, preferred=True)
    version("2023_NoC_Placement", tag="v2023_NoC_Placement")
    version("8.0.0", tag="v8.0.0")

    # C++14 compilers are required.
    conflicts("%gcc@:6.1")
    conflicts("%clang@:3.4")

    depends_on("python@3.8:", type=("build", "run"), when="+python")
    depends_on("py-pip", type=("build", "run"), when="+python")
    depends_on("py-wheel", type=("build", "run"), when="+python")
    depends_on("py-setuptools", type="build", when="+python")

    # This dependency is different from what `spack compilers` lists (which were
    # used to compile the Spack packages). This is only used to compile Yosys,
    # which is included within the VTR codebase.
    depends_on("llvm@12: libcxx=project")

    depends_on("cmake@3.14:", type="build")
    depends_on("pkg-config", type="build")
    depends_on("ninja", type="build")
    depends_on("wget", type="build")
    depends_on("binutils", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    depends_on("libffi")
    depends_on("expat")
    depends_on("sqlite")
    depends_on("openssl")
    depends_on("libx11")
    depends_on("tk")
    depends_on("tcl")
    depends_on("cairo")
    depends_on("gtkplus@3:")

    depends_on("readline")
    depends_on("gawk")
    depends_on("graphviz")
    depends_on("py-xdot")
    depends_on("boost")
    depends_on("zlib")

    # Additional dependencies: Eigen and Intel TBB
    depends_on("eigen@3:", when="+eigen3")
    # FindTBB.cmake in the VTR does not work with latest TBB package layout.
    depends_on("intel-tbb@:2020.3", when="+tbb")

    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            try:
                include.extend(query.headers.directories)
            except spack.error.NoHeadersError:
                pass
            try:
                library.extend(query.libs.directories)
            except spack.error.NoLibrariesError:
                pass
        # Build uses a mix of Spack's compiler wrapper and the actual compiler
        # LLVM Clang. Therefore, it's necessary to set the following environment
        # variables in order to build specific components (i.e., Yosys) of VTR.
        env.set("CPATH", ":".join(include))
        env.set("LIBRARY_PATH", ":".join(library))

        # Add a missing libstdc++ rpath for yosys build which uses LLVM Clang.
        libstdcxx_dir = pjoin(os.path.dirname(os.path.dirname(self.compiler.cxx)), "lib")

        for lib_dir in [libstdcxx_dir, libstdcxx_dir + "64"] + library:
            if os.path.exists(lib_dir):
                env.append_flags("LDFLAGS", "-Wl,-rpath,{0}".format(lib_dir))

        env.set("PWD", self.build_directory)

    def build(self, spec, prefix):
        if self.spec.satisfies("+python") and not self.spec.satisfies("@8.0.0"):
            # Workaround for `UnicodeEncodeError: 'ascii' codec can't encode
            # characters in position ...` from pip output (the progress bar is
            # non-ascii).
            which("bash")("-c", "pip install -r requirements.txt --progress-bar off")
        make()

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set("VTR_ROOT", self.prefix)
