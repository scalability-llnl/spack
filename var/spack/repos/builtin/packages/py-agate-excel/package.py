# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgateExcel(PythonPackage):
    """agate-excel adds read support for Excel files (xls and xlsx) to
    agate."""

    homepage = "https://agate-excel.readthedocs.io/en/latest/"
    pypi = "agate-excel/agate-excel-0.2.3.tar.gz"

    license("MIT")

    version("0.2.3", sha256="8f255ef2c87c436b7132049e1dd86c8e08bf82d8c773aea86f3069b461a17d52")

    depends_on("py-setuptools", type="build")
    depends_on("py-agate@1.5.0:", type=("build", "run"))
    depends_on("py-xlrd@0.9.4:", type=("build", "run"))
    depends_on("py-openpyxl@2.3.0:", type=("build", "run"))
