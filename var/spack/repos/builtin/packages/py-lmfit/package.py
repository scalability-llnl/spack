# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLmfit(PythonPackage):
    """Least-Squares Minimization with Bounds and Constraints"""

    homepage = "https://lmfit.github.io/lmfit-py/"
    pypi = "lmfit/lmfit-0.9.5.tar.gz"

    license("BSD-3-Clause")

    version("1.0.2", sha256="67090ce56685cf7f92bd7358a1e7d4ad862b3758988109ec440e9825e5184b45")
    version("1.0.1", sha256="d249eb756899360f4d2a544c9458f47fc8f765ac22c09e099530585fd64e286e")
    version("0.9.15", sha256="cd7bdf47c09a3d49f30dff9a1c7f778973d15d1e1b5dc642f14c22f6630eaf2f")
    version("0.9.5", sha256="eebc3c34ed9f3e51bdd927559a5482548c423ad5a0690c6fdcc414bfb5be6667")

    depends_on("python@3.6:", type=("build", "run"), when="@1:")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@0.9.15")

    depends_on("py-asteval@0.9.16:", type=("build", "run"), when="@0.9.15:")

    depends_on("py-numpy@1.5:", type=("build", "run"), when="@0.9.5:")
    depends_on("py-numpy@1.16:", type=("build", "run"), when="@0.9.15:")

    depends_on("py-scipy@0.14:", type=("build", "run"), when="@0.9.5")
    depends_on("py-scipy@1.2:", type=("build", "run"), when="@0.9.15:")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.11:", type=("build", "run"), when="@0.9.15")
    depends_on("py-uncertainties@3.0.1:", type=("build", "run"), when="@0.9.15:")
