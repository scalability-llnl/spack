# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyParseType(PythonPackage):
    """parse_type extends the parse module (opposite of string.format())."""

    homepage = "https://github.com/jenisys/parse_type"
    pypi = "parse-type/parse_type-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="20b43c660e48ed47f433bce5873a2a3d4b9b6a7ba47bd7f7d2a7cec4bec5551f")

    depends_on("py-setuptools", type="build")
    depends_on("py-parse@1.18.0:", type=("build", "run"))
    depends_on("py-six@1.11:", type=("build", "run"))
