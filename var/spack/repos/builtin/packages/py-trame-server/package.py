# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrameServer(PythonPackage):
    """Internal server side implementation of trame"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/Kitware/trame-server"
    pypi = "trame-server/trame-server-2.17.3.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("johnwparent")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("Apache-2.0", checked_by="johnwparent")

    version("2.17.3", sha256="1d6cbb0cd83f9073e895dfd32425ee29c751c8c3881dbb675bf8289c27058379")

    depends_on("py-setuptools@42:", type="build")
