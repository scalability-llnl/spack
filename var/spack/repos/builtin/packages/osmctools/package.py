# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Osmctools(AutotoolsPackage):
    """A few really fast tools to convert, filter and update OpenStreetMap
    data files"""

    homepage = "https://gitlab.com/osm-c-tools/osmctools"
    url = "https://gitlab.com/osm-c-tools/osmctools/-/archive/0.9/osmctools-0.9.tar.gz"

    license("AGPL-3.0-only")

    version("0.9", sha256="2f5298be5b4ba840a04f360c163849b34a31386ccd287657885e21268665f413")
    version("0.8", sha256="54ae48717afd05707c9b1fd750dd56c33c3bae0755424ce8ca3795ee28e0ece8")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
