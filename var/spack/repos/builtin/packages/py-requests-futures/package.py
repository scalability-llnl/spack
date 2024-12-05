# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsFutures(PythonPackage):
    """Asynchronous Python HTTP Requests for Humans using Futures"""

    homepage = "https://github.com/ross/requests-futures"
    pypi = "requests-futures/requests-futures-1.0.0.tar.gz"

    license("Apache-2.0")

    version("1.0.0", sha256="35547502bf1958044716a03a2f47092a89efe8f9789ab0c4c528d9c9c30bc148")
    version("0.9.7", sha256="a9ca2c3480b6fac29ec5de59c146742e2ab2b60f8c68581766094edb52ea7bad")

    depends_on("py-setuptools@38.6.1:", type="build")
    depends_on("py-requests@1.2.0:", type=("build", "run"))
