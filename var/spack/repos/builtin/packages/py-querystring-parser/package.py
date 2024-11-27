# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuerystringParser(PythonPackage):
    """QueryString parser that correctly handles nested dictionaries."""

    homepage = "https://pypi.org/project/querystring-parser/"
    pypi = "querystring-parser/querystring_parser-1.2.4.tar.gz"

    version("1.2.4", sha256="644fce1cffe0530453b43a83a38094dbe422ccba8c9b2f2a1c00280e14ca8a62")

    depends_on("py-six", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
