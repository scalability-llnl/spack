# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLibxmlPerl(PerlPackage):
    """libxml-perl is a collection of smaller Perl modules, scripts, and
    documents for working with XML in Perl.  libxml-perl software works in
    combination with XML::Parser, PerlSAX, XML::DOM, XML::Grove and others."""

    homepage = "https://metacpan.org/release/libxml-perl"
    url = "https://cpan.metacpan.org/authors/id/K/KM/KMACLEOD/libxml-perl-0.08.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.08", sha256="4571059b7b5d48b7ce52b01389e95d798bf5cf2020523c153ff27b498153c9cb")
