# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySgp4(PythonPackage):
    """Track earth satellite TLE orbits using up-to-date 2010 version of SGP4"""

    homepage = "https://github.com/brandon-rhodes/python-sgp4"
    pypi = "sgp4/sgp4-1.4.tar.gz"

    license("MIT")

    version("1.4", sha256="1fb3cdbc11981a9ff34a032169f83c1f4a2877d1b6c295aed044e1d890b73892")

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
