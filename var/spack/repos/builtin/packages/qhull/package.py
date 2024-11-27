# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qhull(CMakePackage):
    """Qhull computes the convex hull, Delaunay triangulation, Voronoi
    diagram, halfspace intersection about a point, furt hest-site
    Delaunay triangulation, and furthest-site Voronoi diagram. The
    source code runs in 2-d, 3-d, 4-d, and higher dimensions. Qhull
    implements the Quickhull algorithm for computing the convex
    hull. It handles roundoff errors from floating point
    arithmetic. It computes volumes, surface areas, and
    approximations to the convex hull."""

    homepage = "http://www.qhull.org"
    url = "https://github.com/qhull/qhull/archive/refs/tags/2020.2.tar.gz"

    license("custom")

    version("2020.2", sha256="59356b229b768e6e2b09a701448bfa222c37b797a84f87f864f97462d8dbc7c5")
    version("2020.1", sha256="0258bbf5de447e3d6b3968c5a7b51c08ca5d98f11f94f86621ed3e7c98365b8d")
    version("2019.1", sha256="cf7235b76244595a86b9407b906e3259502b744528318f2178155e5899d6cf9f")
    version("2015.2", sha256="8b6dd67ff77ce1ee814da84f4134ef4bdce1f1031e570b8d83019ccef58b1c00")
    version("2012.1", sha256="cb1296fbb9ec8b7d6e8f4c239ad165590616f242c7c46f790c27d8dcebe96c6a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("qhull-unused-intel-17.02.patch", when="@2015.2")

    depends_on("cmake@3.0:", type="build")

    def flag_handler(self, name, flags):
        # See https://github.com/qhull/qhull/issues/65
        if name == "cxxflags" and self.version == Version("2020.1"):
            flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    @property
    def libs(self):
        # in 2020.2 the libqhull.so library was deprecated in favor of
        # libqhull_r.so
        if self.spec.satisfies("@2020.2:"):
            return find_libraries("libqhull_r", self.prefix, shared=True, recursive=True)
        else:
            return find_libraries("libqhull", self.prefix, shared=True, recursive=True)

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
