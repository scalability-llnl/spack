# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIncremental(PythonPackage):
    """A small library that versions your Python projects."""

    homepage = "https://github.com/twisted/incremental"
    pypi = "incremental/incremental-21.3.0.tar.gz"

    license("MIT")

    version("24.7.2", sha256="fb4f1d47ee60efe87d4f6f0ebb5f70b9760db2b2574c59c8e8912be4ebd464c9")
    version("21.3.0", sha256="02f5de5aff48f6b9f665d99d48bfc7ec03b6e3943210de7cfc88856d755d6f57")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.0:", type="build", when="@24.7:")
    depends_on("py-tomli", type=("build", "run"), when="@24.7: ^python@:3.10")
