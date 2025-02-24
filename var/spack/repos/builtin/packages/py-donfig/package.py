# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDonfig(PythonPackage):
    """Donfig is a python library making package and script configuration easy"""

    homepage = "https://donfig.readthedocs.io/en/latest/"
    pypi = "donfig/donfig-0.8.1.post1.tar.gz"

    maintainers("Chrismarsh")

    license("MIT", checked_by="Chrismarsh")

    version(
        "0.8.1.post1", sha256="3bef3413a4c1c601b585e8d297256d0c1470ea012afa6e8461dc28bfb7c23f52"
    )

    depends_on("py-setuptools@62.6:", type="build")
    depends_on("py-versioneer@0.28: +toml")
    depends_on("py-pyyaml", type=("build", "run"))
