# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    url = "https://github.com/FEniCS/ffcx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("0.9.0", sha256="afa517272a3d2249f513cb711c50b77cf8368dd0b8f5ea4b759142229204a448")
    version("0.8.0", sha256="8a854782dbd119ec1c23c4522a2134d5281e7f1bd2f37d64489f75da055282e3")
    version("0.7.0", sha256="7f3c3ca91d63ce7831d37799cc19d0551bdcd275bdfa4c099711679533dd1c71")
    version("0.6.0", sha256="076fad61d406afffd41019ae1abf6da3f76406c035c772abad2156127667980e")

    depends_on("python@3.9:", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:", when="@:0.7", type=("build", "run"))
    depends_on("py-setuptools@62:", when="@0.7:", type="build")
    # Runtime dependency on pkg_resources from setuptools at 0.6.0
    depends_on("py-setuptools@58:", when="@:0.6", type=("build", "run"))

    # CFFI is required at runtime for JIT support
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))

    depends_on("py-fenics-ufl@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ufl@2024.2.0:", type=("build", "run"), when="@0.9")
    depends_on("py-fenics-ufl@2024.1.0:", type=("build", "run"), when="@0.8")
    depends_on("py-fenics-ufl@2023.2.0", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ufl@2023.1", type=("build", "run"), when="@0.6")

    depends_on("py-fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-basix@0.9", type=("build", "run"), when="@0.9")
    depends_on("py-fenics-basix@0.8", type=("build", "run"), when="@0.8")
    depends_on("py-fenics-basix@0.7", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-basix@0.6", type=("build", "run"), when="@0.6")

    depends_on("py-pytest@6:", type="test")
    depends_on("py-sympy", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            pytest = which("pytest")
            pytest("--ignore=test_cmdline.py")
