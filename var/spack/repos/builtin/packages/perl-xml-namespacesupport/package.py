# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlNamespacesupport(PerlPackage):
    """This module offers a simple to process namespaced XML names (unames)
    from within any application that may need them. It also helps maintain a
    prefix to namespace URI map, and provides a number of basic checks."""

    homepage = "https://metacpan.org/pod/XML::NamespaceSupport"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PERIGRIN/XML-NamespaceSupport-1.12_9.tar.gz"

    license("GPL-1.0-or-later")

    version("1.12_9", sha256="2e84a057f0a8c845a612d212742cb94fca4fc8a433150b5721bd448f77d1e4a9")
