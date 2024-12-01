# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlScalarUtilNumeric(PerlPackage):
    """This module exports a number of wrappers around perl's builtin grok_number
    function, which returns the numeric type of its argument, or 0 if it
    isn't numeric."""

    homepage = "https://metacpan.org/pod/Scalar::Util::Numeric"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHOCOLATE/Scalar-Util-Numeric-0.40.tar.gz"

    version("0.40", sha256="d7501b6d410703db5b1c1942fbfc41af8964a35525d7f766058acf5ca2cc4440")
