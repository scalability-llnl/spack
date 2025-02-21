# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFields(RPackage):
    """Tools for Spatial Data.

    For curve, surface and function fitting with an emphasis; on splines,
    spatial data, geostatistics,  and spatial statistics. The major methods;
    include cubic, and thin plate splines, Kriging, and compactly supported;
    covariance functions for large data sets. The splines and Kriging methods
    are; supported by functions that can determine the smoothing parameter;
    (nugget and sill variance) and other covariance function parameters by
    cross; validation and also by restricted maximum likelihood. For Kriging;
    there is an easy to use function that also estimates the correlation; scale
    (range parameter).  A major feature is that any covariance function;
    implemented in R and following a simple format can be used for; spatial
    prediction. There are also many useful functions for plotting; and working
    with spatial data as images. This package also contains; an implementation
    of sparse matrix methods for large spatial data; sets and currently
    requires the sparse matrix (spam) package. Use; help(fields) to get started
    and for an overview.  The fields source; code is deliberately commented and
    provides useful explanations of; numerical details as a companion to the
    manual pages. The commented; source code can be viewed by expanding the
    source code version; and looking in the R subdirectory. The reference for
    fields can be generated; by the citation function in R and has DOI
    <doi:10.5065/D6W957CT>. Development; of this package was supported in part
    by the National Science Foundation  Grant; 1417857,  the National Center
    for Atmospheric Research, and Colorado School of Mines.; See the Fields
    URL; for a vignette on using this package and some background on spatial
    statistics."""

    cran = "fields"

    license("GPL-2.0-or-later")

    version("16.2", sha256="3910950cd5476e7e3d17d00dabfa37a6491019426c74b6955a2fbe5648a3b3e4")
    version("14.1", sha256="57c4c5592443d2ee869014b3199989b5edd1aff52e24f1cd313b8f9b34a95434")
    version("13.3", sha256="c652838b1ae7eb368831522824bfbc1d1db7b9d1db5e9bb52b194098549944c3")
    version("11.6", sha256="8600d1d992c40668cc2ab01b3c17d0e1bd44a001ec7ba9f468bc0e9ef87c59db")
    version("9.9", sha256="262f03c630773b580c7162ab2a031c894ca489fd83989fd8a2f67573306e78e1")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@14.1:")
    depends_on("r-spam", type=("build", "run"))
    depends_on("r-viridis", type=("build", "run"), when="@13.3:14.2")
    depends_on("r-viridislite", type=("build", "run"), when="@14.3:")
    depends_on("r-maps", type=("build", "run"))
