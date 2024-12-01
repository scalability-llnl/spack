# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDulwich(PythonPackage):
    """Dulwich aims to provide an interface to Git repos
    (both local and remote) that doesn't call out to Git
    directory, but instead uses pure Python."""

    homepage = "https://www.dulwich.io"
    pypi = "dulwich/dulwich-0.20.15.tar.gz"

    license("Apache-2.0")

    version("0.21.6", sha256="30fbe87e8b51f3813c131e2841c86d007434d160bd16db586b40d47f31dd05b0")
    version("0.20.46", sha256="4f0e88ffff5db1523d93d92f1525fe5fa161318ffbaad502c1b9b3be7a067172")
    version("0.20.44", sha256="10e8d73763dd30c86a99a15ade8bfcf3ab8fe96532cdf497e8cb1d11832352b8")
    version("0.20.21", sha256="ac764c9a9b80fa61afe3404d5270c5060aa57f7f087b11a95395d3b76f3b71fd")
    version("0.20.15", sha256="fb1773373ec2af896031f8312af6962a1b8b0176a2de3fb3d84a84ec04498888")
    version("0.20.14", sha256="21d6ee82708f7c67ce3fdcaf1f1407e524f7f4f7411a410a972faa2176baec0d")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@61.2:", when="@0.21.6", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-certifi", when="@:0.20.44", type=("build", "run"))
    depends_on("py-urllib3@1.25:", when="@0.20.46:", type=("build", "run"))
    depends_on("py-urllib3@1.24.1:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
