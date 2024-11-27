# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXmlplain(PythonPackage):
    """XML as plain object module."""

    homepage = "https://github.com/guillon/xmlplain"
    pypi = "xmlplain/xmlplain-1.6.0.tar.gz"

    maintainers("LydDeb")

    license("Unlicense")

    version("1.6.0", sha256="a9ccfa8ab36e4df1b0580458312501b7ae7625bad3c4fcc1b8c124aad775d8e3")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
