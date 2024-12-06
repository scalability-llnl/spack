# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParamsValidationcompiler(PerlPackage):
    """Params::ValidationCompiler - Build an optimized subroutine parameter validator once,
    use it forever"""

    homepage = "https://metacpan.org/pod/Params::ValidationCompiler"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Params-ValidationCompiler-0.31.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.31", sha256="7b6497173f1b6adb29f5d51d8cf9ec36d2f1219412b4b2410e9d77a901e84a6d")

    depends_on("perl-eval-closure", type=("build", "run", "test"))
    depends_on("perl-exception-class", type=("build", "run", "test"))
    depends_on("perl-specio@0.14:", type=("build", "test"))
    depends_on("perl-test-without-module", type=("build", "test"))
    depends_on("perl-test2-plugin-nowarnings", type=("build", "test"))
    depends_on("perl-test2-suite", type=("build", "test"))
