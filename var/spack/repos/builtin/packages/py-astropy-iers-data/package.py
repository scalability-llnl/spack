# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstropyIersData(PythonPackage):
    """IERS Earth rotation and leap second table

    Note: This package is not meant for standalone purposes
    but is needed by AstroPy."""

    homepage = "https://github.com/astropy/astropy-iers-data"
    pypi = "astropy-iers-data/astropy_iers_data-0.2024.4.29.0.28.48.tar.gz"

    version(
        "0.2024.5.20.0.29.40",
        sha256="7fff3d3404ae8560533ac0e685db7acc02c4d8984faa4ac3d607096879fba2d1",
    )
    version(
        "0.2024.4.29.0.28.48",
        sha256="a2d5acf97e731f1d4a0eab1c8e4c7f454ddc166af06797b141202dd901bd1dfc",
    )

    depends_on("python@3.8:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-wheel", type="build")
