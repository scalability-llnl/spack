# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastcov(PythonPackage):
    """
    A parallelized gcov wrapper for generating intermediate coverage formats
    fast
    """

    homepage = "https://github.com/RPGillespie6/fastcov"
    pypi = "fastcov/fastcov-1.13.tar.gz"

    maintainers("haampie")

    license("MIT")

    version("1.13", sha256="ec8a5271f90a2f8b894cb999e262c33e225ed6072d9a6ca38f636f88cc0543e8")

    # Depends on gcov too, but that's installed with the compiler
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@38.3:", type="build")
