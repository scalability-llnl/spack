# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsubfn(RPackage):
    """Utilities for Strings and Function Arguments.

    gsubfn is like gsub but can take a replacement function or certain other
    objects instead of the replacement string. Matches and back references are
    input to the replacement function and replaced by the function output.
    gsubfn can be used to split strings based on content rather than delimiters
    and for quasi-perl-style string interpolation. The package also has
    facilities for translating formulas to functions and allowing such formulas
    in function calls instead of functions. This can be used with R functions
    such as apply, sapply, lapply, optim, integrate, xyplot, Filter and any
    other function that expects another function as an input argument or
    functions like cat or sql calls that may involve strings where substitution
    is desirable."""

    cran = "gsubfn"

    license("GPL-2.0-or-later")

    version("0.7", sha256="89351df9e65722d2862f26a0a3985666de3c86e8400808ced8a6eb6e165a4602")
    version("0.6-6", sha256="bbc5d29bb48e836407f81880aeb368544a54a5513dacb3411c9838180723dda4")

    depends_on("r-proto", type=("build", "run"))
