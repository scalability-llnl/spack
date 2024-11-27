# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBigfloat(PythonPackage):
    """Arbitrary-precision correctly-rounded floating-point arithmetic, via MPFR."""

    homepage = "https://github.com/mdickinson/bigfloat"
    pypi = "bigfloat/bigfloat-0.4.0.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.4.0", sha256="58b96bde872aca5989d13d82eba3acf2aa1b94e22117dd72a16ba5911b0c0cb8")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("gmp", type="link")
    depends_on("mpfr", type=("build", "link"))
