# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydanticSettings(PythonPackage):
    """Settings management using Pydantic."""

    homepage = "https://github.com/pydantic/pydantic-settings"
    pypi = "pydantic_settings/pydantic_settings-2.6.1.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("2.6.1", sha256="e0f92546d8a9923cb8941689abf85d6601a8c19a23e97a34b2964a2e3f813ca0")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-pydantic@2.7.0:", type=("build", "run"))
    depends_on("py-python-dotenv@0.21:", type=("build", "run"))
