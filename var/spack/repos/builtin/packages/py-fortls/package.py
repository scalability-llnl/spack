# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortls(PythonPackage):
    """A Language Server for Fortran providing code completion, diagnostics, hovering and more."""

    homepage = "https://fortls.fortran-lang.org"
    pypi = "fortls/fortls-2.13.0.tar.gz"

    maintainers("RMeli")

    license("MIT")

    version("3.1.0", sha256="e38f9f6af548f78151d54bdbb9884166f8d717f8e147ab1e2dbf06b985df2c6d")
    version("2.13.0", sha256="23c5013e8dd8e1d65bf07be610d0827bc48aa7331a7a7ce13612d4c646d0db31")

    depends_on("fortran", type="build")  # generated

    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools@61:", when="@3:", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-setuptools-scm@7:+toml", when="@3:", type="build")
    depends_on("py-setuptools-scm-git-archive", when="@:2", type="build")

    depends_on("py-json5", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.7")
