# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsCpp(PythonPackage):
    """Simplified packaging for pybind11-based C++ extensions"""

    homepage = "https://github.com/dmontagu/setuptools-cpp"
    pypi = "setuptools_cpp/setuptools_cpp-0.1.0.tar.gz"

    maintainers("dorton")

    license("MIT")

    version("0.1.0", sha256="4fd5e08603237578d06d28efd592d9847b523ede3e502f660be44b1e6254674d")

    depends_on("py-setuptools", type="build")
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-atomicwrites", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-black", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-coverage", type=("build", "run"))
    depends_on("py-entrypoints", type=("build", "run"))
    depends_on("py-flake8", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"))
    depends_on("py-isort", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-markupsafe", type=("build", "run"))
    depends_on("py-mccabe", type=("build", "run"))
    depends_on("py-more-itertools", type=("build", "run"))
    depends_on("py-mypy", type=("build", "run"))
    depends_on("py-mypy-extensions", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pathspec", type=("build", "run"))
    depends_on("py-pluggy", type=("build", "run"))
    depends_on("py-tornado", type=("build", "run"))
    depends_on("py-typed-ast", type=("build", "run"))
