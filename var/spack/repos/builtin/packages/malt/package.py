# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Malt(CMakePackage):
    """
    MALT is a memory profile tool to track mallocs in a C/C++ application and report
    allocation information (lifetime, sizes...) in a friendly web graphical interface
    by annotating the source code and proving charts.
    """

    # Project infos
    homepage = "https://memtt.github.io/malt"
    url = "https://github.com/memtt/malt/releases/download/v1.2.4/malt-1.2.4.tar.bz2"
    maintainers("svalat")

    license("CECILL-C")

    # Versions
    version("1.2.4", sha256="47068fe981b4cbbfe30eeff37767d9057992f8515106d7809ce090d3390a712f")
    version("1.2.3", sha256="edba5d9e6a11308f82b9c8b61871e47a8ae18493bf8bff7b6ff4f4a4369428de")
    version("1.2.2", sha256="543cace664203fd9eb6b7d4945c573a3e507a43da105b5dc7ac03c78e9bb1a10")
    version(
        "1.2.1",
        sha256="0e4c0743561f9fcc04dc83457386167a9851fc9289765f8b4f9390384ae3618a",
        url="https://github.com/memtt/malt/archive/v1.2.1.tar.gz",
    )

    depends_on("cxx", type="build")

    # Variants
    variant(
        "nodejs",
        default=True,
        description="Enable the installation of the Web GUI based on NodeJS",
    )
    variant(
        "qt",
        default=False,
        when="+nodejs",
        description="Build the viewer based on NodeJS + QT web toolkit (requires NodeJS too)",
    )

    # Dependencies
    depends_on("node-js@18:", type=("build", "run"), when="+nodejs")
    depends_on("libelf")
    depends_on("libunwind")
    depends_on("binutils", type="run")
    depends_on("qt", when="+qt")
