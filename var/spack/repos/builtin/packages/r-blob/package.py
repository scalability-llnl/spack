# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBlob(RPackage):
    """A Simple S3 Class for Representing Vectors of Binary Data ('BLOBS').

    R's raw vector is useful for storing a single binary object.  What if you
    want to put a vector of them in a data frame? The blob package provides the
    blob object, a list of raw vectors, suitable for use as a column in data
    frame."""

    cran = "blob"

    license("MIT")

    version("1.2.4", sha256="d08922ebc4147d930fe4762b1b289935217308c6d3fcaa5ae028ce3f5cf2728f")
    version("1.2.3", sha256="2d88d683ee3d1b56b332b5c7769979b5d3994b5d9285ea634ec919576da3631b")
    version("1.2.2", sha256="4976053c65994c769a4c22b4553bea0bd9c623b3b991dbaf023d2a164770c7fa")
    version("1.2.1", sha256="ef54bc7a9646c1b73f4d2f60c869b4f1940bc3505874175114297ad7772d8bea")
    version("1.2.0", sha256="1af1cfa28607bc0e2f1f01598a00a7d5d1385ef160a9e79e568f30f56538e023")
    version("1.1.0", sha256="16d6603df3ddba177f0ac4d9469c938f89131c4bf8834345db838defd9ffea16")

    depends_on("r-rlang", type=("build", "run"), when="@1.2.0:")
    depends_on("r-vctrs@0.2.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-vctrs@0.2.1:", type=("build", "run"), when="@1.2.1:")

    depends_on("r-prettyunits", type=("build", "run"), when="@1.2.0")
    depends_on("r-tibble", type=("build", "run"), when="@:1.1.0")
