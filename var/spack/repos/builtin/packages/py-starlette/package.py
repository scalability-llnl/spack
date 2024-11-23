# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStarlette(PythonPackage):
    """The little ASGI library that shines."""

    homepage = "https://github.com/encode/starlette"
    pypi = "starlette/starlette-0.36.3.tar.gz"

    license("BSD-3-Clause")

    version("0.36.3", sha256="90a671733cfb35771d8cc605e0b679d23b992f8dcfad48cc60b38cb29aeb7080")
    version("0.27.0", sha256="6a6b0d042acb8d469a01eba54e9cda6cbd24ac602c4cd016723117d6a7e73b75")
    version("0.23.1", sha256="8510e5b3d670326326c5c1d4cb657cc66832193fe5d5b7015a51c7b1e1b1bf42")
    version("0.22.0", sha256="b092cbc365bea34dd6840b42861bdabb2f507f8671e642e8272d2442e08ea4ff")

    depends_on("py-hatchling", type="build")

    depends_on("py-anyio@3.4:4", type=("build", "run"))
    depends_on("py-typing-extensions@3.10.0:", when="^python@:3.9", type=("build", "run"))
