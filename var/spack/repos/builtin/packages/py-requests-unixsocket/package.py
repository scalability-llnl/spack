# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsUnixsocket(PythonPackage):
    """Use requests to talk HTTP via a UNIX domain socket."""

    homepage = "https://github.com/msabramo/requests-unixsocket"
    pypi = "requests-unixsocket/requests-unixsocket-0.2.0.tar.gz"

    license("Apache-2.0")

    version("0.3.0", sha256="28304283ea9357d45fff58ad5b11e47708cfbf5806817aa59b2a363228ee971e")
    version("0.2.0", sha256="9e5c1a20afc3cf786197ae59c79bcdb0e7565f218f27df5f891307ee8817c1ea")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
    depends_on("py-requests@1.1:", type=("build", "run"))
    depends_on("py-urllib3@1.8:", when="@:0.2.0", type=("build", "run"))
