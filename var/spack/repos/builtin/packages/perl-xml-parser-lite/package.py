# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlParserLite(PerlPackage):
    """Lightweight pure-perl XML Parser (based on regexps)"""

    homepage = "https://metacpan.org/pod/XML::Parser::Lite"
    url = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/XML-Parser-Lite-0.721.tar.gz"

    version("0.722", sha256="6f90a027e1531a0e5406cf1de13c709b5216966df8f73d0bab9ab919209763ee")
    version("0.721", sha256="5862a36ecab9db9aad021839c847e8d2f4ab5a7796c61d0fb069bb69cf7908ba")

    depends_on("perl-test-requires", type=("build", "run"))
