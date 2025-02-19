# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyonmttok(CMakePackage, PythonExtension):
    """Python wrapper for OpenNMT/Tokenizer, a fast and customizable text
    tokenization library with BPE and SentencePiece support."""

    homepage = "https://github.com/OpenNMT/Tokenizer/"
    git = "https://github.com/OpenNMT/Tokenizer.git"

    maintainers("meyersbs", "aweits")

    version("1.37.1", tag="v1.37.1", submodules=True)

    extends("python")

    # Uses setuptools.installer, deprecated in:
    # https://setuptools.pypa.io/en/stable/history.html#v59-1-0
    depends_on("py-setuptools@:59.0.1", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("py-pip@19.3:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("python@3.6:3.11", type=("build", "run"))
    depends_on("cmake@3.1.0:", type="build")
    depends_on("py-pytest-runner", type="build")

    variant("cli", default=True, description="Build CLI")

    def setup_build_environment(self, env):
        env.append_path("SPACK_INCLUDE_DIRS", self.prefix.include)
        env.append_path("SPACK_LINK_DIRS", self.prefix.lib)
        env.append_path("SPACK_LINK_DIRS", self.prefix.lib64)

    @run_after("install")
    def install_python(self):
        args = std_pip_args + ["--prefix=" + prefix, "."]
        with working_dir("bindings/python"):
            pip(*args)

    def cmake_args(self):
        args = []
        # From README
        if "+cli" in self.spec:
            args.append("-DLIB_ONLY=OFF")
        else:
            args.append("-DLIB_ONLY=ON")
        return args
