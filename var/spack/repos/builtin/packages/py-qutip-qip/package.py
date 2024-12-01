# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQutipQip(PythonPackage):
    """The QuTiP quantum information processing package"""

    homepage = "https://github.com/qutip/qutip-qip"
    url = "https://github.com/qutip/qutip-qip/archive/refs/tags/v0.2.2.tar.gz"
    # using github for now, because pypi tarball is missing the VERSION file
    # pypi = "qutip-qip/qutip-qip-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version("0.2.3", sha256="a6a3a549cf6983e3ecef2cf07d00be83c146321fb588e250a49d020788a4e590")
    version("0.2.2", sha256="4a9c79bb31c2fb2c72428764b2a5f6d8b1c667cebc8257cce1395c7e87d11217")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type=("build", "run"))

    depends_on("py-numpy@1.16.6:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))

    depends_on("py-qutip@4.6:", type=("build", "run"))
