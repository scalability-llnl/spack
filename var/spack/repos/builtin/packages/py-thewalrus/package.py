# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThewalrus(PythonPackage):
    """A library for the calculation of hafnians, Hermite polynomials and
    Gaussian boson sampling.
    """

    homepage = "https://github.com/XanaduAI/thewalrus"
    pypi = "thewalrus/thewalrus-0.19.0.tar.gz"

    license("Apache-2.0")

    version("0.19.0", sha256="06ff07a14cd8cd4650d9c82b8bb8301ef9a58dcdd4bafb14841768ccf80c98b9")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-dask+delayed", type=("build", "run"))
    depends_on("py-numba@0.49.1:", type=("build", "run"))
    depends_on("py-scipy@1.2.1:", type=("build", "run"))
    depends_on("py-sympy@1.5.1:", type=("build", "run"))
    depends_on("py-numpy@1.19.2:", type=("build", "run"))
