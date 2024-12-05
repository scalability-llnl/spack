# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenidcClient(PythonPackage):
    """A python OpenID Connect client with token caching and management"""

    homepage = "https://github.com/puiterwijk/python-openidc-client"
    pypi = "openidc-client/openidc-client-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="680e969cae18c30adbddd6a087ed09f6a296b4937b4c8bc69be813bdbbfa9847")
    version("0.5.0", sha256="59d59d6fbfd26c5b57c53e582bdf2379274602f96133a163e7ff1ef39c363353")
    version("0.2.0", sha256="50a1f5abc1960c206a462b3b2f2da1f03abdcb542beb1d6d89d2736def228ab9")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests", type=("build", "run"))
