# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeometry(RPackage):
    """Mesh Generation and Surface Tessellation.

    Makes the 'Qhull' library <http://www.qhull.org> available in R, in a
    similar manner as in Octave and MATLAB. Qhull computes convex hulls,
    Delaunay triangulations, halfspace intersections about a point, Voronoi
    diagrams, furthest-site Delaunay triangulations, and furthest-site Voronoi
    diagrams. It runs in 2D, 3D, 4D, and higher dimensions. It implements the
    Quickhull algorithm for computing the convex hull. Qhull does not support
    constrained Delaunay triangulations, or mesh generation of non-convex
    objects, but the package does include some R functions that allow for
    this."""

    cran = "geometry"

    license("GPL-3.0-or-later")

    version("0.4.7", sha256="96204205f51b4d63c2e7a7b00365def27d131f3c9ec66db56b510046e5d2013b")
    version("0.4.6.1", sha256="52c87a43cdf414c08b8183441c44497039cba92a9cff719debf09ad8d5d7f472")
    version("0.4.6", sha256="910465a8c8043faca73bcc7c81c9249b9938677ee6649468003b438a6503f5d8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-magic", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-lpsolve", type=("build", "run"))
    depends_on("r-linprog", type=("build", "run"))
    depends_on("r-rcppprogress", type=("build", "run"))
