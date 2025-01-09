# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDirtyjson(PythonPackage):
    """JSON decoder for Python that can extract data from the muck"""

    homepage = "https://github.com/codecobblers/dirtyjson"
    pypi = "dirtyjson/dirtyjson-1.0.8.tar.gz"

    license("MIT or AFL-2.1", checked_by="qwertos")

    version("1.0.8", sha256="90ca4a18f3ff30ce849d100dcf4a003953c79d3a2348ef056f1d9c22231a25fd")

    depends_on("py-setuptools", type="build")
