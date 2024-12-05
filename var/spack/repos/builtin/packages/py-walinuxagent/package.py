# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWalinuxagent(PythonPackage):
    """Microsoft Azure Linux Guest Agent."""

    homepage = "https://github.com/Azure/WALinuxAgent"
    url = "https://github.com/Azure/WALinuxAgent/archive/pre-v2.2.52.tar.gz"

    license("Apache-2.0")

    version("2.2.52", sha256="02c26af75827bd7042aa2285c78dee86ddb25a6a8f6bb0a85679a2df9ba56a3a")
    version("2.2.50", sha256="3b2b99552e3b35dfcbb4cabf476d0113d701eb23d2e0e61f35f0fa33cabde0a1")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyasn1", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"), when="^python@3.8:")
