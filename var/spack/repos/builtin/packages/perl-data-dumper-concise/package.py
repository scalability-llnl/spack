# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataDumperConcise(PerlPackage):
    """Less indentation and newlines plus sub deparsing"""

    homepage = "https://metacpan.org/pod/Data::Dumper::Concise"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Data-Dumper-Concise-2.023.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.023", sha256="a6c22f113caf31137590def1b7028a7e718eface3228272d0672c25e035d5853")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
