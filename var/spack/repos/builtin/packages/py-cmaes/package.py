# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmaes(PythonPackage):
    """Lightweight Covariance Matrix Adaptation Evolution Strategy (CMA-ES) implementation."""

    homepage = "https://github.com/CyberAgentAILab/cmaes"
    pypi = "cmaes/cmaes-0.10.0.tar.gz"

    maintainers("eugeneswalker")

    license("MIT")

    version("0.10.0", sha256="48afc70df027114739872b50489ae6b32461c307b92d084a63c7090a9742faf9")

    depends_on("py-setuptools@61:", type="build")

    depends_on("py-numpy", type=("build", "run"))
