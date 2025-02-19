# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class StickyVariant(AutotoolsPackage):
    """Package with a sticky variant and a conflict"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("allow-gcc", description="", default=False, sticky=True)

    conflicts("%gcc", when="~allow-gcc")
