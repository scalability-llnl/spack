# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlDomXpath(PerlPackage):
    """XML::DOM::XPath allows you to use XML::XPath methods to query a DOM.
    This is often much easier than relying only on getElementsByTagName."""

    homepage = "https://metacpan.org/pod/XML::DOM::XPath"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIROD/XML-DOM-XPath-0.14.tar.gz"

    version("0.14", sha256="0173a74a515211997a3117a47e7b9ea43594a04b865b69da5a71c0886fa829ea")

    depends_on("perl-xml-dom", type=("build", "run"))
    depends_on("perl-xml-xpathengine", type=("build", "run"))
