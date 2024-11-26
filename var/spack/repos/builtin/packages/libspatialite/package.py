# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspatialite(AutotoolsPackage):
    """SpatiaLite is an open source library intended to extend the
    SQLite core to support fully fledged Spatial SQL capabilities."""

    homepage = "https://www.gaia-gis.it"
    url = "https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0a.tar.gz"

    license("MPL-1.1")

    version("5.1.0", sha256="43be2dd349daffe016dd1400c5d11285828c22fea35ca5109f21f3ed50605080")
    version("5.0.1", sha256="eecbc94311c78012d059ebc0fae86ea5ef6eecb13303e6e82b3753c1b3409e98")
    version(
        "5.0.0-beta0",
        sha256="caacf5378a5cfab9b8e98bb361e2b592e714e21f5c152b795df80d0ab1da1c42",
        deprecated=True,
    )
    version("5.0.0", sha256="7b7fd70243f5a0b175696d87c46dde0ace030eacc27f39241c24bac5dfac6dac")
    version(
        "4.3.0a",
        sha256="88900030a4762904a7880273f292e5e8ca6b15b7c6c3fb88ffa9e67ee8a5a499",
        deprecated=True,
    )
    version(
        "3.0.1",
        sha256="4983d6584069fd5ff0cfcccccee1015088dab2db177c0dc7050ce8306b68f8e6",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("freexl")
    depends_on("freexl@2:", when="@5.1:")
    depends_on("geos")
    depends_on("geos@:3.9", when="@:5.0.0")
    depends_on("iconv")
    depends_on("librttopo", when="@5.0.1:")
    depends_on("libxml2")
    depends_on("minizip", when="@5.0.0:")
    depends_on("proj")
    depends_on("proj@:5", when="@:4")
    depends_on("sqlite+rtree")
