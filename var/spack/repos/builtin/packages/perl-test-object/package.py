# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestObject(PerlPackage):
    """Thoroughly testing objects via registered handlers"""

    homepage = "https://metacpan.org/pod/Test::Object"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Object-0.08.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.08", sha256="65278964147837313f4108e55b59676e8a364d6edf01b3dc198aee894ab1d0bb")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
