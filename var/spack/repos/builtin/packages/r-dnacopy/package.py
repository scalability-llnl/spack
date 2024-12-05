# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDnacopy(RPackage):
    """DNA copy number data analysis.

    Implements the circular binary segmentation (CBS) algorithm to segment
    DNA copy number data and identify genomic regions with abnormal copy
    number."""

    bioc = "DNAcopy"

    version("1.74.0", commit="7d22a81570c0fe76f4b5a5c25d0b8fd3696ec70e")
    version("1.72.0", commit="1a1ae854c3425aee68b060e3e7ab788db5bed08c")
    version("1.70.0", commit="9595d0ad7c78af4ed568cbd210b894d3350eae0a")
    version("1.68.0", commit="08f039f58bc2f5ed2cc3117ae817dbac333002a6")
    version("1.64.0", commit="01650266ea7a4e5c600de545fe70a1103e79b2d8")
    version("1.58.0", commit="1954745eafca990d6ddeefe84059c54a8c37df23")
    version("1.56.0", commit="e521826f2515b309921272f65db421cbe2ff961a")
    version("1.54.0", commit="fe2657936afbce8ee03221461dff4265e3ded4c4")
    version("1.52.0", commit="2632fbecec4cef3705b85676942a59188ae9bba4")
    version("1.50.1", commit="a20153029e28c009df813dbaf13d9f519fafa4e8")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
