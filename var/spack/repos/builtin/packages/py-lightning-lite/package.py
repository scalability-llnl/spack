# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningLite(PythonPackage):
    """LightningLite enables pure PyTorch users to scale their existing code on any kind
    of device while retaining full control over their own loops and optimization logic."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "lightning-lite/lightning-lite-1.8.0.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("1.8.0", sha256="a71940409d3d1a5bb20f63716c86a745157ce30100f1c16600dfe33d9b657955")

    # src/lightning_lite/__setup__.py
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # requirements/lite/base.txt
    depends_on("py-numpy@1.17.2:", type=("build", "run"))
    depends_on("py-torch@1.9:", type=("build", "run"))
    depends_on("py-fsspec@2021.06.1:+http", type=("build", "run"))
    depends_on("py-packaging@17:", type=("build", "run"))
    depends_on("py-typing-extensions@4:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.3", type=("build", "run"))
