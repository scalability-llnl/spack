# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nacos(MavenPackage):
    """Nacos is an easy-to-use platform designed for dynamic service
    discovery and configuration and service management. It helps you
    to build cloud native applications and microservices platform easily."""

    homepage = "https://nacos.io/"
    url = "https://github.com/alibaba/nacos/archive/1.3.2.tar.gz"

    license("Apache-2.0")

    version("1.3.2", sha256="3d3fdbe4033a9861a26c807d319db7c93f15de6491ddda512f9e5e421c563734")
