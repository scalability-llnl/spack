# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrameServer(PythonPackage):
    """Internal server side implementation of trame"""

    homepage = "https://github.com/Kitware/trame-server"
    pypi = "trame-server/trame-server-2.17.3.tar.gz"

    maintainers("johnwparent")

    license("Apache-2.0", checked_by="johnwparent")

    version("2.17.3", sha256="1d6cbb0cd83f9073e895dfd32425ee29c751c8c3881dbb675bf8289c27058379")

    depends_on("py-setuptools@42:", type="build")
