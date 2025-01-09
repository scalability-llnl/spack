# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Goaccess(AutotoolsPackage):
    """An open source real-time web log analyzer and interactive viewer that
    runs in a terminal in *nix systems or through your browser"""

    homepage = "https://goaccess.io"
    url = "https://tar.goaccess.io/goaccess-1.9.3.tar.gz"

    maintainers("haampie")

    license("MIT", checked_by="haampie")

    version("1.9.3", sha256="49f0ee49e3c4a95f5f75f6806b0406746fcbf2f9ad971cae23e2ea95d3ec7837")

    depends_on("gettext")
    depends_on("ncurses")

    depends_on("c", type="build")
