# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Udunits(AutotoolsPackage):
    """Automated units conversion"""

    homepage = "https://www.unidata.ucar.edu/software/udunits"
    url = "https://artifacts.unidata.ucar.edu/repository/downloads-udunits/2.2.28/udunits-2.2.28.tar.gz"

    maintainers("AlexanderRichert-NOAA")

    license("UCAR")

    # Unidata now only provides the latest version of each X.Y branch.
    # Older 2.2 versions have been deprecated accordingly but are still
    # available in the build cache.
    version("2.2.28", sha256="590baec83161a3fd62c00efa66f6113cec8a7c461e3f61a5182167e0cc5d579e")
    version(
        "2.2.24",
        sha256="20bac512f2656f056385429a0e44902fdf02fc7fe01c14d56f3c724336177f95",
        deprecated=True,
    )
    version(
        "2.2.23",
        sha256="b745ae10753fe82cdc7cc834e6ce471ca7c25ba2662e6ff93be147cb3d4fd380",
        deprecated=True,
    )
    version(
        "2.2.21",
        sha256="a154d1f8428c24e92723f9e50bdb5cc00827e3f5ff9cba64d33e5409f5c03455",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("expat")

    variant("shared", default=True, description="Build shared library")

    @property
    def libs(self):
        return find_libraries(["libudunits2"], root=self.prefix, recursive=True, shared=True)

    def configure_args(self):
        return self.enable_or_disable("shared")
