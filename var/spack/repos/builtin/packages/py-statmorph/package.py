# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStatmorph(PythonPackage):
    """
    Python code for calculating non-parametric morphological diagnostics of galaxy
    images.
    """

    homepage = "https://github.com/vrodgom/statmorph"
    pypi = "statmorph/statmorph-0.4.0.tar.gz"

    maintainers("meyersbs")

    license("BSD-3-Clause")

    version("0.4.0", sha256="7d1bb802baf3e203ac44c630a58c5049da5eb4d85091ac35e3f5c6ee4af8b05a")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.14.0:", type=("build", "run"))
    depends_on("py-scipy@0.19:", type=("build", "run"))
    depends_on("py-scikit-image@0.14:", type=("build", "run"))
    depends_on("py-astropy@2.0:", type=("build", "run"))
    depends_on("py-photutils@0.7:", type=("build", "run"))
