# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathMatrixreal(PerlPackage):
    """Implements the data type "matrix of real numbers" (and consequently
    also "vector of real numbers")."""

    homepage = "https://metacpan.org/pod/Math::MatrixReal"
    url = "http://search.cpan.org/CPAN/authors/id/L/LE/LETO/Math-MatrixReal-2.13.tar.gz"

    version("2.13", sha256="4f9fa1a46dd34d2225de461d9a4ed86932cdd821c121fa501a15a6d4302fb4b2")

    depends_on("perl-module-build", type="build")
