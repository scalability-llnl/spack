# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPid(PythonPackage):
    """Pidfile featuring stale detection and file-locking, can also be
    used as context-manager or decorator."""

    homepage = "https://github.com/trbs/pid/"
    url = "https://github.com/trbs/pid/archive/3.0.3.tar.gz"

    license("Apache-2.0")

    version("3.0.3", sha256="082281e2f6b99b4aaa02a24ae4796c604ac17f19cdd0327b8c1ba9c2e73aadc8")
    version("3.0.2", sha256="0be7dc260e35788163b3171a5f0e1a8b9888bc2b77232c053c042a65496b8396")
    version("3.0.1", sha256="2f51b61210f8e1f009b09a2034717003ca22dcd86995537ecb857863bddca89a")
    version("3.0.0", sha256="3d251eadedc6fbd1fe4b43d521e76b83afd244b8b1951a2cd96864406bc96381")
    version("2.2.5", sha256="d4c68554bf4b2fc7d0b50749f535f5c1fceb74ff025ce1a3f06745d15c595d40")
    version("2.2.4", sha256="de3cc35e18c5409d8424813ab422b637af4d25bfdcf2c15ee6c5af447778de22")
    version("2.2.3", sha256="14555fc214e0dfee7d94598b759523349832597e163415d1a7b0d87d9902cc47")
    version("2.2.2", sha256="716bb5803fed50facdb62be0e48d08dd95e7392fcfb03f5540915623f9c4ee44")
    version("2.2.1", sha256="2c5b398d348b8b1901ccb29b5c914c583187692acfbc3c28fc4ee483b9909357")
    version("2.2.0", sha256="f2c3beb5742159794379b73088eb3f592a4b7b93bfef95f8bbc27ab98e5394ed")

    depends_on("py-setuptools", type="build")
