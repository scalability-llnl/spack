# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdMysql(PerlPackage):
    """MySQL driver for the Perl5 Database Interface (DBI)"""

    homepage = "http://search.cpan.org/~michielb/DBD-mysql-4.043/lib/DBD/mysql.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MI/MICHIELB/DBD-mysql-4.043.tar.gz"

    version('4.043', sha256='629f865e8317f52602b2f2efd2b688002903d2e4bbcba5427cb6188b043d6f99')

    depends_on('perl-test-deep', type=('build', 'run'))
    depends_on('perl-dbi', type=('build', 'run'))
    depends_on('mariadb@:10.1.23')
