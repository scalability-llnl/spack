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

    version("0.5.7", sha256="ae2c2b6f5f5d10adf7aaab32409028f1e28d3ce833664bdd1e8c2072e8da169a")

    depends_on("py-setuptools", type="build")
