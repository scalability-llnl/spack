# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertthat(RPackage):
    """Easy Pre and Post Assertions.

    An extension to stopifnot() that makes it easy to declare the pre and post
    conditions that you code should satisfy, while also producing friendly
    error messages so that your users know what's gone wrong."""

    cran = "assertthat"

    license("GPL-3.0-only")

    version("0.2.1", sha256="85cf7fcc4753a8c86da9a6f454e46c2a58ffc70c4f47cac4d3e3bcefda2a9e9f")
    version("0.2.0", sha256="d73ef79b1e75293ed889a99571b237a95829c099f7da094d4763f83ea6fde5f2")
    version("0.1", sha256="1363645a9a128f615aa0641dc5f5c5abd960b1c38320492366dad1e7a5c29a37")
