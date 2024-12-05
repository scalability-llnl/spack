# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypng(PythonPackage):
    """PyPNG allows PNG image files to be read and written using pure Python."""

    homepage = "https://gitlab.com/drj11/pypng"
    pypi = "pypng/pypng-0.0.20.tar.gz"

    maintainers("snehring")

    license("MIT")

    version(
        "0.20220715.0", sha256="739c433ba96f078315de54c0db975aee537cbc3e1d0ae4ed9aab0ca1e427e2c1"
    )
    version("0.0.20", sha256="1032833440c91bafee38a42c38c02d00431b24c42927feb3e63b104d8550170b")

    depends_on("py-setuptools@35.0.2:", type="build")
