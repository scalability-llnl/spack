# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPipenv(PythonPackage):
    """Python virtualenv management tool that  supports a multitude of systems."""

    homepage = "https://pypi.org/project/pipenv/#description"
    pypi = "pipenv/pipenv-2023.9.7.tar.gz"

    version("2023.9.7", sha256="6de1c34666e144fe84aa893ecbe012218350802657eef67feccc6b4f0e3002b5")

    depends_on("python@2.X:2.Y,3.Z:", type=("build", "run"))
    depends_on("py-pip@X.Y:", type="build")
    depends_on("py-wheel@X.Y:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-hatchling", type="build")
    depends_on("py-flit-core", type="build")
    depends_on("py-poetry-core", type="build")
