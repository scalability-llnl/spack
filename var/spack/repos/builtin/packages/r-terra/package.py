# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTerra(RPackage):
    """Spatial Data Analysis.

    Methods for spatial data analysis with raster and vector data. Raster
    methods allow for low-level data manipulation as well as high-level global,
    local, zonal, and focal computation. The predict and interpolate methods
    facilitate the use of regression type (interpolation, machine learning)
    models for spatial prediction, including with satellite remote sensing
    data. Processing of very large files is supported. See the manual and
    tutorials on <https://rspatial.org/terra/> to get started. 'terra' is very
    similar to the 'raster' package; but 'terra' can do more, is easier to use,
    and it is faster."""

    cran = "terra"

    license("GPL-3.0-or-later")

    version("1.7-78", sha256="658956b79d8a1371aefdf7300316f1756b58d436ba549ade012307684b2d4b7e")
    version("1.7-29", sha256="3f39b052a34c9f1166a342be4c25bbdc1e2c81402edb734901d63fc6fa547ca5")
    version("1.6-17", sha256="db888f4220ca511332f4d011345b2b207fcc1de26d2eae473e0eeb5dfd8bbc02")
    version("1.5-21", sha256="091ee928ccaa6561aa9f8ee6c1c99f139dc89f1653c2a76a035cca14d404f43f")
    version("1.5-17", sha256="e7ac57d1712d280616a4b5a85cd915b2b3e24fe08ee044b740588d884e6be6e7")
    version("1.5-12", sha256="865cc14ee8c3239037c08170df4011eed27cf638ac1d05f0b7cd704abf97cc19")
    version("1.4-22", sha256="b8eccfa36764577248d7b390e24af6db65fb8824c07f9b782bd6b83c4d2b3976")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpp@1.0-10:", type=("build", "run"), when="@1.7-29:")
    depends_on("gdal@2.2.3:")
    depends_on("geos@3.4.0:")
    depends_on("proj@4.9.3:")
    depends_on("sqlite")
