# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Enzyme(CMakePackage):
    """
    The Enzyme project is a tool for performing reverse-mode automatic
    differentiation (AD) of statically-analyzable LLVM IR.
    This allows developers to use Enzyme to automatically create gradients
    of their source code without much additional work.
    """

    homepage = "https://enzyme.mit.edu"
    url = "https://github.com/wsmoses/Enzyme/archive/v0.0.15.tar.gz"
    list_url = "https://github.com/wsmoses/Enzyme/releases"
    git = "https://github.com/wsmoses/Enzyme"

    maintainers("wsmoses", "vchuravy", "tgymnich")

    root_cmakelists_dir = "enzyme"

    version("main", branch="main")
    version("0.0.135", sha256="49c798534faec7ba524a3ed053dd4352d690a44d3cad5a14915c9398dc9b175b")
    version("0.0.100", sha256="fbc53ec02adc0303ff200d7699afface2d9fbc7350664e6c6d4c527ef11c2e82")
    version("0.0.81", sha256="4c17d0c28f0572a3ab97a60f1e56bbc045ed5dd64c2daac53ae34371ca5e8b34")
    version("0.0.69", sha256="144d964187551700fdf0a4807961ceab1480d4e4cd0bb0fc7bbfab48fe053aa2")
    version("0.0.48", sha256="f5af62448dd2a8a316e59342ff445003581bc154f06b9b4d7a5a2c7259cf5769")
    version("0.0.32", sha256="9d42e42f7d0faf9beed61b2b1d27c82d1b369aeb9629539d5b7eafbe95379292")
    version("0.0.15", sha256="1ec27db0d790c4507b2256d851b256bf7e074eec933040e9e375d6e352a3c159")
    version("0.0.14", sha256="740641eeeeadaf47942ac88cc52e62ddc0e8c25767a501bed36ec241cf258b8d")
    version("0.0.13", sha256="d4a53964ec1f763772db2c56e6734269b7656c8b2ecd41fa7a41315bcd896b5a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("llvm@7:12", when="@0.0.13:0.0.15")
    depends_on("llvm@7:14", when="@0.0.32:0.0.47")
    depends_on("llvm@7:14", when="@0.0.48:0.0.68")
    depends_on("llvm@9:16", when="@0.0.69:0.0.79")
    depends_on("llvm@11:16", when="@0.0.80:0.0.99")
    depends_on("llvm@11:19", when="@0.0.100:")
    depends_on("cmake@3.13:", type="build")

    def cmake_args(self):
        spec = self.spec
        args = ["-DLLVM_DIR=" + spec["llvm"].prefix.lib + "/cmake/llvm"]
        return args

    @property
    def libs(self):
        ver = self.spec["llvm"].version.up_to(1)
        libs = ["LLVMEnzyme-{0}".format(ver), "ClangEnzyme-{0}".format(ver)]
        if self.version >= Version("0.0.32"):  # TODO actual lower bound
            libs.append("LLDEnzyme-{0}".format(ver))

        return find_libraries(libs, root=self.prefix, recursive=True)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Get the LLVMEnzyme and ClangEnzyme lib paths
        llvm, clang = self.libs

        if "LLVMEnzyme-" in clang:
            llvm, clang = clang, llvm

        env.set("LLVMENZYME", llvm)
        env.set("CLANGENZYME", clang)
