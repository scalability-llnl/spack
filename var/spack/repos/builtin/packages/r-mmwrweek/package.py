# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMmwrweek(RPackage):
    """The first day of any MMWR week is Sunday. MMWR week numbering is
    sequential beginning with 1 and incrementing with each week to a maximum
    of 52 or 53. MMWR week #1 of an MMWR year is the first week of the year
    that has at least four days in the calendar year. This package provides
    functionality to convert Dates to MMWR day, week, and year and the
    reverse."""

    homepage = "https://cloud.r-project.org/package=MMWRweek"
    url      = "https://cloud.r-project.org/src/contrib/MMWRweek_0.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MMWRweek"

    version('0.1.1', sha256='969fd18535f3b78dd360d62d29d5f15409fc059f4af5d345abfde711e4adbc99')
