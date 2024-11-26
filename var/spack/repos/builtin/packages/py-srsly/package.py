# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySrsly(PythonPackage):
    """srsly: Modern high-performance serialization utilities for Python."""

    homepage = "https://github.com/explosion/srsly"
    pypi = "srsly/srsly-2.0.1.tar.gz"

    license("MIT")

    version("2.4.6", sha256="47b41f323aba4c9c3311abf60e443c03a9efe9c69f65dc402d173c32f7744a6f")
    version("2.0.1", sha256="fa3c7375be8fe75f23c27feafbfb5f738d55ffdbf02964c6896fb7684f519a52")
    version("2.0.0", sha256="785b00e00406120dbef4ca82925051e6b60fe870c5f84f0d22b3632d574eb870")
    version("1.0.2", sha256="59258b81d567df207f8a0a33c4b5fa232afccf1d927c8ce3ba5395bfd64c0ed8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", when="@2:", type="build")
    depends_on("py-cython@0.25:", when="@2:", type="build")
    depends_on("py-catalogue@2.0.3:2.0", when="@2.4.6:", type=("build", "run"))

    # https://github.com/explosion/srsly/pull/24
    patch("subprocess.patch", when="@2.0.0:2.0.1")

    # https://github.com/explosion/srsly/pull/97
    conflicts("^py-cython@3:", when="@:2.4.6")
