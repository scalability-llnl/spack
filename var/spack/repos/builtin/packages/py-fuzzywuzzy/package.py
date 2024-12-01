# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuzzywuzzy(PythonPackage):
    """Fuzzy string matching in python."""

    homepage = "https://github.com/seatgeek/fuzzywuzzy"
    pypi = "fuzzywuzzy/fuzzywuzzy-0.18.0.tar.gz"

    license("GPL-2.0-only")

    version("0.18.0", sha256="45016e92264780e58972dca1b3d939ac864b78437422beecebb3095f8efd00e8")

    variant("speedup", default=False, description="Provide a 4-10x speedup")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-levenshtein@0.12:", when="+speedup", type=("build", "run"))
