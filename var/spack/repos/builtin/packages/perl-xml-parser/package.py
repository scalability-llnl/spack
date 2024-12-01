# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlParser(PerlPackage):
    """XML::Parser - A perl module for parsing XML documents"""

    homepage = "https://metacpan.org/pod/XML::Parser"
    url = "http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/XML-Parser-2.44.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.47", sha256="ad4aae643ec784f489b956abe952432871a622d4e2b5c619e8855accbfc4d1d8")
    version("2.46", sha256="d331332491c51cccfb4cb94ffc44f9cd73378e618498d4a37df9e043661c515d")
    version("2.44", sha256="1ae9d07ee9c35326b3d9aad56eae71a6730a73a116b9fe9e8a4758b7cc033216")

    depends_on("expat")
    depends_on("perl-libwww-perl", type=("build", "run"))

    def configure_args(self):
        args = []

        p = self.spec["expat"].prefix.lib
        args.append(f"EXPATLIBPATH={p}")
        p = self.spec["expat"].prefix.include
        args.append(f"EXPATINCPATH={p}")

        return args
