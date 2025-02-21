# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZcBuildout(PythonPackage):
    """System for managing development buildouts"""

    pypi = "zc.buildout/zc.buildout-2.13.1.tar.gz"

    license("ZPL-2.1")

    version("2.13.1", sha256="3d14d07226963a517295dfad5879d2799e2e3b65b2c61c71b53cb80f5ab11484")

    depends_on("py-setuptools@8.0:", type=("build", "run"))
