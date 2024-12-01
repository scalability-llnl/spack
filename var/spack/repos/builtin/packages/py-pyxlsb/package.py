# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyxlsb(PythonPackage):
    """Excel 2007-2010 Binary Workbook (xlsb) parser"""

    pypi = "pyxlsb/pyxlsb-1.0.10.tar.gz"

    license("LGPL-3.0-only")

    version("1.0.10", sha256="8062d1ea8626d3f1980e8b1cfe91a4483747449242ecb61013bc2df85435f685")
    version("1.0.8", sha256="dcf26d6494b45d8852d68571f828c2361b74711a2e19ba03eee77f96b9210464")
    version("1.0.6", sha256="47e8230582de15ad9824a456d1d4cb36a6535f4ad5e5eb2464d31f0445b9db46")

    depends_on("py-setuptools", type="build")
