# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsodr(RPackage):
    """A Global Surface Summary of the Day (GSOD) Weather Data Client for R.

    Provides automated downloading, parsing, cleaning, unit conversion and
    formatting of Global Surface Summary of the Day ('GSOD') weather data from
    the from the USA National Centers for Environmental Information ('NCEI').
    Units are converted from from United States Customary System ('USCS') units
    to International System of Units ('SI').  Stations may be individually
    checked for number of missing days defined by the user, where stations with
    too many missing observations are omitted.  Only stations with valid
    reported latitude and longitude values are permitted in the final data.
    Additional useful elements, saturation vapour pressure ('es'), actual
    vapour pressure ('ea') and relative humidity ('RH') are calculated from the
    original data using the improved August-Roche-Magnus approximation
    (Alduchov & Eskridge 1996) and included in the final data set.  The
    resulting metadata include station identification information, country,
    state, latitude, longitude, elevation, weather observations and associated
    flags.  For information on the 'GSOD' data from 'NCEI', please see the
    'GSOD' 'readme.txt' file available from,
    <https://www1.ncdc.noaa.gov/pub/data/gsod/readme.txt>."""

    cran = "GSODR"

    license("MIT")

    version("4.1.1", sha256="d5bf80244b5562206f459cb0ed588c11f8edf4eb2a26e2715be7938ec6be92e0")
    version("3.1.8", sha256="f43668b14be30632086b832be83c74fa7c25e123fbce0d0203e992a0c11e7c8d")
    version("3.1.6", sha256="fbeac54e86fba1e4415b41608ca59cf50be1b421cc890eb5c5b0d6d1c9229f6a")
    version("3.1.5", sha256="37682141707d7e29fab653ccdeb154fea2c085080f686b33f1a54140608e824d")
    version("3.1.4", sha256="615ac4271b44a63064cb23632b887c60c86f4742957fc46f300423f8f75858c8")
    version("2.1.2", sha256="4fc1d084b6c21055d8cc17a6a6dc412261aa0d4ef4079bcd73b580a8c16bf74e")
    version("2.1.1", sha256="dba732e5bd1e367b9d710e6b8924f0c02fa4546202f049124dba02bc2e3329f5")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-countrycode", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-data-table@1.11.6:", type=("build", "run"), when="@:2.1.2")
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))

    depends_on("r-httr", type=("build", "run"), when="@:3.1.8")
    depends_on("r-future-apply", type=("build", "run"), when="@:2.1.2")
