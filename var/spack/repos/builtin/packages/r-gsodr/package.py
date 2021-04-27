# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGsodr(RPackage):
    """A Global Surface Summary of the Day (GSOD) Weather Data Client for R

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

    homepage = "https://docs.ropensci.org/GSODR/"
    url      = "https://cloud.r-project.org/src/contrib/GSODR_2.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GSODR"

    version('2.1.2', sha256='4fc1d084b6c21055d8cc17a6a6dc412261aa0d4ef4079bcd73b580a8c16bf74e')
    version('2.1.1', sha256='dba732e5bd1e367b9d710e6b8924f0c02fa4546202f049124dba02bc2e3329f5')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-countrycode', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-data-table@1.11.6:', type=('build', 'run'))
    depends_on('r-future-apply', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-r-utils', type=('build', 'run'))
