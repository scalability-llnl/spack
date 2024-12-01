# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScooby(PythonPackage):
    """A Great Dane turned Python environment detective."""

    homepage = "https://github.com/banesullivan/scooby"
    pypi = "scooby/scooby-0.5.7.tar.gz"

    license("MIT")

    version("0.10.0", sha256="7ea33c262c0cc6a33c6eeeb5648df787be4f22660e53c114e5fff1b811a8854f")
    version("0.5.7", sha256="ae2c2b6f5f5d10adf7aaab32409028f1e28d3ce833664bdd1e8c2072e8da169a")

    # https://github.com/banesullivan/scooby/pull/83
    depends_on("python@:3.11", when="@:0.5", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", when="@0.10:", type="build")
