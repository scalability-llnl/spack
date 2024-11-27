# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiodns(PythonPackage):
    """Simple DNS resolver for asyncio.It provides a simple way for
    doing asynchronous DNS resolutions using pycares."""

    homepage = "https://pypi.org/project/aiodns/"
    pypi = "aiodns/aiodns-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="815fdef4607474295d68da46978a54481dd1e7be153c7d60f9e72773cd38d77d")
    version("1.2.0", sha256="d67e14b32176bcf3ff79b5d47c466011ce4adeadfa264f7949da1377332a0449")
    version("1.1.1", sha256="d8677adc679ce8d0ef706c14d9c3d2f27a0e0cc11d59730cdbaf218ad52dd9ea")

    depends_on("py-setuptools", type="build")
    depends_on("py-pycares@3.0.0:", type=("build", "run"))
