# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpyxl(PythonPackage):
    """A Python library to read/write Excel 2010 xlsx/xlsm files"""

    homepage = "https://openpyxl.readthedocs.org/"
    pypi = "openpyxl/openpyxl-3.1.2.tar.gz"

    license("MIT")

    version("3.1.2", sha256="a6f5977418eff3b2d5500d54d9db50c8277a368436f4e4f8ddb1be3422870184")
    version("3.0.7", sha256="6456a3b472e1ef0facb1129f3c6ef00713cebf62e736cd7a75bcc3247432f251")
    version("3.0.3", sha256="547a9fc6aafcf44abe358b89ed4438d077e9d92e4f182c87e2dc294186dc4b64")
    version("2.4.5", sha256="78c331e819fb0a63a1339d452ba0b575d1a31f09fdcce793a31bec7e9ef4ef21")
    version("2.2.0", sha256="c34e3f7e3106dbe6d792f35d9a2f01c08fdd21a6fe582a2f540e39a70e7443c4")
    version("1.8.6", sha256="aa11a4acd2765392808bca2041f6f9ba17565c72dccc3f5d876bf78effa06126")

    depends_on("py-setuptools", type="build")
    depends_on("py-et-xmlfile", when="@2.4:", type=("build", "run"))
    depends_on("py-jdcal", when="@2.2.0:3.0.6", type=("build", "run"))
