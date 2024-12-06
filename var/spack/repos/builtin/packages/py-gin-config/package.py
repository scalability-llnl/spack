# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGinConfig(PythonPackage):
    """Gin provides a lightweight configuration framework for
    Python, based on dependency injection."""

    homepage = "https://github.com/google/gin-config"
    pypi = "gin-config/gin-config-0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.5.0", sha256="0c6ea5026ded927c8c93c990b01c695257c1df446e45e549a158cfbc79e19ed6")

    depends_on("py-setuptools", type="build")
