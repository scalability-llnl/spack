# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlWriter(PerlPackage):
    """XML::Writer is a helper module for Perl programs that write an XML
    document. The module handles all escaping for attribute values and
    character data and constructs different types of markup, such as tags,
    comments, and processing instructions.

    By default, the module performs several well-formedness checks to catch
    errors during output. This behaviour can be extremely useful during
    development and debugging, but it can be turned off for production-grade
    code.

    The module can operate either in regular mode in or Namespace processing
    mode. In Namespace mode, the module will generate Namespace Declarations
    itself, and will perform additional checks on the output."""

    homepage = "https://metacpan.org/pod/XML::Writer"
    url = "https://cpan.metacpan.org/authors/id/J/JO/JOSEPHW/XML-Writer-0.625.tar.gz"

    version("0.900", sha256="73c8f5bd3ecf2b350f4adae6d6676d52e08ecc2d7df4a9f089fa68360d400d1f")
    version("0.625", sha256="e080522c6ce050397af482665f3965a93c5d16f5e81d93f6e2fe98084ed15fbe")
