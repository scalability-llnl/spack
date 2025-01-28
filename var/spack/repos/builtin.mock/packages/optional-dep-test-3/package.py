# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OptionalDepTest3(Package):
    """Depends on the optional-dep-test package"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/optional-dep-test-3-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("var", default=False)

    depends_on("pkg-a", when="~var")
    depends_on("pkg-b", when="+var")
