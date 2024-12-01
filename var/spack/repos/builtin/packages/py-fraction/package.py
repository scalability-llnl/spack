# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFraction(PythonPackage):
    """
    Fraction carries out all the fraction operations including addition, subtraction, multiplicati
    on, division, reciprocation.
    """

    homepage = "https://github.com/bradley101/fraction"
    pypi = "Fraction/Fraction-2.2.0.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("2.2.0", sha256="2c1179f20c8b749622935fe04db1c7f2987f011f2376bdad84c2a39c8e3d0fdb")

    depends_on("py-setuptools", type="build")
