# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH2(PythonPackage):
    """HTTP/2 State-Machine based protocol implementation"""

    homepage = "https://github.com/python-hyper/hyper-h2"
    pypi = "h2/h2-4.0.0.tar.gz"

    license("MIT")

    version("4.1.0", sha256="a83aca08fbe7aacb79fec788c9c0bac936343560ed9ec18b82a13a12c28d2abb")
    version("4.0.0", sha256="bb7ac7099dd67a857ed52c815a6192b6b1f5ba6b516237fc24a085341340593d")
    version("3.2.0", sha256="875f41ebd6f2c44781259005b157faed1a5031df3ae5aa7bcb4628a6c0782f14")

    depends_on("python@3.6.1:", type=("build", "run"), when="@4.0.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-hyperframe@5.2:5", type=("build", "run"), when="@3.2.0")
    depends_on("py-hyperframe@6.0:6", type=("build", "run"), when="@4.0.0:")
    depends_on("py-hpack@3.0:3", type=("build", "run"), when="@3.2.0")
    depends_on("py-hpack@4.0:4", type=("build", "run"), when="@4.0.0:")
