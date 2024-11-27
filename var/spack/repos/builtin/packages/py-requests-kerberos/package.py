# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsKerberos(PythonPackage):
    """An authentication handler for using Kerberos with Python Requests."""

    homepage = "https://github.com/requests/requests-kerberos"
    pypi = "requests_kerberos/requests_kerberos-0.15.0.tar.gz"

    maintainers("wdconinc")

    license("ISC", checked_by="wdconinc")

    version("0.15.0", sha256="437512e424413d8113181d696e56694ffa4259eb9a5fc4e803926963864eaf4e")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-requests@1.1.0:", type=("build", "run"))
    depends_on("py-cryptography@1.3:", type=("build", "run"))
    depends_on("py-pyspnego +kerberos", type=("build", "run"))
