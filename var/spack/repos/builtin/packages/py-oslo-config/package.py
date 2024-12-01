# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloConfig(PythonPackage):
    """
    The Oslo configuration API supports parsing command line arguments and .ini
    style configuration files.
    """

    homepage = "https://docs.openstack.org/oslo.config/"
    pypi = "oslo.config/oslo.config-8.7.1.tar.gz"

    maintainers("haampie")

    version("8.7.1", sha256="a0c346d778cdc8870ab945e438bea251b5f45fae05d6d99dfe4953cca2277b60")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:", type="build")

    depends_on("py-debtcollector@1.2.0:", type=("build", "run"))
    depends_on("py-netaddr@0.7.18:", type=("build", "run"))
    depends_on("py-stevedore@1.20.0:", type=("build", "run"))
    depends_on("py-oslo-i18n@3.15.3:", type=("build", "run"))
    depends_on("py-rfc3986@1.2.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-requests@2.18.0:", type=("build", "run"))
    depends_on("py-importlib-metadata@1.7.0:", when="^python@:3.7", type=("build", "run"))
