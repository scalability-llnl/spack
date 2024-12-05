# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGraphviz(PythonPackage):
    """Simple Python interface for Graphviz"""

    homepage = "https://github.com/xflr6/graphviz"
    pypi = "graphviz/graphviz-0.10.1.zip"

    license("MIT")

    version("0.13.2", sha256="60acbeee346e8c14555821eab57dbf68a169e6c10bce40e83c1bf44f63a62a01")
    version("0.13", sha256="dc08677f37c65a4a480f00df4bd0d19a0a103c06aad95f21a37f0b7fd440de81")
    version("0.12", sha256="c60e232a66e4847f9f644fbaa94730ca4f78385a1314a2cc1e7f4cb2d7461298")
    version("0.11.1", sha256="914b8b124942d82e3e1dcef499c9fe77c10acd3d18a1cfeeb2b9de05f6d24805")
    version("0.10.1", sha256="d311be4fddfe832a56986ac5e1d6e8715d7fcb0208560da79d1bb0f72abef41f")
    version("0.8.4", sha256="4958a19cbd8461757a08db308a4a15c3d586660417e1e364f0107d2fe481689f")

    variant("dev", default=False, description="development mode")
    variant("docs", default=False, description="build documentation")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:0.10.1")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@0.11.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-tox@3.0:", type=("build", "run"), when="+dev")
    depends_on("py-flake8", type=("build", "run"), when="+dev")
    depends_on("py-pep8-naming", type=("build", "run"), when="+dev")
    depends_on("py-wheel", type=("build", "run"), when="+dev")
    depends_on("py-twine", type=("build", "run"), when="+dev")
    depends_on("py-sphinx@1.7:", type=("build", "run"), when="+docs")
    depends_on("py-sphinx-rtd-theme", type=("build", "run"), when="+docs")
