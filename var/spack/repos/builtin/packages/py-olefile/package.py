# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOlefile(PythonPackage):
    """Python package to parse, read and write Microsoft OLE2 files"""

    homepage = "https://www.decalage.info/python/olefileio"
    pypi = "olefile/olefile-0.44.zip"

    license("Unlicense")

    version("0.44", sha256="61f2ca0cd0aa77279eb943c07f607438edf374096b66332fae1ee64a6f0f73ad")

    depends_on("python@2.6:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
