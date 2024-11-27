# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSlugify(PythonPackage):
    """A Python Slugify application that handles Unicode"""

    homepage = "https://github.com/un33k/python-slugify"
    pypi = "python-slugify/python-slugify-4.0.0.tar.gz"

    license("MIT")

    version("4.0.0", sha256="a8fc3433821140e8f409a9831d13ae5deccd0b033d4744d94b31fea141bdd84c")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-text-unidecode@1.3:", type=("build", "run"))
