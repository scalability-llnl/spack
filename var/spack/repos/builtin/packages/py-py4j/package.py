# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy4j(PythonPackage):
    """Enables Python programs to dynamically access arbitrary Java
    objects."""

    homepage = "https://www.py4j.org/"
    pypi = "py4j/py4j-0.10.4.zip"

    license("BSD-3-Clause")

    maintainers("teaguesterling")

    version("0.10.9.7", sha256="0b6e5315bb3ada5cf62ac651d107bb2ebc02def3dee9d9548e3baac644ea8dbb")
    version("0.10.9.5", sha256="276a4a3c5a2154df1860ef3303a927460e02e97b047dc0a47c1c3fb8cce34db6")
    version("0.10.9.3", sha256="0d92844da4cb747155b9563c44fc322c9a1562b3ef0979ae692dbde732d784dd")
    version("0.10.9", sha256="36ec57f43ff8ced260a18aa9a4e46c3500a730cac8860e259cbaa546c2b9db2f")
    version("0.10.7", sha256="721189616b3a7d28212dfb2e7c6a1dd5147b03105f1fc37ff2432acd0e863fa5")
    version("0.10.6", sha256="d3e7ac7c2171c290eba87e70aa5095b7eb6d6ad34789c007c88d550d9f575083")
    version("0.10.4", sha256="406fbfdbcbbb398739f61fafd25724670a405a668eb08c1721d832eadce06aae")
    version("0.10.3", sha256="f4570108ad014dd52a65c2288418e31cb8227b5ecc39ad7fc7fe98314f7a26f2")

    variant("java", default=True, description="Require java via Spack instead of using system JRE")

    depends_on("py-setuptools", type="build")
    depends_on("java", when="+java", type="run")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/p/py4j/"

        if version < Version("0.10.9"):
            url += "py4j-{0}.zip"
        else:
            url += "py4j-{0}.tar.gz"

        url = url.format(version)
        return url
