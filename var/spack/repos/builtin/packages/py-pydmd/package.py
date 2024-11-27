# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydmd(PythonPackage):
    """PyDMD is a Python package that uses Dynamic Mode Decomposition
    for a data-driven model simplification based on spatiotemporal
    coherent structures."""

    homepage = "https://mathlab.github.io/PyDMD/"
    url = "https://github.com/mathLab/PyDMD/archive/v0.3.tar.gz"

    license("MIT")

    version("0.3", sha256="f490fc139677e4d9fc1240636a2c5992d22879517c9574d13164dc5179b0f785")

    variant("docs", default=False, description="Build HTML documentation")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-nose", type="test")
    depends_on("texlive", type="build", when="+docs")
    depends_on("py-sphinx@1.4.0:1.4", type="build", when="+docs")
    depends_on("py-sphinx-rtd-theme", type="build", when="+docs")

    # https://github.com/mathLab/PyDMD/pull/133
    patch("isuue-133.patch", when="@0.3")

    @run_after("install")
    def install_docs(self):
        if "+docs" in self.spec:
            with working_dir("docs"):
                make("html")
            install_tree("docs", self.prefix.docs)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        python("test.py")
