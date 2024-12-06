# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBeeswarm(RPackage):
    """The Bee Swarm Plot, an Alternative to Stripchart.

    The bee swarm plot is a one-dimensional scatter plot like "stripchart", but
    with closely-packed, non-overlapping points."""

    cran = "beeswarm"

    license("Artistic-2.0")

    version("0.4.0", sha256="51f4339bf4080a2be84bb49a844c636625657fbed994abeaa42aead916c3d504")
    version("0.2.3", sha256="0115425e210dced05da8e162c8455526a47314f72e441ad2a33dcab3f94ac843")

    depends_on("c", type="build")  # generated
