# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataDumper(PerlPackage):
    """Stringified perl data structures, suitable for both printing and eval"""

    homepage = "https://metacpan.org/pod/Data::Dumper"
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/Data-Dumper-2.173.tar.gz"

    version("2.183", sha256="e42736890b7dae1b37818d9c5efa1f1fdc52dec04f446a33a4819bf1d4ab5ad3")
    version("2.173", sha256="697608b39330988e519131be667ff47168aaaaf99f06bd2095d5b46ad05d76fa")
