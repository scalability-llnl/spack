# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStarlette(PythonPackage):
    """The little ASGI library that shines."""

    homepage = "https://github.com/encode/starlette"
    pypi = "starlette/starlette-0.23.1.tar.gz"

    license("BSD-3-Clause")

    version("0.41.2", sha256="9834fd799d1a87fd346deb76158668cfa0b0d56f85caefe8268e2d97c3468b62")
    version("0.37.2", sha256="9af890290133b79fc3db55474ade20f6220a364a0402e0b556e7cd5e1e093823")
    version("0.36.3", sha256="90a671733cfb35771d8cc605e0b679d23b992f8dcfad48cc60b38cb29aeb7080")
    version("0.35.1", sha256="3e2639dac3520e4f58734ed22553f950d3f3cb1001cd2eaac4d57e8cdc5f66bc")
    version("0.32.0", sha256="87c899fe3aee6a42f711380b03e1d244a21079529cb3dbe1a5109e60915e0bbb")
    version("0.28.0", sha256="7bf3da5e997e796cc202cef2bd3f96a7d9b1e1943203c2fe2b42e020bc658482")
    version("0.27.0", sha256="6a6b0d042acb8d469a01eba54e9cda6cbd24ac602c4cd016723117d6a7e73b75")
    version("0.23.1", sha256="8510e5b3d670326326c5c1d4cb657cc66832193fe5d5b7015a51c7b1e1b1bf42")
    version("0.22.0", sha256="b092cbc365bea34dd6840b42861bdabb2f507f8671e642e8272d2442e08ea4ff")

    depends_on("py-hatchling", type="build")

    depends_on("py-anyio@3.4:4", type=("build", "run"))
    depends_on("py-typing-extensions@3.10.0:", when="^python@:3.9", type=("build", "run"))
