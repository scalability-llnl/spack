# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMunsell(RPackage):
    """Utilities for Using Munsell Colours.

    Provides easy access to, and manipulation of, the Munsell colours.
    Provides a mapping between Munsell's original notation (e.g. "5R 5/10") and
    hexadecimal strings suitable for use directly in R graphics. Also provides
    utilities to explore slices through the Munsell colour tree, to transform
    Munsell colours and display colour palettes."""

    cran = "munsell"

    license("MIT")

    version("0.5.1", sha256="03a2fd9ac40766cded96dfe33b143d872d0aaa262a25482ce19161ca959429a6")
    version("0.5.0", sha256="d0f3a9fb30e2b5d411fa61db56d4be5733a2621c0edf017d090bdfa5e377e199")
    version("0.4.3", sha256="397c3c90af966f48eebe8f5d9e40c41b17541f0baaa102eec3ea4faae5a2bd49")

    depends_on("r-colorspace", type=("build", "run"))
