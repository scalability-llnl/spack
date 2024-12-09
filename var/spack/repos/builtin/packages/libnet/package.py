# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnet(AutotoolsPackage):
    """Libnet is an API to help with the construction and handling of
    network packets. It provides a portable framework for low-level
    network packet writing and handling"""

    homepage = "https://github.com/libnet/libnet"
    url = "https://github.com/libnet/libnet/archive/v1.2.tar.gz"

    license("BSD-2-Clause")

    version("1.3", sha256="44e28a4e5a9256ce74d96fd1ad8ac2e3f300f55dc70c93bb81851183a21d7d3a")
    version("1.2", sha256="b7a371a337d242c017f3471d70bea2963596bec5bd3bd0e33e8517550e2311ef")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
