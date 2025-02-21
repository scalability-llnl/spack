# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgdal(RPackage):
    """Bindings for the 'Geospatial' Data Abstraction Library.

    Provides bindings to the 'Geospatial' Data Abstraction Library ('GDAL') (>=
    1.11.4) and access to projection/transformation operations from the 'PROJ'
    library. Use is made of classes defined in the 'sp' package. Raster and
    vector map data can be imported into R, and raster and vector 'sp' objects
    exported. The 'GDAL' and 'PROJ' libraries are external to the package, and,
    when installing the package from source, must be correctly installed first;
    it is important that 'GDAL' < 3 be matched with 'PROJ' < 6. From 'rgdal'
    1.5-8, installed with to 'GDAL' >=3, 'PROJ' >=6 and 'sp' >= 1.4, coordinate
    reference systems use 'WKT2_2019' strings, not 'PROJ' strings. 'Windows'
    and 'macOS' binaries (including 'GDAL', 'PROJ' and their dependencies) are
    provided on 'CRAN'."""

    cran = "rgdal"

    version("1.6-7", sha256="555cedfdadb05db90b061d4b056f96d8b7010c00ea54bc6c1bbcc7684fadae33")
    version(
        "1.6-6",
        sha256="d742d7aadfc004771e61cac28a1faffeb4dbda981dea19115be11c541087399a",
        deprecated=True,
    )
    version(
        "1.6-2",
        sha256="7eab4b0adaa788b985cd33da214799d562a943f5788631ebd1301dfc69ca033d",
        deprecated=True,
    )
    version(
        "1.5-32",
        sha256="4583a4e187492eb936b59bc6bfeefea687b115bc3ae25172e0ed348b38f473ed",
        deprecated=True,
    )
    version(
        "1.5-28",
        sha256="7f54432cfa8c0db463f68e8856c3ca0a90671dc841ac5203af049eb318e261a2",
        deprecated=True,
    )
    version(
        "1.5-19",
        sha256="6fbfd71b19e7b8d9dbddc91cb1eef8890c74a1e2bf8f619da165ff51bf1231b2",
        deprecated=True,
    )
    version(
        "1.5-18",
        sha256="53467c19bc93d8ea311458eaa281c8c456168ab75e84d76ef5cc6c00f53122df",
        deprecated=True,
    )
    version(
        "1.4-4",
        sha256="2532e76e0af27d145f799d70006a5dbecb2d3be698e3d0bbf580f4c41a34c5d7",
        deprecated=True,
    )
    version(
        "1.3-9",
        sha256="3e44f88d09894be4c0abd8874d00b40a4a5f4542b75250d098ffbb3ba41e2654",
        deprecated=True,
    )
    version(
        "1.2-16",
        sha256="017fefea4f9a6d4540d128c707197b7025b55e4aff98fc763065366b025b03c9",
        deprecated=True,
    )

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.5:")
    depends_on("r-sp@1.1-0:", type=("build", "run"))
    depends_on("gdal@1.11.4:")
    depends_on("proj@4.8.0:5", when="@:1.3-9")
    depends_on("proj@4.8.0:", when="@1.4-2:")

    conflicts("^proj@:5", when="^gdal@3:")
    conflicts("^proj@6:", when="^gdal@:2")
