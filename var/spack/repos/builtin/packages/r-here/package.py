# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHere(RPackage):
    """A Simpler Way to Find Your Files.

    Constructs paths to your project's files. Declare the relative path of a
    file within your project with 'i_am()'. Use the 'here()' function as a
    drop-in replacement for 'file.path()', it will always locate the files
    relative to your project root."""

    cran = "here"

    license("MIT")

    version("1.0.1", sha256="08ed908033420d3d665c87248b3a14d1b6e2b37844bf736be620578c20ca346b")

    depends_on("r-rprojroot@2.0.2:", type=("build", "run"))
