# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy6s(PythonPackage):
    """
    A wrapper for the 6S Radiative Transfer Model to make it easy to run
    simulations with a variety of input parameters, and to produce outputs in
    an easily processable form.
    """

    homepage = "https://py6s.rtwilson.com/"
    pypi = "py6s/Py6S-1.8.0.tar.gz"

    version("1.8.0", sha256="256162d2f1f558e601d4f79022c037a0051838ba307b9f4d1f5fcf0b46a0c277")

    depends_on("python@3:", type=("build", "run"), when="@1.8.0")
    depends_on("py-setuptools", type="build")
    depends_on("py-pysolar@0.6", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
