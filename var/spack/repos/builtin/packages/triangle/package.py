# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Triangle(Package):
    """Triangle is a two-dimensional mesh generator and Delaunay
    triangulator. Triangle generates exact Delaunay triangulations,
    constrained Delaunay triangulations, conforming Delaunay
    triangulations, Voronoi diagrams, and high-quality triangular
    meshes."""

    homepage = "https://www.cs.cmu.edu/~quake/triangle.html"
    url = "https://www.netlib.org/voronoi/triangle.zip"

    license("Unlicense")

    version("1.6", sha256="1766327add038495fa3499e9b7cc642179229750f7201b94f8e1b7bee76f8480")

    depends_on("libx11", type="link")

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)

        install("triangle", prefix.bin)
        install("showme", prefix.bin)
