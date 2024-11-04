# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPydanticCore(PythonPackage):
    """Core functionality for Pydantic validation and serialization"""

    homepage = "https://github.com/pydantic/pydantic-core"
    pypi = "pydantic_core/pydantic_core-2.18.4.tar.gz"

    license("MIT", checked_by="qwertos")

    version("2.18.4", sha256="ec3beeada09ff865c344ff3bc2f427f5e6c26401cc6113d77e372c3fdac73864")

    depends_on("rust@1.76:", type="build")
    depends_on("py-maturin@1", type="build")
    depends_on("py-typing-extensions@4.6,4.7.1:", type="build")
