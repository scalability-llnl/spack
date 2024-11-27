# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Cvise(CMakePackage):
    """C-Vise is a super-parallel Python port of the C-Reduce. The port is
    fully compatible to the C-Reduce and uses the same efficient LLVM-based
    C/C++ reduction tool named clang_delta."""

    homepage = "https://github.com/marxin/cvise"
    url = "https://github.com/marxin/cvise"
    git = "https://github.com/marxin/cvise.git"

    license("NCSA")

    version("master", branch="master")
    version("2.10.0", tag="v2.10.0", commit="c8606497e354ddab273745cf823823bdd3e86bd8")
    version("2.7.0", tag="v2.7.0", commit="d9e4a50514d9931b2a1293755a7e96e0f9520032")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("pytest", default=False, description="Add py-pytest as dependency")
    variant("colordiff", default=False, description="Add colordiff support")

    depends_on("cmake@2.8.12:", type="build")
    depends_on("cmake@3.14:", when="@2.9:", type="build")
    depends_on("flex", type=("build", "run"))
    depends_on("llvm@9.0.0:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-pebble", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("unifdef", type=("build", "run"))

    depends_on("py-pytest", when="+pytest", type=("build", "run"))
    depends_on("colordiff", when="+colordiff", type=("build", "run"))

    # C-Vise doesn't directly depend on ncurses, but LLVM does. However, LLVM
    # doesn't provide correctly export terminfo CMake targets that it depends on
    # and C-Vise fails during configuration with ncurses +termlib.
    depends_on("ncurses ~termlib", when="^llvm +lldb")
