# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningFabric(PythonPackage):
    """Fabric is the fast and lightweight way to scale PyTorch models without boilerplate."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "lightning-fabric/lightning-fabric-2.0.0.tar.gz"

    license("Apache-2.0")

    version("2.0.0", sha256="56ecf23e2857f76cc1ca4528cc314b884fed1541182d4e8b130e3c2efd39c896")

    # src/lightning_fabric/__setup__.py
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # requirements/fabric/base.txt
    depends_on("py-numpy@1.17.2:", type=("build", "run"))
    depends_on("py-torch@1.11:", type=("build", "run"))
    depends_on("py-fsspec@2021.06.1:+http", type=("build", "run"))
    depends_on("py-packaging@17.1:", type=("build", "run"))
    depends_on("py-typing-extensions@4:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.7:", type=("build", "run"))
