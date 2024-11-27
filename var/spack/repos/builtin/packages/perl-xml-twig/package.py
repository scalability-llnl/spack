# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlTwig(PerlPackage):
    """This module provides a way to process XML documents. It is build on top
    of XML::Parser.

    The module offers a tree interface to the document, while allowing you to
    output the parts of it that have been completely processed.

    It allows minimal resource (CPU and memory) usage by building the tree only
    for the parts of the documents that need actual processing, through the use
    of the twig_roots and twig_print_outside_roots options. The finish and
    finish_print methods also help to increase performances.

    XML::Twig tries to make simple things easy so it tries its best to takes
    care of a lot of the (usually) annoying (but sometimes necessary) features
    that come with XML and XML::Parser."""

    homepage = "https://metacpan.org/pod/XML::Twig"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIROD/XML-Twig-3.52.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.52", sha256="fef75826c24f2b877d0a0d2645212fc4fb9756ed4d2711614ac15c497e8680ad")

    depends_on("perl-xml-parser", type=("build", "run"))

    patch("non_interactive.patch")
