# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchdiffeq(PythonPackage):
    """ODE solvers and adjoint sensitivity analysis in PyTorch."""

    homepage = "https://github.com/rtqichen/torchdiffeq"
    pypi = "torchdiffeq/torchdiffeq-0.2.3.tar.gz"

    license("MIT")

    version("0.2.3", sha256="fe75f434b9090ac0c27702e02bed21472b0f87035be6581f51edc5d4013ea31a")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.3:", type=("build", "run"))
    depends_on("py-scipy@1.4:", type=("build", "run"))
