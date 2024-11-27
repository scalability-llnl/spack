# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydv(PythonPackage):
    """PDV is a 1D graphics and data analysis tool, heavily based on the
    ULTRA plotting tool"""

    homepage = "https://github.com/griffin28/PyDV"
    url = "https://github.com/griffin28/PyDV/archive/pydv-2.4.2.tar.gz"

    license("BSD-3-Clause")

    version("2.4.2", sha256="46bda76e27e85beaad446455d0cc279388d455f05912a8ff8e4fb66de983992c")

    depends_on("py-setuptools", type="build")
    depends_on("py-cycler", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyside", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
