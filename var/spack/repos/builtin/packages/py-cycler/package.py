# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCycler(PythonPackage):
    """Composable style cycles."""

    homepage = "https://matplotlib.org/cycler/"
    pypi = "cycler/cycler-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version("0.11.0", sha256="9c87405839a19696e837b3b818fed3f5f69f16f1eec1a1ad77e043dcea9c772f")
    version("0.10.0", sha256="cd7b2d1018258d7247a71425e9f26463dfb444d411c39569972f4ce586b0c9d8")

    depends_on("python@3.6:", when="@0.11:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", when="@:0.10", type=("build", "run"))
