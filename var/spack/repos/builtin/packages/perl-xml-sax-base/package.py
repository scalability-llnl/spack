# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlSaxBase(PerlPackage):
    """This module has a very simple task - to be a base class for PerlSAX
    drivers and filters. It's default behaviour is to pass the input directly
    to the output unchanged. It can be useful to use this module as a base
    class so you don't have to, for example, implement the characters()
    callback."""

    homepage = "https://metacpan.org/pod/XML::SAX::Base"
    url = "https://cpan.metacpan.org/authors/id/G/GR/GRANTM/XML-SAX-Base-1.09.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.09", sha256="66cb355ba4ef47c10ca738bd35999723644386ac853abbeb5132841f5e8a2ad0")
