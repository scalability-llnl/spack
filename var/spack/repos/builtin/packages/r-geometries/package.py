# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeometries(RPackage):
    """Convert Between R Objects and Geometric Structures.

    Geometry shapes in 'R' are typically represented by matrices (points,
    lines), with more complex shapes being lists of matrices (polygons).
    'Geometries' will convert various 'R' objects into these shapes. Conversion
    functions are available at both the 'R' level, and through 'Rcpp'."""

    cran = "geometries"

    license("MIT")

    version("0.2.4", sha256="c6292acc336bb8520b8cb3672566f993fd077cb1f6f980ae39b9c9f56b971410")
    version("0.2.2", sha256="32d3063de0f8a751382788f85ebaee5f39d68e486253c159d553bb3d72d69141")
    version("0.2.0", sha256="8cf5094f3c2458fef5d755799c766afd27c66cd1c292574a6ab532d608360314")

    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpp@1.0.10:", type=("build", "run"), when="@0.2.2:")
