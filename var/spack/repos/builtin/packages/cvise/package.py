# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    maintainers = ["olupton"]

    version("develop", branch="master")
    version("2.7.0", tag="v2.7.0")
    version("2.4.0", tag="v2.4.0")
    version("2.3.0", tag="v2.3.0")

    variant("pytest", default=False, description="Add py-pytest as dependency")

    depends_on("cmake", type="build")
    depends_on("flex", type=("build", "run"))
    depends_on("llvm@9.0.0:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-pebble", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("unifdef", type=("build", "run"))
    depends_on("py-pytest", when="+pytest", type=("build", "run"))

    # depends_on("colordiff", type=("build", "run"))
    # depends_on("libxml2", type=("build", "run"))
    # depends_on("ncurses", type=("build", "run"))  # this is an llvm dependency really
    # depends_on("zlib", type=("build", "run"))

    def cmake_args(self):
        return ["-DPYTHON_EXECUTABLE=" + self.spec["python"].command.path]
