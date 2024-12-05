# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFileMagic(PythonPackage):
    """This library is a Python ctypes interface to libmagic"""

    homepage = "https://pypi.org/project/file-magic/"
    pypi = "file-magic/file-magic-0.4.1.tar.gz"

    version("0.4.1", sha256="a91d1483117f7ed48cd0238ad9be36b04824d57e9c38ea7523113989e81b9c53")

    depends_on("py-setuptools@61:", type="build")
    depends_on("file", type="run")
