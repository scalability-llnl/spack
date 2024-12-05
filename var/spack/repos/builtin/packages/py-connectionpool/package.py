# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConnectionpool(PythonPackage):
    """Thread-safe connection pool for python."""

    homepage = "https://github.com/zhouyl/ConnectionPool"
    pypi = "connection_pool/connection_pool-0.0.3.tar.gz"
    maintainers("marcusboden")

    license("MIT")

    version("0.0.3", sha256="bf429e7aef65921c69b4ed48f3d48d3eac1383b05d2df91884705842d974d0dc")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
