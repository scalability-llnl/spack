# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsScm(PythonPackage):
    """The blessed package to manage your versions by scm tags."""

    homepage = "https://github.com/pypa/setuptools_scm"
    pypi = "setuptools_scm/setuptools_scm-4.1.2.tar.gz"
    tags = ["build-tools"]

    license("MIT")

    version("8.0.4", sha256="b5f43ff6800669595193fd09891564ee9d1d7dcb196cab4b2506d53a2e1c95c7")
    version("7.1.0", sha256="6c508345a771aad7d56ebff0e70628bf2b0ec7573762be9960214730de278f27")
    version("7.0.5", sha256="031e13af771d6f892b941adb6ea04545bbf91ebc5ce68c78aaf3fff6e1fb4844")
    version("7.0.3", sha256="cf8ab8e235bed840cd4559b658af0d8e8a70896a191bbc510ee914ec5325332d")
    version("6.3.2", sha256="a49aa8081eeb3514eb9728fa5040f2eaa962d6c6f4ec9c32f6c1fba88f88a0f2")
    version("6.0.1", sha256="d1925a69cb07e9b29416a275b9fadb009a23c148ace905b2fb220649a6c18e92")
    version("5.0.2", sha256="83a0cedd3449e3946307811a4c7b9d89c4b5fd464a2fb5eeccd0a5bb158ae5c8")
    version("4.1.2", sha256="a8994582e716ec690f33fec70cca0f85bd23ec974e3f783233e4879090a7faa8")
    version("3.5.0", sha256="5bdf21a05792903cafe7ae0c9501182ab52497614fa6b1750d9dbae7b60c1a87")
    version("3.3.3", sha256="bd25e1fb5e4d603dcf490f1fde40fb4c595b357795674c3e5cb7f6217ab39ea5")
    version("3.1.0", sha256="1191f2a136b5e86f7ca8ab00a97ef7aef997131f1f6d4971be69a1ef387d8b40")
    version("1.15.6", sha256="49ab4685589986a42da85706b3311a2f74f1af567d39fee6cb1e088d7a75fb5f")

    # Basically a no-op in setuptools_scm 7+, toml support is always built
    variant("toml", default=True, description="Build with TOML support")

    depends_on("python@3.7:", when="@7:", type=("build", "run"))
    depends_on("python@3.6:", when="@6:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))

    depends_on("py-packaging@20.0:", when="@6.3:", type=("build", "run"))
    depends_on("py-setuptools@61:", when="@8:", type=("build", "run"))
    depends_on("py-setuptools@45:", when="@6:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@5:", type=("build", "run"))
    depends_on("py-setuptools@34.4:", type=("build", "run"))
    depends_on("py-toml", when="+toml @:6.1.0", type=("build", "run"))
    depends_on("py-tomli@1:", when="+toml @6.1.0:", type=("build", "run"))
    depends_on("py-tomli@1:", when="@7.0", type=("build", "run"))
    depends_on("py-tomli@1:", when="@7.1: ^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions", when="@7:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@7: ^python@:3.7", type=("build", "run"))

    depends_on("git", type=("build", "run"))

    def url_for_version(self, version):
        # setuptools_scm-7.1.0.tar.gz with an underscore became
        # setuptools-scm-8.0.4.tar.gz with a dash
        url = super().url_for_version(version)
        if version >= Version(8):
            return url.replace("_", "-")
        return url
