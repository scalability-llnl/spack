# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloUtils(PythonPackage):
    """
    The oslo.utils library provides support for common utility type functions,
    such as encoding, exception handling, string manipulation, and time
    handling.
    """

    homepage = "https://docs.openstack.org/oslo.utils/"
    pypi = "oslo.utils/oslo.utils-4.9.2.tar.gz"

    maintainers("haampie")

    version("4.9.2", sha256="20db285734ff6c3b50d5a6afcb2790ade0c7ba02fbc876feed43733f2c41a5c9")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type="build")

    depends_on("py-iso8601@0.1.11:", type=("build", "run"))
    depends_on("py-oslo-i18n@3.15.3:", type=("build", "run"))
    depends_on("py-pytz@2013.6:", type=("build", "run"))
    depends_on("py-netaddr@0.7.18:", type=("build", "run"))
    depends_on("py-netifaces@0.10.4:", type=("build", "run"))
    depends_on("py-debtcollector@1.2.0:", type=("build", "run"))
    depends_on("py-pyparsing@2.1.0:", type=("build", "run"))
    depends_on("py-packaging@20.4:", type=("build", "run"))
