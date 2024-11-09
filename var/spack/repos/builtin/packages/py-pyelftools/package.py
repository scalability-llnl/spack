# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyelftools(PythonPackage):
    """A pure-Python library for parsing and analyzing ELF files and DWARF
    debugging information"""

    homepage = "https://github.com/eliben/pyelftools"
    pypi = "pyelftools/pyelftools-0.26.tar.gz"

    license("Unlicense")

    version("0.29", sha256="ec761596aafa16e282a31de188737e5485552469ac63b60cfcccf22263fd24ff")
    version("0.28", sha256="53e5609cac016471d40bd88dc410cd90755942c25e58a61021cfdf7abdfeacff")
    version("0.27", sha256="cde854e662774c5457d688ca41615f6594187ba7067af101232df889a6b7a66b")
    version("0.26", sha256="86ac6cee19f6c945e8dedf78c6ee74f1112bd14da5a658d8c9d4103aed5756a2")
    version("0.25", sha256="89c6da6f56280c37a5ff33468591ba9a124e17d71fe42de971818cbff46c1b24")
    version("0.24", sha256="e9dd97d685a5b96b88a988dabadb88e5a539b64cd7d7927fac9a7368dc4c459c")
    version("0.23", sha256="fc57aadd096e8f9b9b03f1a9578f673ee645e1513a5ff0192ef439e77eab21de")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
