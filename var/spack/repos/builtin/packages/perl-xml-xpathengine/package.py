# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlXpathengine(PerlPackage):
    """This module provides an XPath engine, that can be re-used by other
    module/classes that implement trees."""

    homepage = "https://metacpan.org/pod/XML::XPathEngine"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIROD/XML-XPathEngine-0.14.tar.gz"

    version("0.14", sha256="d2fe7bcbbd0beba1444f4a733401e7b8aa5282fad4266d42735dd74582b2e264")
