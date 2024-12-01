# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRapidfuzz(PythonPackage):
    """Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance."""

    homepage = "https://github.com/maxbachmann/rapidfuzz"
    pypi = "rapidfuzz/rapidfuzz-1.8.2.tar.gz"

    license("MIT")

    version("3.3.1", sha256="6783b3852f15ed7567688e2e358757a7b4f38683a915ba5edc6c64f1a3f0b450")
    version("2.2.0", sha256="acb8839aac452ec61a419fdc8799e8a6e6cd21bed53d04678cdda6fba1247e2f")
    version("1.8.2", sha256="d6efbb2b6b18b3a67d7bdfbcd9bb72732f55736852bbef823bdf210f9e0c6c90")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools@42:", when="@2:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-build@0.17", when="@3:", type="build")
    depends_on("py-scikit-build@0.13:", when="@2.2:", type="build")
    depends_on("py-rapidfuzz-capi@1.0.5", when="@2", type="build")
    depends_on("py-jarowinkler@1.2.0:1", when="@2", type=("build", "run"))

    # CMakeLists.txt
    depends_on("cmake@3.12:", type="build")
    depends_on("ninja", type="build")
