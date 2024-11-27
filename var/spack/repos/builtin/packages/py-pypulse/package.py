# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypulse(PythonPackage):
    """Pulse is a package used to handle PSRFITS files and perform subsequent
    analyses on pulse profiles."""

    homepage = "https://github.com/mtlam/PyPulse"
    pypi = "PyPulse/PyPulse-0.0.1.tar.gz"

    license("BSD-3-Clause")

    version("0.1.1", sha256="89cb362d2108215784f5b0df8e79311f7856f0da705ce4d77d4e884ca6c651b4")
    version("0.0.1", sha256="239823737644bdf1e09e23e81b3fc439db096aa589581d9fa2b5717f1572e75b")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-astropy", type=("build", "run"))
