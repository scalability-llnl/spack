# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlSax(PerlPackage):
    """XML::SAX is a SAX parser access API for Perl. It includes classes and
    APIs required for implementing SAX drivers, along with a factory class for
    returning any SAX parser installed on the user's system."""

    homepage = "https://metacpan.org/pod/XML::SAX"
    url = "https://cpan.metacpan.org/authors/id/G/GR/GRANTM/XML-SAX-1.02.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.02", sha256="4506c387043aa6a77b455f00f57409f3720aa7e553495ab2535263b4ed1ea12a")

    depends_on("perl-xml-namespacesupport", type=("build", "run"))
    depends_on("perl-xml-sax-base", type=("build", "run"))
