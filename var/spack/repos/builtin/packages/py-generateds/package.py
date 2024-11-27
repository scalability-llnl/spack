# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenerateds(PythonPackage):
    """Generate Python data structures and XML parser from Xschema."""

    homepage = "http://www.davekuhlman.org/generateDS.html"
    pypi = "generateDS/generateDS-2.41.4.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("2.43.2", sha256="e86f033f4d93414dd5b04cab9544a68b8f46d559073d85cd0990266b7b9ec09e")
    version("2.43.1", sha256="2d3d71b42a09ba153bc51d2204324d04e384d0f15e41bdba881ee2daff9bbd68")
    version("2.42.2", sha256="1d322aa7e074c262062b068660dd0c53bbdb0bb2b30152bb9e0074bd29fd365a")
    version("2.42.1", sha256="87e4654449d34150802ca0cfb2330761382510d1385880f4d607cd34466abc2d")
    version("2.41.5", sha256="8800c09454bb22f8f80f2ee138072d4e58bd5b6c14dbdf0a2a7ca13f06ba72e4")
    version("2.41.4", sha256="804592eef573fa514741528a0bf9998f0c57ee29960c87f54608011f1fc722ea")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-requests@2.21:", type=("build", "run"))
