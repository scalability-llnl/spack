# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListMoreutils(PerlPackage):
    """Provide the stuff missing in List::Util"""

    homepage = "http://search.cpan.org/~rehsack/List-MoreUtils/lib/List/MoreUtils.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RE/REHSACK/List-MoreUtils-0.428.tar.gz"

    version('0.428', sha256='713e0945d5f16e62d81d5f3da2b6a7b14a4ce439f6d3a7de74df1fd166476cc2')

    depends_on('perl-exporter-tiny', type=('build', 'run'))
    depends_on('perl-list-moreutils-xs', type=('build', 'run'))
