# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRefUtil(PerlPackage):
    """Utility functions for checking references"""

    homepage = "https://metacpan.org/pod/Ref::Util"
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARC/Ref-Util-0.204.tar.gz"

    maintainers("EbiArnie")

    license("MIT")

    version("0.204", sha256="415fa73dbacf44f3d5d79c14888cc994562720ab468e6f71f91cd1f769f105e1")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
