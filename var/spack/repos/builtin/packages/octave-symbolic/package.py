# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveSymbolic(OctavePackage, SourceforgePackage):
    """Adds symbolic calculation features to GNU Octave.
    These include common Computer Algebra System tools such as algebraic operations,
    calculus, equation solving, Fourier and Laplace transforms, variable precision
    arithmetic and other features.
    Compatibility with other symbolic toolboxes is intended."""

    homepage = "https://octave.sourceforge.io/symbolic/"
    sourceforge_mirror_path = "octave/symbolic-2.9.0.tar.gz"

    license("GPL-3.0-only")

    version("2.9.0", sha256="089ec44a0a49417a8b78797e87f338da6a6e227509f3080724996483d39b23cb")

    extends("octave@4.2.0:")
