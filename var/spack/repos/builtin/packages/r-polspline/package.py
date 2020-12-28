# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPolspline(RPackage):
    """Routines for the polynomial spline fitting routines hazard regression,
       hazard estimation with flexible tails, logspline, lspec, polyclass,
       and polymars, by C. Kooperberg and co-authors.
    """

    homepage = "https://cloud.r-project.org/package=polspline"
    url      = "https://cloud.r-project.org/src/contrib/polspline_1.1.18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/polspline"

    version('1.1.18', sha256='df250ee144bfff154249ba50308f46863107ef3efb2333ad908e599ed0eb0102')
    version('1.1.17', sha256='d67b269d01105d4a6ea774737e921e66e065a859d1931ae38a70f88b6fb7ee30')
    version('1.1.16', sha256='aa3b5a1560008a1a401a65a25f19a27ba6f0a6ea185b6d093acd40e4e2818934')
    version('1.1.15', sha256='8cdbaa5ee672055a4d02f965025199ce764958f84bfa159e853feba7ee24faa7')
