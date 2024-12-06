# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStopit(PythonPackage):
    """
    Raise asynchronous exceptions in other threads, control the timeout of
    blocks or callables with two context managers and two decorators.
    """

    pypi = "stopit/stopit-1.1.2.tar.gz"

    license("MIT")

    version("1.1.2", sha256="f7f39c583fd92027bd9d06127b259aee7a5b7945c1f1fa56263811e1e766996d")

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
