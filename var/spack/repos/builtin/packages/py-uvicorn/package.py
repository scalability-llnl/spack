# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUvicorn(PythonPackage):
    """The lightning-fast ASGI server."""

    homepage = "https://www.uvicorn.org/"
    pypi = "uvicorn/uvicorn-0.27.1.tar.gz"

    license("BSD-3-Clause")

    version("0.27.1", sha256="3d9a267296243532db80c83a959a3400502165ade2c1338dea4e67915fd4745a")
    version("0.20.0", sha256="a4e12017b940247f836bc90b72e725d7dfd0c8ed1c51eb365f5ba30d9f5127d8")

    variant("standard", default=False, description="Build standard dependencies")

    depends_on("py-hatchling", type="build")
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-h11@0.8:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@4:", when="^python@:3.10", type=("build", "run"))

    with when("+standard"):
        depends_on("py-colorama@0.4:", when="platform=windows", type=("build", "run"))
        depends_on("py-httptools@0.5:", type=("build", "run"))
        depends_on("py-python-dotenv@0.13:", type=("build", "run"))
        depends_on("py-pyyaml@5.1:", type=("build", "run"))
        depends_on("py-uvloop@0.14,0.15.2:", when="platform=linux", type=("build", "run"))
        depends_on("py-uvloop@0.14,0.15.2:", when="platform=darwin", type=("build", "run"))
        depends_on("py-watchfiles@0.13:", type=("build", "run"))
        depends_on("py-websockets@10.4:", type=("build", "run"))
