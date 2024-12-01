# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIsdparser(RPackage):
    """Parse 'NOAA' Integrated Surface Data Files.

    Tools for parsing 'NOAA' Integrated Surface Data ('ISD') files, described
    at <https://www.ncdc.noaa.gov/isd>. Data includes for example, wind speed
    and direction, temperature, cloud data, sea level pressure, and more.
    Includes data from approximately 35,000 stations worldwide, though best
    coverage is in North America/Europe/Australia. Data is stored as variable
    length ASCII character strings, with most fields optional. Included are
    tools for parsing entire files, or individual lines of data."""

    cran = "isdparser"

    license("MIT")

    version("0.4.0", sha256="6f609e8f5ae4ce2e7904401f289d60d219b8f3a2bec9f661d10afa18ab73b317")
    version("0.3.0", sha256="6c9e1d7f3661802838010d659d7c77b964423dcc9a6623402df1fe3be627b7b9")

    depends_on("r-tibble@1.2:", type=("build", "run"))
    depends_on("r-data-table@1.10.0:", type=("build", "run"))
    depends_on("r-lubridate", type=("build", "run"), when="@0.4.0:")
