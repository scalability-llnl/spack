# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysqlite3(PythonPackage):
    """DB-API 2.0 interface for Sqlite 3.x"""

    homepage = "https://github.com/coleifer/pysqlite3"
    pypi = "pysqlite3/pysqlite3-0.4.6.tar.gz"

    license("Zlib")

    version("0.4.7", sha256="0352864898aa406beb762f4a620594c950a9a4430caab679bce574065698c8ac")
    version("0.4.6", sha256="7ec4d4c477fa96609c1517afbc33bf02747588e528e79c695de95907cea7bf30")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("sqlite", type=("build", "link", "run"))

    def patch(self):
        filter_file(
            "^include_dirs *=.*",
            "include_dirs = " + self.spec["sqlite"].headers.directories[0],
            "setup.cfg",
        )
        filter_file(
            "^library_dirs *=.*",
            "library_dirs = " + self.spec["sqlite"].libs.directories[0],
            "setup.cfg",
        )
