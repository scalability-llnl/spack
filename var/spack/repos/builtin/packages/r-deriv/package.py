# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDeriv(RPackage):
    """Symbolic Differentiation.

    R-based solution for symbolic differentiation. It admits user-defined
    function as well as function substitution in arguments of functions to be
    differentiated. Some symbolic simplification is part of the work."""

    cran = "Deriv"

    version("4.1.3", sha256="dbdbf5ed8babf706373ae33a937d013c46110a490aa821bcd158a70f761d0f8c")
    version("4.1.2", sha256="c4b0c3f351f6df53778d48033460cf8674e7a7878fbc542085d66a9a78803ac9")
