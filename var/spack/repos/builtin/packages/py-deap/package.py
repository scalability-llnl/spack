# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeap(PythonPackage):
    """Distributed Evolutionary Algorithms in Python."""

    homepage = "https://deap.readthedocs.org/"
    pypi = "deap/deap-1.3.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("1.3.3", sha256="8772f1b0fff042d5e516b0aebac2c706243045aa7d0de8e0b8658f380181cf31")
    version("1.3.1", sha256="11f54493ceb54aae10dde676577ef59fc52d52f82729d5a12c90b0813c857a2f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    # uses 2to3
    depends_on("py-setuptools@:57", type="build", when="@1.3.1")
    depends_on("py-numpy", type=("build", "run"))
