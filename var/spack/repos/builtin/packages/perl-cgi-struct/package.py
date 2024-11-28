# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCgiStruct(PerlPackage):
    """Build structures from CGI data"""

    homepage = "https://metacpan.org/pod/CGI::Struct"
    url = "https://cpan.metacpan.org/authors/id/F/FU/FULLERMD/CGI-Struct-1.21.tar.gz"

    maintainers("EbiArnie")

    license("BSD")

    version("1.21", sha256="d13d8da7fdcd6d906054e4760fc28a718aec91bd3cf067a58927fb7cb1c09d6c")

    depends_on("perl-test-deep", type=("build", "link"))
