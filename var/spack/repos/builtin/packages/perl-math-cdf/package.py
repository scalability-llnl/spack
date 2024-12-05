# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathCdf(PerlPackage):
    """Generate probabilities and quantiles from several statistical
    probability functions"""

    homepage = "https://metacpan.org/pod/Math::CDF"
    url = "http://search.cpan.org/CPAN/authors/id/C/CA/CALLAHAN/Math-CDF-0.1.tar.gz"

    version("0.1", sha256="7896bf250835ce47dcc813cb8cf9dc576c5455de42e822dcd7d8d3fef2125565")

    depends_on("c", type="build")  # generated
