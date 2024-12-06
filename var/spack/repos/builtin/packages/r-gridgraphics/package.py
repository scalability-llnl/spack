# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGridgraphics(RPackage):
    """Redraw Base Graphics Using 'grid' Graphics.

    Functions to convert a page of plots drawn with the 'graphics' package into
    identical output drawn with the 'grid' package. The result looks like the
    original 'graphics'-based plot, but consists of 'grid' grobs and viewports
    that can then be manipulated with 'grid' functions (e.g., edit grobs and
    revisit viewports)."""

    cran = "gridGraphics"

    version("0.5-1", sha256="29086e94e63891884c933b186b35511aac2a2f9c56967a72e4050e2980e7da8b")
    version("0.4-1", sha256="b770127b71664bbf67f8853a2666c071f2b9920743eddc9f3a58ecb948b923cf")
