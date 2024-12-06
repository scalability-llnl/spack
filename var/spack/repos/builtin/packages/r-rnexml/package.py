# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRnexml(RPackage):
    """Semantically Rich I/O for the 'NeXML' Format.

    Provides access to phyloinformatic data in 'NeXML' format. The package
    should add new functionality to R such as the possibility to manipulate
    'NeXML' objects in more various and refined way and compatibility with
    'ape' objects."""

    cran = "RNeXML"

    version("2.4.11", sha256="246913cbb0e816401bb8e37dda20646202547f5cc8379c9dadf832f61d6cfd46")
    version("2.4.8", sha256="26d429f95afe2e24d79eb7b0d3eeec4068e7d33b715abb8f48f380e0ccbbb850")
    version("2.4.7", sha256="cb311d6dda33a95521a6df360a2d2f4e6d6bc6b330ac5e19ea721ca665bce6fe")
    version("2.4.5", sha256="2b667ecb6400e4c0c125ca73a98cde81330cde3a85b764261f77159e702754f3")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-ape@3.1:", type=("build", "run"))
    depends_on("r-xml@3.95:", type=("build", "run"))
    depends_on("r-plyr@1.8:", type=("build", "run"))
    depends_on("r-reshape2@1.2.2:", type=("build", "run"))
    depends_on("r-httr@0.3:", type=("build", "run"))
    depends_on("r-uuid@0.1-1:", type=("build", "run"))
    depends_on("r-dplyr@0.5.0:", type=("build", "run"))
    depends_on("r-dplyr@0.7.0:", type=("build", "run"), when="@2.4.8:")
    depends_on("r-tidyr@0.3.1:", type=("build", "run"))
    depends_on("r-stringr@1.0:", type=("build", "run"))
    depends_on("r-stringi", type=("build", "run"))
    depends_on("r-xml2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@2.4.7:")
    depends_on("r-lazyeval@0.1.0:", type=("build", "run"), when="@:2.4.7")
