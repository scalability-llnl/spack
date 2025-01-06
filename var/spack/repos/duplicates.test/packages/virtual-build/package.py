# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VirtualBuild(Package):
    """A package that has a pure build virtual dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    version("1.0.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("pkgconfig", type="build")
