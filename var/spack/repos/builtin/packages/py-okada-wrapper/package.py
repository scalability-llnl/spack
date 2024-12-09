# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOkadaWrapper(PythonPackage):
    """Python and MATLAB wrappers for the Okada Green's function codes"""

    homepage = "https://github.com/tbenthompson/okada_wrapper"
    pypi = "okada_wrapper/okada_wrapper-18.12.07.3.tar.gz"

    maintainers("snehring")

    license("MIT", checked_by="snehring")

    version(
        "18.12.07.3", sha256="ee296ad6e347c8df400f6f3d1badc371925add8d1af33854634c2fe1a2b2c855"
    )

    depends_on("fortran", type="build")  # generated

    # https://github.com/tbenthompson/okada_wrapper/issues/8
    depends_on("python@3:3.11", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
