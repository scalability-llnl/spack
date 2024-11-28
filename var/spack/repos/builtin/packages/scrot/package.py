# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scrot(AutotoolsPackage):
    """scrot (SCReenshOT) is a simple command line screen
    capture utility that uses imlib2 to grab and save images.
    Multiple image formats are supported through imlib2's
    dynamic saver modules."""

    homepage = "https://github.com/resurrecting-open-source-projects/scrot"
    url = "https://github.com/resurrecting-open-source-projects/scrot/releases/download/1.5/scrot-1.5.tar.gz"

    license("MIT")

    version("1.6", sha256="42f64d38f04ec530c8b4ebdae04cce8b6893b2f8d30627391d390edcba917090")
    version("1.5", sha256="42fcf1c97940f4b4e34ca69990a0fc9b98991357bd6a4b67f30ebe0ccc10f093")

    depends_on("c", type="build")

    depends_on("giblib", when="@:1.5")
    depends_on("imlib2")
    depends_on("libxcomposite")
    depends_on("libxfixes")
