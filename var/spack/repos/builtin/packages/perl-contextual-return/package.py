# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlContextualReturn(PerlPackage):
    """Create context-sensitive return values"""

    homepage = "http://search.cpan.org/~dconway/Contextual-Return/lib/Contextual/Return.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/Contextual-Return-0.004014.tar.gz"

    version('0.004014', sha256='09fe1415e16e49a69e13c0ef6e6a4a3fd8b856f389d3f3e624d7ab3b71719f78')

    depends_on('perl-want')
