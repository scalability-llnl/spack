# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStarletteContext(PythonPackage):
    """Access context in Starlette"""

    homepage = "https://github.com/tomwojcik/starlette-context"
    pypi = "starlette-context/starlette_context-0.3.5.tar.gz"

    license("MIT")

    version("0.3.5", sha256="e6b9f905823860e9e36c013dbfcf770562f3b88bec21cb861fef2e0bd0615697")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-starlette", type=("build", "run"))
