# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbi(PerlPackage):
    """The DBI is the standard database interface module for Perl. It defines
    a set of methods, variables and conventions that provide a consistent
    database interface independent of the actual database being used."""

    homepage = "https://dbi.perl.org/"
    url = "https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/DBI-1.645.tgz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.645", sha256="e38b7a5efee129decda12383cf894963da971ffac303f54cc1b93e40e3cf9921")
    version("1.643", sha256="8a2b993db560a2c373c174ee976a51027dd780ec766ae17620c20393d2e836fa")
    version("1.636", sha256="8f7ddce97c04b4b7a000e65e5d05f679c964d62c8b02c94c1a7d815bb2dd676c")

    def url_for_version(self, version):
        if version <= Version("1.643"):
            return f"http://search.cpan.org/CPAN/authors/id/T/TI/TIMB/DBI-{version}.tar.gz"
        else:
            return f"https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/DBI-{version}.tgz"
