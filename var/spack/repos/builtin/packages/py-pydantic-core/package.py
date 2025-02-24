# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPydanticCore(PythonPackage):
    """Core functionality for Pydantic validation and serialization"""

    homepage = "https://github.com/pydantic/pydantic-core"
    pypi = "pydantic_core/pydantic_core-2.18.4.tar.gz"

    license("MIT", checked_by="qwertos")

    version("2.27.1", sha256="62a763352879b84aa31058fc931884055fd75089cccbd9d58bb6afd01141b235")
    version("2.18.4", sha256="ec3beeada09ff865c344ff3bc2f427f5e6c26401cc6113d77e372c3fdac73864")

    # Based on PyPI wheel availability
    depends_on("python@:3.13", type=("build", "run"))
    depends_on("python@:3.12", when="@:2.19", type=("build", "run"))
    depends_on("rust@1.76:", type="build")
    depends_on("py-maturin@1", type="build")
    depends_on("py-typing-extensions@4.6,4.7.1:", type="build")
