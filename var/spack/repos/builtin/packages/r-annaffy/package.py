# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnaffy(RPackage):
    """Annotation tools for Affymetrix biological metadata.

    Functions for handling data from Bioconductor Affymetrix annotation data
    packages. Produces compact HTML and text reports including experimental
    data and URL links to many online databases. Allows searching biological
    metadata using various criteria."""

    bioc = "annaffy"

    license("LGPL-2.1-or-later")

    version("1.72.0", commit="7cb439706a7e93fb5b44ead374010077a44ea78b")
    version("1.70.0", commit="c99e81259adb39b5d8e954fd7afe7f93675229bc")
    version("1.68.0", commit="fa930c0bbdca9828a130ab06d86c65d451380830")
    version("1.66.0", commit="aa1afa1509754128d27508228c1f39f51a8da043")
    version("1.62.0", commit="ad9c37e0e7e45e0f35c208ce528ba48000b37432")
    version("1.56.0", commit="8c8e16aa0f3073880c39684fd8e554a052ec6233")
    version("1.54.0", commit="e1b3bf10515255eb994cd8bdf85697ea728c3484")
    version("1.52.0", commit="ef84030163045f702941c8d5a59fbd4a09f30e2c")
    version("1.50.0", commit="a822e20f3e961a8afa5eb23536343115a33fb259")
    version("1.48.0", commit="89a03c64ac9df5d963ed60b87893a3fffa6798a0")

    depends_on("r@2.5.0:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@1.64.2:")
    depends_on("r-go-db", type=("build", "run"))
    depends_on("r-annotationdbi@0.1.15:", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))

    depends_on("r-kegg-db", type=("build", "run"), when="@:1.62.0")
