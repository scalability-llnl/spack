# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMinrpc(PythonPackage):
    """Minimalistic RPC utility (only used within cpymad and pytao)."""

    homepage = "https://github.com/hibtc/minrpc"
    pypi = "minrpc/minrpc-0.0.11.tar.gz"

    license("GPL-3.0-only")

    version("0.0.11", sha256="bed53160f2774fdae7bd3d0fb5d1c77d17395394ec28a9e95a5859f486b54893")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
