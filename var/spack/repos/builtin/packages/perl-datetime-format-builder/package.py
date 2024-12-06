# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeFormatBuilder(PerlPackage):
    """Create DateTime parser classes and objects."""

    homepage = "https://metacpan.org/pod/DateTime::Format::Builder"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-Format-Builder-0.83.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.83", sha256="61ffb23d85b3ca1786b2da3289e99b57e0625fe0e49db02a6dc0cb62c689e2f2")

    depends_on("perl-datetime@1.00:", type=("build", "run", "test"))
    depends_on("perl-datetime-format-strptime@1.04:", type=("build", "run", "test"))
    depends_on("perl-params-validate@0.72:", type=("build", "run", "test"))
