# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWrapt(PythonPackage):
    """Module for decorators, wrappers and monkey patching."""

    homepage = "https://github.com/GrahamDumpleton/wrapt"
    pypi = "wrapt/wrapt-1.11.2.tar.gz"

    license("BSD-2-Clause")

    version("1.15.0", sha256="d06730c6aed78cee4126234cf2d071e01b44b915e725a6cb439a879ec9754a3a")
    version("1.14.1", sha256="380a85cf89e0e69b7cfbe2ea9f765f004ff419f34194018a6827ac0e3edfed4d")
    version("1.13.3", sha256="1fea9cd438686e6682271d36f3481a9f3636195578bab9ca3382e2f5f01fc185")
    version("1.12.1", sha256="b62ffa81fb85f4332a4f609cab4ac40709470da05643a082ec1eb88e6d9b97d7")
    version("1.11.2", sha256="565a021fd19419476b9362b05eeaa094178de64f8361e44468f9e9d7843901e1")
    version("1.11.1", sha256="4aea003270831cceb8a90ff27c4031da6ead7ec1886023b80ce0dfe0adf61533")
    version("1.10.10", sha256="42160c91b77f1bc64a955890038e02f2f72986c01d462d53cb6cb039b995cdd9")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@38.3:", type="build")
