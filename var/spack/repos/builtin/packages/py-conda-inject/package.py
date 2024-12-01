# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCondaInject(PythonPackage):
    """Helper functions for injecting a conda environment into the current python environment."""

    pypi = "conda_inject/conda_inject-1.3.1.tar.gz"

    license("MIT")

    version("1.3.1", sha256="9e8d902230261beba74083aae12c2c5a395e29b408469fefadc8aaf51ee441e5")

    depends_on("py-pyyaml@6", type=("build", "run"))

    depends_on("python@3.9:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
