# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfUnits(PythonPackage):
    """Units of measure as required by the Climate and Forecast (CF)
    metadata conventions.
    """

    homepage = "https://scitools.org.uk"
    pypi = "cf-units/cf-units-2.1.1.tar.gz"
    git = "https://github.com/SciTools/cf-units.git"

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("2.1.4", sha256="25f81ad994af30713ee8f5ef18ffddd83c6ec1ac308e1bd89d45de9d2e0f1c31")
    version("2.1.1", sha256="fa0ef8efd84546e61088aa23e76ebbaf7043167dc3a7f35f34549c234b543530")

    depends_on("c", type="build")  # generated

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-antlr4-python3-runtime", type=("build", "run"))
    depends_on("py-pytest-runner", type=("build"))
    depends_on("udunits")
