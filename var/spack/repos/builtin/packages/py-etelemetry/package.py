# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEtelemetry(PythonPackage):
    """A lightweight python client to communicate with the etelemetry server"""

    homepage = "https://github.com/sensein/etelemetry-client"
    url = "https://github.com/sensein/etelemetry-client/archive/refs/tags/v0.2.2.tar.gz"

    license("Apache-2.0")

    version("0.3.0", sha256="5f710fdb17ec02f93be29d234b33c1c62ad641320d1b4047e61044679018de03")
    version("0.2.2", sha256="bfec416552d248ad0f50b90ba5ff015e825ad70e4a87f7a06cc7da6d19152897")

    depends_on("python@3.7:", when="@0.3:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-ci-info@0.2.0:", type=("build", "run"))
