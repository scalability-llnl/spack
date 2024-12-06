# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNoseCov(PythonPackage):
    """This plugin produces coverage reports."""

    pypi = "nose-cov/nose-cov-1.6.tar.gz"

    license("MIT")

    version("1.6", sha256="8bec0335598f1cc69e3262cc50d7678c1a6010fa44625ce343c4ec1500774412")

    depends_on("py-setuptools", type="build")
    depends_on("py-nose@0.11.4:", type=("build", "run"))
    depends_on("py-cov-core@1.6:", type=("build", "run"))
