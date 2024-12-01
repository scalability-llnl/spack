# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCsvkit(PythonPackage):
    """A library of utilities for working with CSV, the king of tabular file
    formats"""

    homepage = "http://csvkit.rtfd.org/"
    pypi = "csvkit/csvkit-0.9.1.tar.gz"
    git = "https://github.com/wireservice/csvkit.git"

    license("MIT")

    version("1.1.1", sha256="beddb7b78f6b22adbed6ead5ad5de4bfb31dd2c55f3211b2a2b3b65529049223")
    version("1.0.4", sha256="1353a383531bee191820edfb88418c13dfe1cdfa9dd3dc46f431c05cd2a260a0")
    version("0.9.1", sha256="92f8b8647becb5cb1dccb3af92a13a4e85702d42ba465ce8447881fb38c9f93a")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-agate@1.6.1:", when="@1:", type=("build", "run"))
    depends_on("py-agate-excel@0.2.2:", when="@1:", type=("build", "run"))
    depends_on("py-agate-dbf@0.2.2:", when="@1.0.7:", type=("build", "run"))
    depends_on("py-agate-dbf@0.2.0:", when="@1:", type=("build", "run"))
    depends_on("py-agate-sql@0.5.3:", when="@1:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-six@1.6.1:", when="@:1.0", type=("build", "run"))
    with when("@0.9.1"):
        depends_on("py-xlrd@0.7.1:", type=("build", "run"))
        depends_on("py-sqlalchemy@0.6.6:", type=("build", "run"))
        depends_on("py-openpyxl@2.2.0", type=("build", "run"))
        depends_on("py-python-dateutil@2.2", type=("build", "run"))

    @when("@0.9.1")
    def patch(self):
        # Non-existent version requirement
        filter_file("2.2.0-b1", "2.2.0", "setup.py", string=True)
