# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTempora(PythonPackage):
    """Objects and routines pertaining to date and time (tempora)"""

    homepage = "https://github.com/jaraco/tempora"
    pypi = "tempora/tempora-1.14.1.tar.gz"

    license("MIT")

    version("1.14.1", sha256="cb60b1d2b1664104e307f8e5269d7f4acdb077c82e35cd57246ae14a3427d2d6")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@1.15.0:", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-jaraco-functools@1.20:", type=("build", "run"))
    depends_on("python@2.7:", type=("build", "run"))
