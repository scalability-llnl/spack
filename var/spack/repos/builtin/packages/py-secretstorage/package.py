# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySecretstorage(PythonPackage):
    """Python bindings to FreeDesktop.org Secret Service API."""

    homepage = "https://github.com/mitya57/secretstorage"
    pypi = "SecretStorage/SecretStorage-3.1.2.tar.gz"

    license("BSD-3-Clause")

    version("3.3.3", sha256="2403533ef369eca6d2ba81718576c5e0f564d5cca1b58f73a8b23e7d4eeebd77")
    version("3.3.1", sha256="fd666c51a6bf200643495a04abb261f83229dcb6fd8472ec393df7ffc8b6f195")
    version("3.1.2", sha256="15da8a989b65498e29be338b3b279965f1b8f09b9668bd8010da183024c8bff6")
    version("2.3.1", sha256="3af65c87765323e6f64c83575b05393f9e003431959c9395d1791d51497f29b6")

    depends_on("python@3.6:", when="@3.3:", type=("build", "run"))
    depends_on("python@3.5:", when="@3.0:3.2", type=("build", "run"))
    depends_on("py-setuptools@30.3:", when="@3:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cryptography@2.0:", when="@3.2:", type=("build", "run"))
    depends_on("py-cryptography", when="@:3.1", type=("build", "run"))
    depends_on("py-jeepney@0.6:", when="@3.3:", type=("build", "run"))
    depends_on("py-jeepney@0.4.2:", when="@3.0:3.2", type=("build", "run"))
