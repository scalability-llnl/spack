# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataDumper(PerlPackage):
    """Stringified perl data structures, suitable for both printing and eval"""

    homepage = "https://metacpan.org/pod/Data::Dumper"
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/Data-Dumper-2.173.tar.gz"

    version("2.173", sha256="697608b39330988e519131be667ff47168aaaaf99f06bd2095d5b46ad05d76fa")
