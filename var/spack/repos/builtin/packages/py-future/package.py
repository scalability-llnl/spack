# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuture(PythonPackage):
    """Clean single-source support for Python 3 and 2"""

    homepage = "https://python-future.org/"
    pypi = "future/future-0.18.2.tar.gz"
    git = "https://github.com/PythonCharmers/python-future.git"

    license("MIT")

    version("1.0.0", sha256="bd2968309307861edae1458a4f8a4f3598c03be43b97521076aebf5d94c07b05")
    version("0.18.3", sha256="34a17436ed1e96697a86f9de3d15a3b0be01d8bc8de9c1dffd59fb8234ed5307")
    version("0.18.2", sha256="b1bead90b70cf6ec3f0710ae53a525360fa360d306a86583adc6bf83a4db537d")
    version("0.17.1", sha256="67045236dcfd6816dc439556d009594abf643e5eb48992e36beac09c2ca659b8")
    version("0.17.0", sha256="eb6d4df04f1fb538c99f69c9a28b255d1ee4e825d479b9c62fc38c0cf38065a4")
    version("0.16.0", sha256="e39ced1ab767b5936646cedba8bcce582398233d6a627067d4c6a454c90cfedb")
    version("0.15.2", sha256="3d3b193f20ca62ba7d8782589922878820d0a023b885882deec830adbf639b97")

    depends_on("py-setuptools", type="build")

    @property
    def skip_modules(self):
        modules = []

        if "~tkinter" in self.spec["python"]:
            modules.extend(["tkinter", "future.moves.tkinter"])

        if self.spec.satisfies("@:0.17.1 ^python@3.10:"):
            # The Iterable abstract class was removed from collections in Python 3.10
            modules.extend(["future.backports", "past.types", "past.builtins"])

        return modules
