# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySocialAuthCore(PythonPackage):
    """Python social authentication made simple."""

    homepage = "https://github.com/python-social-auth/social-core"
    pypi = "social-auth-core/social-auth-core-4.3.0.tar.gz"

    license("BSD-3-Clause")

    version("4.3.0", sha256="4686f0e43cf12954216875a32e944847bb1dc69e7cd9573d16a9003bb05ca477")
    version("4.0.3", sha256="694eb355825cd72d3346afb816dd899493be1a8ee7405945d2e989cabed10cf2")

    variant("openidconnect", default=False, description="Install requirements for openidconnect")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests@2.9.1:", type=("build", "run"))
    depends_on("py-oauthlib@1.0.3:", type=("build", "run"))
    depends_on("py-requests-oauthlib@0.6.1:", type=("build", "run"))
    depends_on("py-pyjwt@2.0.0:", type=("build", "run"))
    depends_on("py-cryptography@1.4:", type=("build", "run"))
    depends_on("py-defusedxml@0.5.0:", type=("build", "run"))
    depends_on("py-python3-openid@3.0.10:", type=("build", "run"))

    depends_on("py-python-jose@3.0.0:", when="+openidconnect", type=("build", "run"))
