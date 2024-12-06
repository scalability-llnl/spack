# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiofiles(PythonPackage):
    """aiofiles is an Apache2 licensed library, written in Python, for
    handling local disk files in asyncio applications."""

    homepage = "https://github.com/Tinche/aiofiles"
    pypi = "aiofiles/aiofiles-0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.7.0", sha256="a1c4fc9b2ff81568c83e21392a82f344ea9d23da906e4f6a52662764545e19d4")
    version("0.5.0", sha256="98e6bcfd1b50f97db4980e182ddd509b7cc35909e903a8fe50d8849e02d815af")

    depends_on("python@3.6:3", when="@0.7:", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@0.7:", type="build")

    # Historical dependencies
    depends_on("py-setuptools", when="@:0.6", type="build")
