# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBilliard(PythonPackage):
    """Python multiprocessing fork with improvements and bugfixes"""

    pypi = "billiard/billiard-3.5.0.5.tar.gz"

    license("BSD-3-Clause")

    version("4.2.0", sha256="9a3c3184cb275aa17a732f93f65b20c525d3d9f253722d26a82194803ade5a2c")
    version("3.6.4.0", sha256="299de5a8da28a783d51b197d496bef4f1595dd023a93a4f59dde1886ae905547")
    version("3.6.3.0", sha256="d91725ce6425f33a97dfa72fb6bfef0e47d4652acd98a032bd1a7fbf06d5fa6a")
    version("3.6.1.0", sha256="b8809c74f648dfe69b973c8e660bcec00603758c9db8ba89d7719f88d5f01f26")
    version("3.6.0.0", sha256="756bf323f250db8bf88462cd042c992ba60d8f5e07fc5636c24ba7d6f4261d84")
    version("3.5.0.5", sha256="42d9a227401ac4fba892918bba0a0c409def5435c4b483267ebfe821afaaba0e")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
