# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbae(AutotoolsPackage):
    """The Xbae widget set consists of the well known XbaeMatrix widget,
    and Caption and XbaeInput widgets."""

    homepage = "https://sourceforge.net/projects/xbae/"
    url = "https://sourceforge.net/projects/xbae/files/xbae/4.60.4/xbae-4.60.4.tar.gz"

    license("MIT", checked_by="wdconinc")  # Old style, Bellcore variant

    version("4.60.4", sha256="eb72702ed0a36d043f2075a9d5a4545556da1b8dab4d67d85fca92f37aeb04a8")

    depends_on("c", type="build")

    depends_on("libxext")
    depends_on("libxmu")
    depends_on("libxpm")
    depends_on("libxt")
    depends_on("motif")
