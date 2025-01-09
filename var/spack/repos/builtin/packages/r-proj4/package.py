# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProj4(RPackage):
    """A simple interface to the PROJ.4 cartographic projections library.

    A simple interface to lat/long projection and datum transformation of the
    PROJ.4 cartographic projections library. It allows transformation of
    geographic coordinates from one projection and/or datum to another."""

    cran = "proj4"

    license("GPL-2.0-only")

    version("1.0-14", sha256="d3d571da92136666dd3658b6006a7d4d4254cdeada5cda21b05b0c0e692a00b6")
    version("1.0-12", sha256="4aeb8a54d5b459674093c76068b92dbd3ce99a4e5db8829fbae868c2e43776f8")
    version("1.0-11", sha256="c5f186530267005d53cc2e86849613b254ca4515a8b10310146f712d45a1d11d")
    version("1.0-10.1", sha256="66857cbe5cba4930b18621070f9a7263ea0d8ddc3e5a035a051a1496e4e1da19")
    version("1.0-10", sha256="5f396f172a17cfa9821a390f11ff7d3bff3c92ccf585572116dec459c621d1d0")
    version("1.0-8.1", sha256="a3a2a8f0014fd79fa34b5957440fd38299d8e97f1a802a61a068a6c6cda10a7e")

    depends_on("r@2.0.0:", type=("build", "run"))
    depends_on("proj@4.4.6:7", when="@:1.0-8")
    depends_on("proj@4.4.6:")

    # This is needed because the configure script links to sqlite3
    depends_on("sqlite", when="@1.0-10.1:")
