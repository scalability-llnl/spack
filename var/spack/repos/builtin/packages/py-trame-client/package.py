# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrameClient(PythonPackage):
    """Internal client side implementation of trame"""

    homepage = "https://github.com/Kitware/trame-client"
    pypi = "trame-client/trame-client-2.17.1.tar.gz"

    maintainers("johnwparent")

    license("Apache-2.0", checked_by="johnwparent")

    version("2.17.1", sha256="0841e569d0792c7fc218a502663c814ad69e318d2885cec82a7fe1d07fdf0bf4")

    depends_on("py-setuptools@42:", type="build")
