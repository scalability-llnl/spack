# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCloudauthz(PythonPackage):
    """Implements means of authorization delegation on cloud-based resource providers."""

    homepage = "https://github.com/galaxyproject/cloudauthz"
    pypi = "cloudauthz/cloudauthz-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="7e62f3ae04b1842540ca484717d40bd9ec17c6764dd842c1f73f6290b9b54ac1")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests@2.18.4:", type=("build", "run"))
    depends_on("py-adal@1.0.2:", type=("build", "run"))
