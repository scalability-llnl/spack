# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMmwrweek(RPackage):
    """Convert Dates to MMWR Day, Week, and Year.

    The first day of any MMWR week is Sunday. MMWR week numbering is sequential
    beginning with 1 and incrementing with each week to a maximum of 52 or 53.
    MMWR week #1 of an MMWR year is the first week of the year that has at
    least four days in the calendar year. This package provides functionality
    to convert Dates to MMWR day, week, and year and the reverse."""

    cran = "MMWRweek"

    license("GPL-2.0-or-later")

    version("0.1.3", sha256="1aa8b687dc3340c3f277689eb0ca529e0064a4a3a66868137f2f8ab209d133d0")
    version("0.1.1", sha256="969fd18535f3b78dd360d62d29d5f15409fc059f4af5d345abfde711e4adbc99")
