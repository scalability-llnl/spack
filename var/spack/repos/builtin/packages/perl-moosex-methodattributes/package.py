# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoosexMethodattributes(PerlPackage):
    """Code attribute introspection"""

    homepage = "https://metacpan.org/pod/MooseX::MethodAttributes"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/MooseX-MethodAttributes-0.32.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.32", sha256="cb33886574b7d2dd39c42c0dcdc707acdb0aec7dbbde9a21c0422660368c197b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
    depends_on("perl-moosex-role-parameterized", type=("build", "test"))
    depends_on("perl-namespace-autoclean@0.08:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
