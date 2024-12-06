# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ExternalCommonPerl(Package):
    homepage = "http://www.perl.org"
    url = "http://www.cpan.org/src/5.0/perl-5.32.0.tar.gz"

    version("5.32.0", md5="be78e48cdfc1a7ad90efff146dce6cfe")
    depends_on("external-common-gdbm")
