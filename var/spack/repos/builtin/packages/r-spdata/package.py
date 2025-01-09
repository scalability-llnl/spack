# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpdata(RPackage):
    """Datasets for Spatial Analysis.

    Diverse spatial datasets for demonstrating, benchmarking and teaching
    spatial data analysis.  It includes R data of class sf (defined by the
    package 'sf'), Spatial ('sp'), and nb ('spdep'). Unlike other spatial data
    packages such as 'rnaturalearth' and 'maps',  it also contains data stored
    in a range of file formats including GeoJSON, ESRI Shapefile and
    GeoPackage.  Some of the datasets are designed to illustrate specific
    analysis techniques. cycle_hire() and cycle_hire_osm(), for example, is
    designed to illustrate point pattern analysis techniques."""

    cran = "spData"

    version("2.3.1", sha256="8c377f2123b7b274c5ca0de656ccd30aaba1b5b245be58a842395311ecc70075")
    version("2.2.2", sha256="878a58e98b6cf259432149ecb4e5d66ada59466e1b5b0dafa60ec839e90104ed")
    version("2.2.0", sha256="6e9c0a72f29021a84e9049b147c9e0186f14876a4a1663ad98bbb33440ee901f")
    version("2.0.1", sha256="c635a3e2e5123b4cdb2e6877b9b09e3d50169e1512a53b2ba2db7fbe63b990fc")
    version("0.3.8", sha256="7a61268db4fdbfb004b77d36e953cbb3fdfdac7e8bb6c500628ec6c592c79ad6")
    version("0.3.0", sha256="de24ea659541a6c795cd26a1f6a213e15061af9c97a24cba1c24ce30c6c24c98")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"), when="@0.3.8:")
    depends_on("r-raster", type=("build", "run"), when="@0.3.8:2.0.1")
