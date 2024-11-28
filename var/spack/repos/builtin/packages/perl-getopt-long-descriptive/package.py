# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGetoptLongDescriptive(PerlPackage):
    """Getopt::Long, but simpler and more powerful"""

    homepage = "https://metacpan.org/pod/Getopt::Long::Descriptive"
    url = "https://cpan.metacpan.org/authors/id/H/HD/HDP/Getopt-Long-Descriptive-0.088.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.088", sha256="5008d3694280087e03280208637916ba968013c54bee863a3c3e1185368f9e65")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-params-validate@0.97:", type=("build", "run", "test"))
    depends_on("perl-sub-exporter@0.972:", type=("build", "run", "test"))
