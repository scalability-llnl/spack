# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClone(PerlPackage):
    """Clone - recursively copy Perl datatypes"""

    homepage = "https://metacpan.org/pod/Clone"
    url      = "https://cpan.metacpan.org/authors/id/G/GA/GARU/Clone-0.41.tar.gz"

    version('0.41', sha256='e8c056dcf4bc8889079a09412af70194a54a269689ba72edcd91291a46a51518')
