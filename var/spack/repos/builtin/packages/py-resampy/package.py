# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResampy(PythonPackage):
    """Efficient sample rate conversion in python"""

    homepage = "https://github.com/bmcfee/resampy"
    pypi = "resampy/resampy-0.2.2.tar.gz"

    license("ISC")

    version("0.2.2", sha256="62af020d8a6674d8117f62320ce9470437bb1d738a5d06cd55591b69b463929e")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.10:", type=("build", "run"))
    depends_on("py-scipy@0.13:", type=("build", "run"))
    depends_on("py-numba@0.32:", type=("build", "run"))
    depends_on("py-six@1.3:", type=("build", "run"))
