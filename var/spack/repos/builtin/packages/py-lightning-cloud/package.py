# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningCloud(PythonPackage):
    """Lightning AI Command Line Interface."""

    homepage = "https://lightning.ai/"
    pypi = "lightning_cloud/lightning_cloud-0.5.31.tar.gz"

    license("Apache-2.0")

    version("0.5.38", sha256="86fd5144b721bb289e9fd863604a67d55515688ccbadf0d858adfca1cefaf78f")
    version("0.5.37", sha256="1e0d577e1696e3aef974c589c4bd1ed22c70a332750863a393ec3949166137e0")
    version("0.5.36", sha256="990558d93a1b67d8bcbf8a87feb2ac455e13ec5223916ad2d5707d96df9558c9")
    version("0.5.31", sha256="a5a138f4abbeffe66ee476fb9a8d621befac0434ffeeeec1cc00ccd3d72ffc09")

    depends_on("py-setuptools", type="build")

    # requirements.txt
    depends_on("py-click", type=("build", "run"))
    depends_on("py-fastapi", when="@0.5.36:", type=("build", "run"))
    depends_on("py-fastapi+all", when="@:0.5.31", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-python-multipart", when="@0.5.36:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-urllib3", type=("build", "run"))
    depends_on("py-uvicorn", when="@0.5.36:", type=("build", "run"))
    depends_on("py-websocket-client", type=("build", "run"))
