# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXlrd(PythonPackage):
    """Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files"""

    homepage = "http://www.python-excel.org/"
    pypi = "xlrd/xlrd-0.9.4.tar.gz"

    version("2.0.1", sha256="f72f148f54442c6b056bf931dbc34f986fd0c3b0b6b5a58d013c9aef274d0c88")
    version("0.9.4", sha256="8e8d3359f39541a6ff937f4030db54864836a06e42988c452db5b6b86d29ea72")

    depends_on("python@2.7:2.8,3.6:", when="@2:", type=("build", "run"))
    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
